# Bell Pairs — Fisica, tecnologia superconduttrice e interpretazione dei risultati

**Progetto `quantum-computing` · IBM Quantum Composer + Qiskit · 22 novembre 2026**

Questa guida spiega in termini fisici, matematici e tecnologici due esperimenti **effettivamente simulati**: una coppia di Bell con **2 qubit** e due coppie di Bell indipendenti con **4 qubit**. Distingue le **probabilità teoriche** dai **1.024 campioni del simulatore Aer** e dall'esecuzione su un **processore quantistico reale, ancora da effettuare**.

Per creazione, esportazione, comandi PyCharm/WSL e Git, vedere [README.md](README.md).

## 1. Che cosa abbiamo costruito

Due circuiti in **IBM Quantum Composer**, salvati come OpenQASM 3 ed eseguiti in Python con Qiskit:

**Esperimento A: una coppia di Bell (2 qubit)**

```text
a: |0⟩ ──H──●──
             │
b: |0⟩ ─────X──
```

**Esperimento B: due coppie di Bell (4 qubit)**

```text
a[0]: |0⟩ ──H──●────────
                 │
a[1]: |0⟩ ──H──┼──●─────
                 │  │
b[0]: |0⟩ ─────X──┼─────
                    │
b[1]: |0⟩ ─────────X────
```

La `X` collegata al pallino è una **CNOT** (porta X controllata). Le coppie sono `(a[0], b[0])` e `(a[1], b[1])`. I circuiti sono **logici/ideali**: la loro rappresentazione non coincide con un disegno di collegamenti elettrici interni a una QPU.

## 2. Qubit, vettori di stato e notazione di Dirac

Un **bit classico** vale 0 oppure 1. Lo stato puro di un **qubit** si rappresenta come

$$
|\psi\rangle=\alpha|0\rangle+\beta|1\rangle, \qquad
|\alpha|^2+|\beta|^2=1.
$$

- $|0\rangle$ e $|1\rangle$ sono **stati della base computazionale** (non due qubit distinti).
- $\alpha,\beta$ sono **ampiezze complesse**; possono avere fase.
- $|\alpha|^2$ e $|\beta|^2$ sono le **probabilità** di ottenere 0 e 1 con una misura in tale base (**regola di Born**).
- La scrittura $|\cdot\rangle$ è la notazione *ket* di Dirac.

Una sovrapposizione **coerente** non è semplicemente una moneta che ha già un valore nascosto. Le fasi delle ampiezze possono dare luogo a **interferenza**.

Gli stati base possono essere scritti come vettori:

$$
|0\rangle=\begin{pmatrix}1\\0\end{pmatrix},\qquad
|1\rangle=\begin{pmatrix}0\\1\end{pmatrix}.
$$

## 3. Hadamard: dalla certezza alla sovrapposizione

La porta **H** è la matrice unitaria

$$
H=\frac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
$$

Applicata allo stato iniziale:

$$
H|0\rangle=|+\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2}.
$$

Quindi si ottiene 0 oppure 1 con probabilità **50%** ciascuno, ma **senza effettuare ancora una misura**. Il fattore $1/\sqrt2$ garantisce la normalizzazione:

$$
\left|\frac{1}{\sqrt2}\right|^2+
\left|\frac{1}{\sqrt2}\right|^2=1.
$$

La Hadamard non è una porta che *sceglie* casualmente un bit: conserva la coerenza. Se applicata due volte senza misure intermedie, $H^2=I$ e il qubit ritorna allo stato iniziale.

## 4. CNOT: controllo quantistico e preparazione dello stato di Bell

Per due qubit in ordine `(controllo, bersaglio)`:

| Prima | Dopo la CNOT |
|---|---|
| $|00\rangle$ | $|00\rangle$ |
| $|01\rangle$ | $|01\rangle$ |
| $|10\rangle$ | $|11\rangle$ |
| $|11\rangle$ | $|10\rangle$ |

Quando il controllo è in sovrapposizione, la porta agisce **linearmente su entrambi i termini**:

$$
|00\rangle\xrightarrow{H\text{ sul primo qubit}}
\frac{|00\rangle+|10\rangle}{\sqrt2}
\xrightarrow{\mathrm{CNOT}}
\boxed{\frac{|00\rangle+|11\rangle}{\sqrt2}}.
$$

Lo stato finale è la coppia di Bell $|\Phi^+\rangle$. La CNOT non è una copia arbitraria di un qubit sconosciuto: il **teorema di non clonazione** lo vieta. Correlare coerentemente gli stati base è cosa diversa dal clonare uno stato generico.

## 5. Che cosa significa entanglement?

Uno stato puro di due qubit è **entangled** quando **non può essere scritto come prodotto di due stati puri individuali**. Per esempio

$$
|\Phi^+\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2}
$$

non è separabile. Misurando entrambi i qubit nella base computazionale otteniamo `00` oppure `11`, ma non `01` o `10` nel circuito ideale.

**Non tutte le sovrapposizioni sono entangled:**

$$
\frac{|00\rangle+|01\rangle}{\sqrt2}
=|0\rangle\otimes\frac{|0\rangle+|1\rangle}{\sqrt2}
$$

è un prodotto di stati individuali. Inoltre **la sola correlazione `00/11` in una base non dimostra sperimentalmente entanglement**: una miscela classica può avere le stesse probabilità. La coerenza si mette in evidenza confrontando misure in altre basi, oppure tramite protocolli specifici di verifica dell'entanglement.

I quattro stati di Bell standard sono

$$
|\Phi^\pm\rangle=\frac{|00\rangle\pm|11\rangle}{\sqrt2},\qquad
|\Psi^\pm\rangle=\frac{|01\rangle\pm|10\rangle}{\sqrt2}.
$$

## 6. Esperimento A — Risultati a 2 qubit

**File sorgente:** `bell_pair_2q.qasm`; **esecuzione:** `.venv/bin/python simulate_qasm.py bell_pair_2q.qasm`.

Stato teorico:

$$
|\psi_2\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2}.
$$

Le **ampiezze** dei due termini sono $1/\sqrt2\approx0.707107$. Le **probabilità** sono il modulo quadro, cioè $1/2=50\%$ ciascuna.

Output effettivamente ottenuto:

```text
=== PROBABILITÀ TEORICHE ===
|00> = 50.00%
|11> = 50.00%

=== 1024 MISURAZIONI SIMULATE ===
|00> = 510
|11> = 514
```

| Stato | Probabilità teorica | Conteggio simulato | Frequenza osservata |
|---|---:|---:|---:|
| `00` | 50% | 510 | 49,80% |
| `11` | 50% | 514 | 50,20% |

L'ideale è **512** misurazioni per stato *in media*, non in ogni esecuzione. La differenza di 2 dal valore atteso per ciascuno è una normale fluttuazione del campionamento.

## 7. Esperimento B — Risultati a 4 qubit

**File sorgente:** `bell_pairs_4q.qasm`; **esecuzione:** `.venv/bin/python simulate_qasm.py bell_pairs_4q.qasm`.

Prepariamo due copie indipendenti dello stato $|\Phi^+\rangle$ (una per ogni coppia). La loro composizione si descrive con il **prodotto tensoriale**:

$$
|\psi_4\rangle=|\Phi^+\rangle_{a_0b_0}
\otimes|\Phi^+\rangle_{a_1b_1}.
$$

Espandendo, nella convenzione di ordine dei bit utilizzata dalla stampa di Qiskit:

$$
\boxed{|\psi_4\rangle=\frac{1}{2}
\big(|0000\rangle+|0101\rangle+|1010\rangle+|1111\rangle\big)}.
$$

Esistono $2^4=16$ stati della base computazionale, **ma soltanto quattro hanno ampiezza diversa da zero nel nostro stato**. Ciascuno ha ampiezza $0.5$ e probabilità $|0.5|^2=0.25=25\%$. Le altre 12 combinazioni hanno probabilità teorica nulla.

### Ordine dei qubit in Qiskit

Il codice definisce i qubit nell'ordine `a[0], a[1], b[0], b[1]`. Le stringhe di Qiskit vengono visualizzate, in genere, dall'indice più alto al più basso:

```text
  b[1] b[0] a[1] a[0]
```

Per questo `0101` significa **`a[1]a[0]=01` e `b[1]b[0]=01`**: entrambi i registri restituiscono lo stesso valore. Analogamente `1010` indica `10` per entrambi i registri.

### Risultati effettivamente ottenuti

```text
=== PROBABILITÀ TEORICHE ===
|0000> = 25.00%
|0101> = 25.00%
|1010> = 25.00%
|1111> = 25.00%

=== 1024 MISURAZIONI SIMULATE ===
|0000> = 267
|0101> = 272
|1010> = 244
|1111> = 241
```

| Stato | Probabilità teorica | Conteggio Aer | Frequenza simulata |
|---|---:|---:|---:|
| `0000` | 25% | 267 | 26,07% |
| `0101` | 25% | 272 | 26,56% |
| `1010` | 25% | 244 | 23,83% |
| `1111` | 25% | 241 | 23,54% |
| **Totale** | **100%** | **1.024** | **100%** |

Il conteggio teorico **medio** per ciascuno dei quattro stati è $1024\cdot0.25=256$. Le differenze osservate ($+11,+16,-12,-15$) sono compatibili con le fluttuazioni del campionamento. Questi numeri **non sono prove di errori fisici o rumore di una QPU**: sono generati dal simulatore ideale Aer.

### Perché due coppie danno quattro risultati e non sedici?

Ogni coppia di Bell produce solo `00` oppure `11` nella base computazionale, con probabilità 1/2. Le due coppie sono indipendenti **tra loro**:

$$
2\times2=4\ \text{esiti},\qquad
P(\text{ciascun esito})=\frac12\cdot\frac12=\frac14.
$$

Quattro qubit consentono **16 stati base**, ma il circuito specifico che abbiamo costruito ne popola soltanto quattro. In generale, il numero di qubit e il numero di esiti con probabilità non nulla **non sono la stessa cosa**.

## 8. Statevector, probabilità e shots: tre cose distinte

1. **Statevector**: vettore di ampiezze complesse; per 4 qubit ha **16 componenti**, una per ogni stato base. Soltanto quattro componenti del nostro vettore sono 0.5; le restanti sono zero.
2. **Probabilità ideali**: moduli quadri delle ampiezze, calcolati esattamente (entro la precisione numerica) con `Statevector.from_instruction()`.
3. **Shots simulati**: il programma aggiunge misure a una **copia** del circuito e con `AerSimulator().run(..., shots=1024)` campiona 1.024 esiti dalla distribuzione. I conteggi oscillano tra esecuzioni.

**Misura**: in un singolo esperimento, il risultato è uno degli stati base possibili. La misurazione non è semplicemente una stampa del vettore: a seconda del modello e del protocollo di misura aggiorna lo stato condizionato all'esito. Lo script attuale **non stampa lo stato successivo a una singola misura**.

## 9. Fisica reale IBM: che cosa implementa i qubit?

IBM Quantum utilizza **qubit superconduttori di tipo transmon**. Non si tratta di normali bit in una CPU né di un simulatore di elettricità classica. Un transmon è un **circuito quantistico superconduttore**, che include una **giunzione Josephson** e capacità elettrica; si scelgono due livelli energetici del dispositivo come $|0\rangle$ e $|1\rangle$.

### 9.1 Perché serve la refrigerazione?

I chip superconduttori lavorano a temperature criogeniche estremamente basse, ottenute con sistemi di refrigerazione a diluizione. Questo aiuta a mantenere il regime superconduttivo e a ridurre le eccitazioni termiche indesiderate. Una QPU comprende quindi molta più infrastruttura dei quattro qubit mostrati nel disegno logico.

### 9.2 Come si implementano H e CNOT?

- Una porta a **singolo qubit** è ottenuta tramite controlli coerenti, per esempio impulsi a microonde calibrati, che provocano rotazioni dello stato quantistico. La `H` del linguaggio Qiskit può venire **decomposta** in una sequenza di operazioni supportate dall'hardware.
- Una porta **a due qubit** richiede un'interazione controllata tra dispositivi. Anche la `cx` del codice può essere decomposta in altre porte native del backend.
- L'insieme delle porte consentite e quali qubit possano interagire direttamente dipendono dal processore selezionato. Il **transpiler** mappa i qubit logici sui qubit fisici, traduce le porte e aggiunge, ove necessario, operazioni per rispettare la connettività.

Il diagramma `H → CNOT` descrive quindi **quali trasformazioni vogliamo ottenere**, non la sequenza esatta di impulsi generati dai controlli elettrici.

### 9.3 Dove entra l'elettronica?

L'hardware richiede sistemi elettronici classici di controllo e acquisizione:

- generazione, modulazione e temporizzazione degli **impulsi a microonde**;
- segnali di controllo e calibrazione delle operazioni sui qubit;
- **risonatori di lettura** accoppiati ai qubit e misure con segnali a microonde;
- amplificazione, acquisizione e digitalizzazione dei segnali di misura;
- elaborazione classica, gestione dell'esperimento e lettura dei risultati;
- apparati criogenici e interfacce elettriche fra temperature differenti.

Questa strumentazione serve alla realizzazione fisica delle operazioni, ma **non viene riprodotta nel dettaglio** dal calcolo `Statevector` o dal campionamento Aer ideale.

## 10. Cosa cambierà quando useremo una QPU IBM reale?

Sarà un **nuovo esperimento**, non ancora effettuato. Prima di inviare il job dovremo accedere all'account IBM Quantum, scegliere una QPU effettivamente disponibile, traspilare il circuito per quel dispositivo e inviarlo con misure. Dovremo registrare almeno: nome del backend, data/ora, numero di shots, identificativo job, circuito traspilato, distribuzione misurata e indicatori di errore/calibrazione disponibili.

Su hardware reale potremo osservare risultati non ideali, anche **stati non previsti** dal modello perfetto, a causa per esempio di errori delle porte, rilassamento, perdita di coerenza e imperfezioni della lettura. I valori saranno confrontati con il 50%/50% dei due qubit e con il 25% per ciascuno dei quattro esiti nel circuito a quattro qubit; non bisogna attribuire automaticamente ogni scostamento al rumore quantistico, poiché esiste anche la variabilità statistica di un campione finito.

### Cosa dimostriamo oggi — e cosa no

**Già verificato in simulazione:**

- la traduzione **Composer → OpenQASM 3 → Qiskit** funziona per entrambi i circuiti;
- una coppia genera `00/11` al 50% ideale; due coppie generano quattro stati al 25%;
- la simulazione Aer a 1.024 shots restituisce frequenze vicine alle previsioni.

**Non ancora verificato sperimentalmente:**

- creazione o misura dello stato su un **processore IBM reale**;
- tassi effettivi di errore o decoerenza del dispositivo scelto;
- violazione di disuguaglianze di Bell o altre misure indipendenti della coerenza;
- scalabilità e correzione degli errori per circuiti più grandi.

## 11. Glossario

| Termine | Significato |
|---|---|
| **Qubit** | Unità di informazione quantistica descritta da ampiezze complesse. |
| **Ket $|\psi\rangle$** | Notazione di Dirac per uno stato. |
| **Ampiezza** | Coefficiente complesso di uno stato base. |
| **Regola di Born** | Il modulo quadro dell'ampiezza dà la probabilità di misura. |
| **Hadamard** | Trasformazione unitaria che crea o modifica sovrapposizioni. |
| **CNOT / CX** | Porta X controllata; può creare entanglement. |
| **Entanglement** | Non separabilità di uno stato quantistico composto. |
| **Prodotto tensoriale $\otimes$** | Composizione matematica degli stati di sottosistemi. |
| **Statevector** | Vettore di tutte le ampiezze per gli stati base. |
| **Shot** | Una ripetizione di un circuito con misurazione. |
| **Qiskit Aer** | Simulatore eseguito su elaboratore classico. |
| **QPU** | Processore quantistico fisico. |
| **Transmon** | Tipo di qubit superconduttore basato su un circuito con giunzione Josephson. |
| **Transpiler** | Compilatore che adatta porte e collegamenti al backend fisico. |

## 12. Approfondimenti

- [IBM Quantum Learning — Running quantum circuits](https://quantum.cloud.ibm.com/learning/en/courses/quantum-computing-in-practice/running-quantum-circuits)
- [IBM Quantum Learning — Noise and errors](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/noise-and-errors)
- [IBM Quantum — Introduzione alla transpilation](https://quantum.cloud.ibm.com/docs/en/qiskit/transpile)
- [IBM Quantum Composer](https://quantum.cloud.ibm.com/composer)
- [IBM Quantum — Interoperabilità OpenQASM 3 / Qiskit](https://quantum.cloud.ibm.com/docs/en/guides/interoperate-qiskit-qasm3)

---

*Documento aggiornato il 22 novembre 2026. Gli output sono risultati realmente osservati nelle simulazioni locali, non misure hardware.*
