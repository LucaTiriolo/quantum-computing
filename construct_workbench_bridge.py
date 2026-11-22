"""Collegamento didattico Construct Circuit Designer -> PsiQDK Workbench.

Esecuzione (da Ubuntu / WSL, nel progetto con PsiQDK installato):
    .venv/bin/python construct_workbench_bridge.py bell_pairs.circuit --once
    .venv/bin/python construct_workbench_bridge.py bell_pairs.circuit

Supporta: H, X, Z e CNOT con controllo positivo singolo.
Legge sia il formato `root.children` (salvataggio Construct) sia `operations`.
Una Routine è un contenitore: le porte annidate vengono eseguite in ordine.

IMPORTANTE: un registro etichettato `1,2,...,n` è SCHEMATICO, non un numero
concreto di qubit. Per l'esempio Bell Pairs, simuliamo solo i rail su cui
ci sono porte esplicitamente indirizzate: [0], [1] e [3] (n). Il simbolo
`...` non viene espanso. Il rail [2] è il segnaposto dei puntini.
Questa è una scelta didattica del bridge, NON una funzione nativa di Construct.
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
import time
from pathlib import Path

REF = re.compile(r"!?[A-Za-z_][A-Za-z0-9_-]*(?:\[[^\]]+\])?|\*")
ONE = re.compile(r"(?P<reg>[A-Za-z_][A-Za-z0-9_-]*)(?:\[(?P<sel>[^\]]+)\])?\Z")
DISPLAY = {"register", "label", "separator", "routine", "group", "column"}
SUPPORTED = {"hadamard", "h", "pauli_x", "x", "not", "cnot", "pauli_z", "z"}


class CircuitIssue(ValueError):
    pass


def tokenize(spec: str) -> list[str]:
    if not isinstance(spec, str) or not spec.strip():
        return []
    tokens = REF.findall(spec)
    remaining = REF.sub("", spec).replace(",", "").replace(" ", "")
    if remaining:
        raise CircuitIssue(f"Selettore di rail non riconosciuto: {spec!r}")
    return tokens


def flatten(nodes):
    """Esplora ricorsivamente Routine/Group senza perdere l'ordine delle porte."""
    for node in nodes:
        yield node
        yield from flatten(node.get("children") or [])


def reference(token: str) -> tuple[str, list[int] | None]:
    if token.startswith("!") or token == "*":
        raise CircuitIssue(f"Controllo negativo o riferimento globale non supportato: {token}")
    match = ONE.fullmatch(token)
    if not match:
        raise CircuitIssue(f"Riferimento non riconosciuto: {token}")
    reg, sel = match.group("reg", "sel")
    if sel is None or sel == "*":
        return reg, None
    try:
        # Non deduciamo dimensioni da intervalli aperti o indici negativi.
        if not re.fullmatch(r"\d+(?:\s*,\s*\d+)*", sel):
            raise ValueError("selettore non esplicito")
        return reg, [int(part.strip()) for part in sel.split(",")]
    except ValueError as exc:
        raise CircuitIssue(f"Usa indici espliciti non negativi: {token}") from exc


def parse_circuit(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("record_type") != "psiquantum.circuit":
        raise CircuitIssue("Il file non è un documento psiquantum.circuit")

    # Il file reale salvato dall'utente usa `root.children`, mentre alcuni
    # esempi della documentazione espongono `operations`.
    if isinstance(data.get("root"), dict):
        nodes = data["root"].get("children", [])
    else:
        nodes = data.get("operations", [])
    ops = list(flatten(nodes))
    registers = {op["id"]: op for op in ops if op.get("type") == "register"}
    gates = [op for op in ops if op.get("type") == "gate"]
    if not gates:
        raise CircuitIssue("Nessuna porta nel circuito")
    for op in ops:
        if op.get("type") not in DISPLAY | {"gate"}:
            raise CircuitIssue(f"Elemento non supportato: {op.get('type')!r} ({op.get('id')})")

    explicit: dict[str, set[int]] = {rid: set() for rid in registers}
    used: set[str] = set()
    for op in gates:
        kind = str(op.get("gate_type", "")).lower().replace("-", "_")
        if kind not in SUPPORTED:
            raise CircuitIssue(f"Porta non supportata: {kind} ({op.get('id')})")
        for field in ("input_registers", "controlled_by"):
            for token in tokenize(op.get(field, "")):
                rid, indexes = reference(token)
                if rid not in registers:
                    raise CircuitIssue(f"Registro {rid!r} non dichiarato")
                used.add(rid)
                if indexes is not None:
                    explicit[rid].update(indexes)

    rail_map: dict[str, dict[int, int]] = {}
    notes: list[str] = []
    for rid in registers:
        if rid not in used:
            continue
        reg = registers[rid]
        names = [x.strip() for x in str(reg.get("rail_names", "")).split(",") if x.strip()]
        symbol_indexes = {i for i, label in enumerate(names) if label in {"...", "…", "\\ldots", "\\cdots"}}
        symbolic = bool(symbol_indexes)
        if symbolic:
            if not explicit[rid]:
                raise CircuitIssue(
                    f"Registro simbolico {rid} senza qubit indirizzati esplicitamente: "
                    "non posso dedurre quanti qubit usare"
                )
            bad = explicit[rid] & symbol_indexes
            if bad:
                raise CircuitIssue(f"Porta indirizzata al simbolo '...' su {rid}{sorted(bad)}")
            if max(explicit[rid]) >= len(names):
                raise CircuitIssue(f"Indice fuori dalle etichette del registro {rid}")
            physical = sorted(explicit[rid])
            notes.append(f"{rid}: rail simbolici {physical} -> {list(range(len(physical)))} nel simulatore; '...' omesso")
        else:
            count = reg.get("size")
            count = count if isinstance(count, int) and count > 0 else (len(names) if names else 1)
            count = max(count, max(explicit[rid], default=-1) + 1)
            physical = list(range(count))
        rail_map[rid] = {old: new for new, old in enumerate(physical)}

    def resolve(spec: str) -> list[tuple[str, int]]:
        expanded = []
        for token in tokenize(spec):
            rid, indexes = reference(token)
            if rid not in rail_map:
                raise CircuitIssue(f"Registro {rid} senza qubit simulabili")
            if indexes is None:
                indexes = list(rail_map[rid])
            for old in indexes:
                if old not in rail_map[rid]:
                    raise CircuitIssue(f"Rail {rid}[{old}] non rappresentabile nel simulatore")
                expanded.append((rid, rail_map[rid][old]))
        return expanded

    steps = []
    for op in gates:
        kind = str(op["gate_type"]).lower().replace("-", "_")
        targets = resolve(op.get("input_registers", ""))
        controls = resolve(op.get("controlled_by", ""))
        if not targets or len(set(targets)) != len(targets):
            raise CircuitIssue(f"Bersagli assenti o duplicati per {op.get('id')}")
        if len(controls) > 1 or (controls and controls[0] in targets):
            raise CircuitIssue(f"Controllo non supportato per {op.get('id')}")
        if kind == "cnot" and (len(targets) != 1 or len(controls) != 1):
            raise CircuitIssue("CNOT richiede un bersaglio e un controllo")
        if kind not in ("cnot", "x", "pauli_x", "not") and controls:
            raise CircuitIssue(f"Controllo su porta {kind!r} non ancora supportato")
        steps.append((op.get("id", "?"), kind, targets, controls))
    return data.get("title", path.stem), rail_map, steps, notes


def simulate(path: Path, inspect: bool = False):
    title, rail_map, steps, notes = parse_circuit(path)
    total = sum(len(m) for m in rail_map.values())
    if total > 16:
        raise CircuitIssue("Troppi qubit per questo esempio (>16)")
    print("\n" + "=" * 65)
    print("Circuito:", title)
    print("Registri:", ", ".join(f"{rid}={len(m)} qubit" for rid, m in rail_map.items()))
    for note in notes:
        print("ATTENZIONE:", note)
    for ident, kind, targets, controls in steps:
        print(f"- {ident}: {kind}  target={targets}  control={controls}")
    print("=" * 65)

    if inspect:
        print("Analisi del file completata; simulazione non eseguita (--inspect).")
        return

    from psiqdk.workbench import QPU, Qubits
    qpu = QPU(num_qubits=total)
    regs = {rid: Qubits(len(rail_map[rid]), rid, qpu=qpu) for rid in rail_map}
    for _ident, kind, targets, controls in steps:
        for rid, idx in targets:
            qb = regs[rid][idx]
            if kind in ("hadamard", "h"):
                qb.had()
            elif kind in ("x", "pauli_x", "not", "cnot"):
                if controls:
                    crid, cidx = controls[0]
                    qb.x(cond=regs[crid][cidx])
                else:
                    qb.x()
            elif kind in ("pauli_z", "z"):
                qb.z()
    print("\n=== STATO FINALE ===")
    qpu.print_state_vector()
    print("\n=== PROBABILITÀ DI MISURAZIONE ===")
    qpu.print_probabilities()


def main():
    parser = argparse.ArgumentParser(description="Osserva un file .circuit e simula le porte con PsiQDK Workbench")
    parser.add_argument("file", help="Percorso o pattern *.circuit (racchiudere fra virgolette)")
    parser.add_argument("--once", action="store_true", help="Simula una volta e termina")
    parser.add_argument("--inspect", action="store_true", help="Controlla solo la conversione, senza PsiQDK")
    args = parser.parse_args()
    file_spec = str(Path(args.file).expanduser())
    print(f"Osservo: {file_spec}", flush=True)
    if not args.once:
        print("Salva in Circuit Designer per aggiornare il file; Ctrl+C per uscire.", flush=True)
    last_signature = None
    while True:
        try:
            if glob.has_magic(file_spec):
                candidates = [Path(p) for p in glob.glob(file_spec) if Path(p).is_file()]
                if not candidates:
                    raise FileNotFoundError(file_spec)
                path = max(candidates, key=lambda p: (p.stat().st_mtime_ns, p.name))
            else:
                path = Path(file_spec).resolve()
            stat = path.stat()
            signature = (str(path), stat.st_mtime_ns, stat.st_size)
            if signature != last_signature:
                last_signature = signature
                print(f"\n[File aggiornato] {path.name}", flush=True)
                try:
                    simulate(path, inspect=args.inspect)
                except (CircuitIssue, ValueError, json.JSONDecodeError) as exc:
                    print(f"Errore nella definizione del circuito: {exc}", file=sys.stderr, flush=True)
                    if args.once:
                        raise SystemExit(1)
                except Exception as exc:
                    print(f"Errore durante simulazione: {exc}", file=sys.stderr, flush=True)
                    if args.once:
                        raise SystemExit(1)
            if args.once:
                break
            time.sleep(1)
        except FileNotFoundError:
            if args.once:
                raise SystemExit(f"File non trovato: {file_spec}")
            print(f"In attesa del file corrispondente a {file_spec} ...", flush=True)
            time.sleep(2)
        except KeyboardInterrupt:
            print("\nMonitoraggio terminato.")
            break


if __name__ == "__main__":
    main()
