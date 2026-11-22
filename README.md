# Quantum Computing — IBM Quantum Composer + Qiskit

Guida operativa del repository `quantum-computing`. Ultimo aggiornamento: **22 novembre 2026**.

Il progetto esplora gli **stati di Bell** usando circuiti progettati graficamente con [IBM Quantum Composer](https://quantum.cloud.ibm.com/composer), salvati come **OpenQASM 3** ed eseguiti in Python tramite **Qiskit** e il simulatore locale **Qiskit Aer**.

**Stato verificato:** simulazione ideale e campionamento locale di un circuito a **2 qubit / 1 coppia** e di un circuito a **4 qubit / 2 coppie**. **Non abbiamo ancora inviato lavori a un processore quantistico IBM fisico.**

Per matematica, interpretazione dei risultati e tecnologia dei qubit superconduttori, vedere [README_FISICA_E_TECNOLOGIA.md](README_FISICA_E_TECNOLOGIA.md).

## 1. Obiettivo e flusso di lavoro

```text
IBM Quantum Composer (editor grafico / codice OpenQASM 3)
          │  File → Salva file
          ▼
       circuito.qasm
          │  Copia nella directory del progetto WSL, se necessario
          ▼
PyCharm (editor) + terminale Ubuntu WSL2
          │
          ▼
python simulate_qasm.py circuito.qasm
          │
          ├── Qiskit: importa il circuito e calcola le probabilità ideali
          └── Qiskit Aer: campiona 1.024 misurazioni simulate
```

**Un'unica sorgente per il circuito:** il `.qasm` esportato da Composer. Lo script `simulate_qasm.py` **non contiene porte H o CNOT specifiche**: le importa dal file. Se il circuito grafico cambia, si salva di nuovo il `.qasm` e si riesegue **lo stesso programma**.

**Limite importante:** Composer **non sincronizza automaticamente** i salvataggi con PyCharm. Il file va esportato/salvato e, se necessario, copiato nel progetto. Non è previsto un processo che controlli continuamente il filesystem.

## 2. Ambiente usato

| Componente | Configurazione |
|---|---|
| IDE | PyCharm su Windows |
| Sistema di esecuzione | Ubuntu 26.04 LTS su WSL2 |
| Directory Linux | `/home/lucat/projects/quantum-computing` |
| Python nel progetto | `.venv/bin/python`, versione 3.12.16 |
| Gestione interprete e dipendenze | `uv` |
| Librerie | `qiskit`, `qiskit-aer`, `qiskit-qasm3-import` |
| Aer verificato | 0.18.4 |
| Versionamento | Git, branch `main` |

Il progetto è aperto in PyCharm attraverso `\\wsl$\Ubuntu\home\lucat\projects\quantum-computing`. Se l'IDE non offre un interprete WSL configurabile, il metodo **già collaudato** è eseguire i comandi dal terminale Ubuntu: non selezionare per errore un Python Windows.

### File del progetto

```text
quantum-computing/
├── .gitignore
├── .venv/                         # Ambiente virtuale locale, NON versionare
├── bell_pair_2q.qasm              # Sorgente Composer: 1 coppia di Bell
├── bell_pairs_4q.qasm             # Sorgente Composer: 2 coppie di Bell
├── simulate_qasm.py               # Importatore + simulazione di qualsiasi circuito supportato
├── bell_pairs_4q.py               # Esercizio Python equivalente, costruito esplicitamente
├── README.md                      # Guida operativa
└── README_FISICA_E_TECNOLOGIA.md # Teoria e risultati
```

`bell_pairs_4q.py` resta un esercizio utile, ma il flusso **preferito** è `*.qasm → simulate_qasm.py`, così le modifiche eseguite in Composer sono la sorgente del calcolo.

## 3. Preparazione dell'ambiente (solo per una nuova installazione)

Da Windows, avviare Ubuntu con `wsl -d Ubuntu`. Nel terminale Ubuntu:

```bash
cd ~/projects/quantum-computing

# Solo se manca l'ambiente virtuale
~/.local/bin/uv python install 3.12
~/.local/bin/uv venv --python 3.12 .venv

# Dipendenze Python per gli esperimenti correnti
~/.local/bin/uv pip install --python .venv/bin/python \
    qiskit qiskit-aer qiskit-qasm3-import

# Verifica
.venv/bin/python -c "import qiskit, qiskit_aer; print('Qiskit:', qiskit.__version__, 'Aer:', qiskit_aer.__version__)"
```

Per il progetto attuale le librerie sono **già state installate**: non serve ripetere la preparazione. Non modificare Python di sistema e non caricare `.venv/` su Git.

## 4. Costruire e salvare i circuiti in IBM Composer

Aprire [IBM Quantum Composer](https://quantum.cloud.ibm.com/composer). È possibile creare o modificare il circuito sia trascinando le porte nell'interfaccia sia scrivendo **OpenQASM 3** nel pannello a destra. Il grafico e il codice restano allineati **all'interno di Composer**.

### Esperimento A — 2 qubit, una coppia di Bell

Sorgente di `bell_pair_2q.qasm`:

```qasm
OPENQASM 3.0;
include "stdgates.inc";

qubit a;
qubit b;

h a;
cx a, b;
```

- `h a`: Hadamard su `a`, inizializzato a `|0⟩`.
- `cx a, b`: CNOT con `a` come controllo e `b` come bersaglio.
- Il pannello **Probabilità** di Composer mostra `00` e `11` con probabilità del **50%** ciascuno.

### Esperimento B — 4 qubit, due coppie di Bell

Sorgente di `bell_pairs_4q.qasm`:

```qasm
OPENQASM 3.0;
include "stdgates.inc";

qubit[2] a;
qubit[2] b;

h a[0];
cx a[0], b[0];

h a[1];
cx a[1], b[1];
```

- Qubit: `a[0]`, `a[1]`, `b[0]`, `b[1]`.
- Due Hadamard e due CNOT: preparazione indipendente delle coppie `(a[0], b[0])` e `(a[1], b[1])`.
- Probabilità ideali: `0000`, `0101`, `1010`, `1111` **25%** ciascuno.

**Salvataggio:** in Composer scegliere **Salva file** (o **File → Salva file**), assegnando i nomi sopra. Si salva il sorgente `.qasm`, non soltanto una figura `.png` o `.svg`. Per riaprire un circuito usare **File → Upload .qasm file**. Il pannello *Sfera Q* non è una misura fisica: visualizza ampiezze/fasi del modello.

## 5. Portare il `.qasm` nel progetto WSL

Se il browser ha scaricato i file in `C:\Users\lucat\Downloads`, da Ubuntu:

```bash
cd ~/projects/quantum-computing
cp /mnt/c/Users/lucat/Downloads/bell_pair_2q.qasm .
cp /mnt/c/Users/lucat/Downloads/bell_pairs_4q.qasm .
```

Se i file sono già nella directory del progetto, non occorre copiarli. In caso di omonimia verificare che il file locale contenga davvero **quattro** qubit prima di eseguire il secondo esperimento; il nome `4q` da solo non garantisce che la struttura sia corretta.

## 6. Simulare il circuito esportato: `simulate_qasm.py`

La versione verificata dello script applica questo procedimento:

```python
import sys
from qiskit import qasm3
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

file_qasm = sys.argv[1]
circuit = qasm3.load(file_qasm)

print("=== CIRCUITO IMPORTATO DA COMPOSER ===")
print(circuit.draw(output="text"))

state = Statevector.from_instruction(circuit)
print("\n=== PROBABILITÀ TEORICHE ===")
for bits, probability in sorted(state.probabilities_dict().items()):
    if probability > 1e-10:
        print(f"|{bits}> = {probability * 100:.2f}%")

measured = circuit.copy()
measured.measure_all()
result = AerSimulator().run(measured, shots=1024).result()

print("\n=== 1024 MISURAZIONI SIMULATE ===")
for bits, count in sorted(result.get_counts().items()):
    print(f"|{bits}> = {count}")
```

**Ambito dello script:** i due file attuali non contengono misurazioni: lo script le aggiunge **soltanto a una copia**, per il campionamento. Non è ancora un esecutore generale di qualunque OpenQASM 3 (ad esempio, misure intermedie, reset, istruzioni classiche o cicli richiederebbero una gestione più specifica). Non invia nulla a IBM Cloud.

### Esecuzioni verificate

```bash
cd ~/projects/quantum-computing
.venv/bin/python simulate_qasm.py bell_pair_2q.qasm
.venv/bin/python simulate_qasm.py bell_pairs_4q.qasm
```

| Esperimento | Esiti teorici | Misurazioni Aer effettivamente ottenute (1.024 shots) |
|---|---|---|
| 2 qubit | `00`, `11`: 50% ciascuno | `00`: **510**, `11`: **514** |
| 4 qubit | `0000`, `0101`, `1010`, `1111`: 25% ciascuno | `0000`: **267**, `0101`: **272**, `1010`: **244**, `1111`: **241** |

I numeri sono **un campione simulato**, non conteggi su hardware fisico. Rieseguendo lo script i conteggi possono cambiare; le probabilità teoriche no. La spiegazione è nel [README scientifico](README_FISICA_E_TECNOLOGIA.md).

## 7. Regola pratica per modificare un circuito

1. Aprire il file `.qasm` in **Composer** e apportare la modifica visuale o testuale.
2. Salvare nuovamente il sorgente `.qasm`.
3. Aggiornare la copia nella directory Ubuntu, se è stata scaricata altrove.
4. Rieseguire `.venv/bin/python simulate_qasm.py nome_file.qasm`.
5. Confrontare **porte importate**, **probabilità esatte** e **conteggi simulati**.
6. Versionare su Git i file sorgente e la documentazione verificata.

Nessuna modifica a `simulate_qasm.py` è necessaria per il semplice passaggio da una a due coppie di Bell.

## 8. Problemi riscontrabili

| Sintomo | Cosa verificare |
|---|---|
| PyCharm segnala `*.qasm` come testo semplice | Non impedisce l'esecuzione: è una questione di associazione file/syntax highlighting. |
| `No Python interpreter configured` | Eseguire dal terminale **WSL**, usando `.venv/bin/python`. |
| `ModuleNotFoundError: qiskit_qasm3_import` | Installare `qiskit-qasm3-import` nello stesso `.venv`. |
| Risultati a 2 qubit lanciando `bell_pairs_4q.qasm` | Il file non è stato aggiornato dopo l'esportazione: controllare il contenuto del `.qasm`. |
| Dati diversi tra Composer e script | Controllare che il `.qasm` locale sia l'ultima versione salvata e che non contenga misure aggiuntive. |
| Campionamenti con conteggi diversi | È normale: 1.024 *shots* sono un campione pseudo-casuale della distribuzione ideale. |

## 9. Git e documentazione

```bash
cd ~/projects/quantum-computing
git status
git add README.md README_FISICA_E_TECNOLOGIA.md \
    bell_pair_2q.qasm bell_pairs_4q.qasm \
    bell_pairs_4q.py simulate_qasm.py
git commit -m "docs: documentati Composer Qiskit e risultati Bell a 2 e 4 qubit"
git push
```

Non aggiungere API key, token di accesso cloud, credenziali o l'ambiente `.venv/` a Git.

## 10. Prossima fase (NON ancora eseguita): processore quantistico IBM reale

La prossima sessione servirà a eseguire **lo stesso circuito** su un processore IBM fisico, senza confondere i risultati del simulatore con quelli sperimentali. Piano di lavoro:

1. Accedere a **IBM Quantum Platform** e verificare disponibilità, piano e istanza abilitata.
2. Installare nel progetto il client IBM richiesto dalla versione corrente delle API (`qiskit-ibm-runtime`, o client indicato dalle istruzioni ufficiali aggiornate).
3. Configurare l'autenticazione **senza salvare segreti nel repository**.
4. Caricare il `.qasm`, aggiungere misure finali e **traspilare** per un backend QPU specifico, rispettandone le porte native e la connettività.
5. Eseguire il job e recuperare i conteggi, l'identificativo del job e il backend utilizzato.
6. Confrontare le frequenze sperimentali con quelle teoriche e simulate, discutendo errori di gate, misura e decoerenza.

**Non è stata effettuata alcuna sottomissione hardware né creato uno script operativo di invio.** La procedura esatta verrà definita con le API e con l'account effettivamente disponibili al momento dell'esecuzione.

## 11. Riferimenti ufficiali

- [IBM Quantum Composer](https://quantum.cloud.ibm.com/composer)
- [Guida a Composer](https://quantum.cloud.ibm.com/docs/en/guides/composer)
- [OpenQASM 3 e Qiskit](https://quantum.cloud.ibm.com/docs/en/guides/interoperate-qiskit-qasm3)
- [API Qiskit `qasm3`](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qasm3)
- [Traspilazione per hardware IBM](https://quantum.cloud.ibm.com/docs/en/qiskit/transpile)
- [IBM Quantum Platform](https://quantum.cloud.ibm.com/)

---

*Documento aggiornato il 22 novembre 2026. Risultati numerici trascritti dalle esecuzioni effettuate nel progetto; procedure hardware indicate solo come attività futura.*
