# Quantum Computing — Construct + PsiQuantum Workbench

Guida operativa del progetto `quantum-computing`.

Questo repository contiene un circuito **Bell State Pairs** creato con **PsiQuantum Construct Circuit Designer** e un piccolo programma Python (`construct_workbench_bridge.py`) che legge il file `.circuit` e ne simula le operazioni supportate con **PsiQDK Workbench**.

> **Flusso effettivo:** modifica in Circuit Designer → salva/esporta il file `.circuit` → aggiorna il file nel progetto → esegui la simulazione da PyCharm/WSL. **Non** esiste, in questa configurazione, una sincronizzazione istantanea del browser con Workbench. Il bridge è un componente didattico del progetto, **non** un importatore ufficiale PsiQuantum.

Per la spiegazione delle formule, delle porte, dei risultati e della tecnologia fotonica, consulta [README_FISICA_E_TECNOLOGIA.md](README_FISICA_E_TECNOLOGIA.md).

## 1. Stato del progetto e ambiente verificato

| Componente | Configurazione usata |
|---|---|
| PC / IDE | Windows + PyCharm |
| Esecuzione Python | Ubuntu 26.04 LTS su WSL2 |
| Progetto Linux | `/home/lucat/projects/quantum-computing` |
| Python del progetto | `.venv/bin/python` — 3.12.16 |
| Gestione Python / venv | `uv` |
| PsiQDK | 2.5.0 |
| PsiQDK Workbench | 4.55.3 |
| File sorgente grafico | `bell_pairs.circuit` |
| Script di conversione | `construct_workbench_bridge.py` |
| Branch Git principale | `main` |

### File principali

```text
quantum-computing/
├── .gitignore
├── .venv/                           # Ambiente locale; escluso da Git
├── 01_hadamard.py                   # Esercizio separato: singolo qubit
├── bell_pairs.circuit               # Sorgente grafico salvato da Construct
├── construct_workbench_bridge.py   # Interprete didattico .circuit → Workbench
├── README.md                        # Questa guida operativa
└── README_FISICA_E_TECNOLOGIA.md   # Fisica, tecnologia e risultati
```

## 2. Ruolo dei componenti

1. **Circuit Designer**: si disegnano registri e porte; serve anche a gestire Routine, etichette LaTeX e stile del diagramma. Non è il motore che ha prodotto le probabilità.
2. **File `.circuit`**: è un documento JSON che conserva la struttura del diagramma. Nel nostro caso i nodi sono in `root.children`; le porte sono annidate nella Routine `Bell Pairs`.
3. **`construct_workbench_bridge.py`**: legge il JSON, attraversa la Routine, interpreta le porte supportate e crea un modello equivalente con le API Python di Workbench.
4. **PsiQDK Workbench**: esegue **una simulazione ideale dello stato quantistico** e stampa ampiezze e probabilità. Non invia il circuito a un computer quantistico fisico.
5. **PyCharm**: è l'editor. Poiché l'interprete è Linux e l'IDE gira su Windows, il metodo già funzionante è eseguire i comandi nel terminale WSL.

## 3. Preparazione dell'ambiente (solo su un nuovo PC o ambiente)

Per il progetto attuale questi passaggi sono **già stati completati**. Servono come promemoria per riprodurre la configurazione.

Da PowerShell si entra in Ubuntu con:

```powershell
wsl -d Ubuntu
```

Da Ubuntu, installato `uv` (vedere la [documentazione di uv](https://docs.astral.sh/uv/getting-started/installation/)):

```bash
cd ~/projects/quantum-computing
~/.local/bin/uv python install 3.12
~/.local/bin/uv venv --python 3.12 .venv
~/.local/bin/uv pip install --python .venv/bin/python psiqdk
```

Verifiche:

```bash
.venv/bin/python --version
.venv/bin/psiqdk
```

Nell'ambiente usato durante l'esercizio sono state verificate **Python 3.12.16**, **PsiQDK 2.5.0**, **Workbench 4.55.3** e la dicitura `All dependencies satisfied`.

> Non cambiare il `python3` di sistema per questo progetto e non aggiungere `.venv/` al repository Git.

## 4. Modificare il circuito in Construct

Aprire [Circuit Designer](https://construct.psiquantum.com/cd) e caricare/aprire `bell_pairs.circuit` se necessario. La versione realizzata contiene:

- due registri, `r1` etichettato `|a⟩` e `r3` etichettato `|b⟩`;
- il registro `r2`, presente nel JSON ma non impiegato nella simulazione;
- la Routine grafica **Bell Pairs** (di colore viola);
- una porta **Hadamard** applicata al registro `r1`;
- tre porte **CNOT**: `r1[0] → r3[0]`, `r1[1] → r3[1]`, `r1[3] → r3[3]`;
- un'etichetta LaTeX con lo stato finale simbolico.

**Salvataggio**

1. Eseguire la modifica desiderata nel browser.
2. Utilizzare **File → Save** oppure **Save As**, ottenendo la versione aggiornata del file `.circuit` sul computer. Può essere richiesto il login a Circuit Designer.
3. Fare in modo che **il file aggiornato sostituisca** `bell_pairs.circuit` nella cartella del progetto WSL; un file rimasto nella cartella Download non viene letto automaticamente dallo script.

Se il browser ha salvato il file nella cartella Download di Windows, da Ubuntu si può copiarlo così (adattare il nome se Chrome ha aggiunto un suffisso):

```bash
cd ~/projects/quantum-computing
cp /mnt/c/Users/lucat/Downloads/bell_pairs.circuit ./bell_pairs.circuit
```

In alternativa, da Esplora file di Windows si raggiunge la cartella Linux attraverso:

```text
\\wsl$\Ubuntu\home\lucat\projects\quantum-computing
```

Non usare **Download as SVG** al posto del `.circuit`: l'SVG è un'immagine, non contiene il documento strutturato che il bridge deve leggere.

## 5. Controllare il circuito prima di eseguirlo

Dal terminale Ubuntu integrato in PyCharm oppure da un normale terminale WSL:

```bash
cd ~/projects/quantum-computing
.venv/bin/python construct_workbench_bridge.py bell_pairs.circuit --once --inspect
```

L'opzione `--inspect` **non simula**: analizza il file e mostra le operazioni riconosciute. Per il nostro documento attuale ci aspettiamo:

```text
Circuito: Bell State Pairs
Registri: r1=3 qubit, r3=3 qubit
- gate1: hadamard  target=[('r1', 0), ('r1', 1), ('r1', 2)]  control=[]
- gate2: cnot  target=[('r3', 0)]  control=[('r1', 0)]
- gate3: cnot  target=[('r3', 1)]  control=[('r1', 1)]
- gate4: cnot  target=[('r3', 2)]  control=[('r1', 2)]
Analisi del file completata; simulazione non eseguita (--inspect).
```

Le righe complete possono includere anche avvisi sui rail simbolici e delimitatori.

## 6. Simulare in Workbench

Eseguire il comando **che abbiamo verificato sul progetto reale**:

```bash
.venv/bin/python construct_workbench_bridge.py bell_pairs.circuit --once
```

Il flag `--once` esegue un caricamento e una simulazione, poi termina. **È la modalità consigliata**: non occorre lasciare un processo in ascolto.

Output essenziale ottenuto nell'esperimento:

```text
=== STATO FINALE ===
|r1|r3>
|0|0>    0.353553+0.000000j
|1|1>    0.353553+0.000000j
|2|2>    0.353553+0.000000j
|3|3>    0.353553+0.000000j
|4|4>    0.353553+0.000000j
|5|5>    0.353553+0.000000j
|6|6>    0.353553+0.000000j
|7|7>    0.353553+0.000000j

=== PROBABILITÀ DI MISURAZIONE ===
|r1|r3>
|0|0>    0.125000
|1|1>    0.125000
|2|2>    0.125000
|3|3>    0.125000
|4|4>    0.125000
|5|5>    0.125000
|6|6>    0.125000
|7|7>    0.125000
```

**Significato sintetico:** lo stato finale consente otto risultati in cui i due registri coincidono; ogni esito ha probabilità 12,5%. `|7|7>` indica i due registri al valore **7 = `111` in binario**, non un qubit singolo di valore 7. La spiegazione completa è nell'altro README.

### Esecuzione da PyCharm

Il progetto è aperto in PyCharm tramite il percorso WSL. Se l'IDE non ha un interprete WSL configurato, **non selezionare un interprete Windows** per queste librerie: eseguire dal terminale WSL.

È stato verificato anche questo comando esplicito, utilizzabile quando serve invocare WSL da Windows:

```powershell
wsl.exe -d Ubuntu --cd /home/lucat/projects/quantum-computing -- .venv/bin/python construct_workbench_bridge.py bell_pairs.circuit --once
```

Può essere richiamato da una configurazione di lancio esterna o *Shell Script* di PyCharm, purché la configurazione lo esegua **in ambiente Windows** con `wsl.exe` disponibile. Non è una configurazione Python nativa dell'IDE.

## 7. Cambiare il circuito e ripetere la simulazione

Il ciclo quotidiano consigliato è breve:

1. **Modifica il diagramma** in Construct.
2. **Salva** il nuovo `.circuit` e aggiorna il file nel progetto WSL.
3. **Esegui una sola volta** il bridge con `--once`.
4. **Confronta** il nuovo elenco di porte, le ampiezze e le probabilità.
5. **Salva le modifiche su Git** quando il risultato è verificato.

Per esempio, una porta X aggiunta in Construct può cambiare lo stato finale; la Routine viola, la sua etichetta e il colore non cambiano invece la fisica simulata.

### Limiti precisi del bridge attuale

Il file `construct_workbench_bridge.py` **non** è un compilatore generale di circuiti Construct.

- Riconosce **Hadamard/H**, **Pauli-X/X/NOT**, **Pauli-Z/Z** e **CNOT** con un singolo controllo positivo.
- Attraversa le Routine, ma ignora gli elementi puramente grafici (etichette, colori, gruppi, separatori) ai fini delle operazioni quantistiche.
- Non gestisce tutte le porte che Circuit Designer consente di disegnare, né controlli negativi o multi-controllo generici: in quei casi segnala un errore invece di inventare una simulazione.
- Nel nostro diagramma i registri sono indicati come `1,2,...,n`. I rail esplicitamente utilizzati sono `[0]`, `[1]` e `[3]`. Il bridge **comprime** `[0,1,3] → [0,1,2]`, ignora il segnaposto grafico `...` e simula **tre qubit per registro, sei in totale**.
- La formula LaTeX del documento resta simbolica con `n`, ma **non** impone un numero arbitrario di qubit alla simulazione.
- Il bridge usa `print_state_vector()` e `print_probabilities()`: **non misura/collassa** i registri e **non esegue su hardware fisico**.
- Se si esegue il programma **senza `--once`**, entra in modalità di controllo periodico del file; questa modalità esiste nello script ma non è necessaria né consigliata per l'uso attuale.

## 8. Errori comuni e soluzioni rapide

| Sintomo | Controllo |
|---|---|
| `Nessuna porta nel circuito` | Verificare di usare la versione del bridge che legge `root.children` e attraversa le Routine; non sostituire automaticamente il diagramma. |
| `File non trovato` | Controllare directory corrente e nome esatto; il file deve essere `bell_pairs.circuit` nel progetto. |
| Le modifiche grafiche non cambiano il risultato | È normale per colore, etichetta e Routine; le porte fisiche devono cambiare. |
| La modifica in Construct non appare in Workbench | Il `.circuit` scaricato non ha ancora sostituito quello in WSL. |
| `No Python interpreter configured` in PyCharm | Usare il terminale Ubuntu/WSL e `.venv/bin/python`, non l'interprete Windows. |
| `ModuleNotFoundError: psiqdk` | Verificare di lanciare l'ambiente `.venv` e che `psiqdk` risulti installato. |
| Porta non supportata | Il bridge ha una lista volutamente ristretta; va esteso e testato prima di fidarsi di nuove operazioni. |

## 9. Versionare le modifiche con Git

Il repository è già stato inizializzato localmente. Dopo la creazione di questi README e dopo le future modifiche:

```bash
cd ~/projects/quantum-computing
git status
git add README.md README_FISICA_E_TECNOLOGIA.md
git commit -m "docs: guide Construct Workbench e analisi fisica"
git push
```

Se il push non è stato ancora autenticato, configurare l'accesso a GitHub separatamente; non inserire una password Google nel prompt HTTPS di Git.

## 10. Riferimenti ufficiali

- [PsiQuantum Construct — documentazione](https://docs.construct.psiquantum.com/)
- [Circuit Designer — Getting Started](https://docs.construct.psiquantum.com/circuit-designer/getting_started.html)
- [Il formato `.circuit`](https://docs.construct.psiquantum.com/circuit-designer/resources/circuits_filetype.html)
- [Circuit Designer — File Menu](https://docs.construct.psiquantum.com/circuit-designer/features/file.html)
- [Workbench — Getting Started](https://docs.construct.psiquantum.com/psiqdk-workbench/Getting-Started.html)
- [Workbench — simulazione dello state vector](https://docs.construct.psiquantum.com/psiqdk-workbench/howtos/Run-Statevector-Simulation.html)

---

**Documento aggiornato:** 22 novembre 2026. Basato sul file `bell_pairs.circuit`, sullo script `construct_workbench_bridge.py` e sull'output Workbench verificato durante l'esercizio.
