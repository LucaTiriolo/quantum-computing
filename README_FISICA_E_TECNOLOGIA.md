# Bell State Pairs — Fisica, tecnologia fotonica e interpretazione dei risultati

Questa guida spiega **che cosa abbiamo realmente simulato** nel progetto `quantum-computing`: il significato di qubit, sovrapposizione, porte Hadamard e CNOT, entanglement, normalizzazione, ampiezze e probabilità. Nell'ultima parte distingue il **modello logico del simulatore** dalla possibile **realizzazione fisica fotonica** e dai componenti elettronici che la controllano.

Per l'uso pratico di Circuit Designer, PyCharm, WSL e Workbench, vedere il [README operativo](README.md).

> **Avvertenza essenziale:** abbiamo simulato uno **stato quantistico ideale** sul computer classico tramite Workbench. Non abbiamo generato fotoni, misurato particelle in laboratorio o eseguito il circuito su un processore quantistico PsiQuantum.

## 1. Qual è l'esperimento?

Abbiamo progettato in Construct il diagramma **Bell State Pairs**:

- un registro `a` (`r1`) e un registro `b` (`r3`);
- una Hadamard su ciascuno dei qubit rappresentati del registro `a`;
- una CNOT fra ogni qubit `aᵢ` (controllo) e il corrispondente qubit `bᵢ` (bersaglio);
- una Routine grafica denominata **Bell Pairs**.

Il diagramma originale usa l'etichettatura simbolica `1, 2, ..., n`. Nel file JSON i controlli/bersagli delle tre CNOT sono `[0]`, `[1]` e `[3]`: il terzo rappresenta la linea grafica `n`. Il bridge realizzato per il progetto mappa questi indici sui tre qubit **effettivamente simulati** `[0]`, `[1]`, `[2]`.

In termini **logici** l'esperimento equivale a:

```text
Registro a       H ───────●──────────────────────────    a₀
                         │
Registro b       ─────────⊕──────────────────────────    b₀

Registro a       H ─────────────●────────────────────    a₁
                               │
Registro b       ───────────────⊕────────────────────    b₁

Registro a       H ───────────────────●──────────────    a₂
                                     │
Registro b       ─────────────────────⊕──────────────    b₂
```

Questo schema è illustrativo: ogni coppia ha la propria H e la propria CNOT, e le operazioni sulle coppie sono indipendenti. Il simulatore usa **sei qubit**, non sei *bit classici*.

## 2. Che cos'è un qubit?

Un **bit classico** assume un valore `0` oppure `1`. Un **qubit** è descritto da uno stato in uno spazio vettoriale complesso di dimensione due:

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle, \qquad |\alpha|^2 + |\beta|^2 = 1.
$$

Qui:

- $|0\rangle$ e $|1\rangle$ sono i due stati della **base computazionale**;
- $\alpha$ e $\beta$ sono **ampiezze di probabilità** e possono essere numeri complessi;
- la probabilità di ottenere `0` o `1` misurando in questa base è rispettivamente $|\alpha|^2$ e $|\beta|^2$;
- il simbolo $|\cdot\rangle$ è la **notazione di Dirac** (*ket*).

Un qubit in sovrapposizione non equivale semplicemente a un bit classico di valore già deciso ma sconosciuto: le **fasi relative** fra ampiezze hanno effetti verificabili attraverso l'interferenza.

## 3. Porta Hadamard: dalla certezza alla sovrapposizione

La porta **H** è l'operatore unitario:

$$
H=\frac{1}{\sqrt{2}}
\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
$$

Sul qubit iniziale $|0\rangle$ agisce così:

$$
H|0\rangle = \frac{|0\rangle+|1\rangle}{\sqrt{2}}
= |+\rangle.
$$

Di conseguenza, dopo una Hadamard ideale, le probabilità nella base computazionale sono:

$$
P(0)=\left|\frac{1}{\sqrt{2}}\right|^2=\frac12,
\qquad P(1)=\frac12.
$$

La Hadamard **non è una misura** e non assegna un valore casuale al qubit: trasforma coerentemente le ampiezze. Il segno meno nella seconda riga della matrice è essenziale per i fenomeni di interferenza. Per esempio, senza misure intermedie, $H(H|0\rangle)=|0\rangle$.

## 4. Porta CNOT: un controllo quantistico

La CNOT (*controlled NOT*) agisce su due qubit. Se il controllo vale `0`, non cambia il bersaglio; se vale `1`, inverte il bersaglio.

| Prima (controllo, bersaglio) | Dopo CNOT |
|---|---|
| $|00\rangle$ | $|00\rangle$ |
| $|01\rangle$ | $|01\rangle$ |
| $|10\rangle$ | $|11\rangle$ |
| $|11\rangle$ | $|10\rangle$ |

Se il controllo è in sovrapposizione, la CNOT agisce **linearmente su tutta la sovrapposizione**:

$$
\frac{|00\rangle+|10\rangle}{\sqrt{2}}
\xrightarrow{\mathrm{CNOT}}
\frac{|00\rangle+|11\rangle}{\sqrt{2}}.
$$

È così che prepariamo una **coppia di Bell** partendo da $|00\rangle$: prima H sul primo qubit, poi CNOT con quel qubit come controllo.

## 5. Cos'è una coppia di Bell e perché è entangled?

Lo stato preparato per una coppia è:

$$
|\Phi^+\rangle = \frac{|00\rangle+|11\rangle}{\sqrt2}.
$$

La parola **entanglement** indica che lo stato complessivo dei due qubit **non può essere scritto come il prodotto di due stati individuali puri**. Per una coppia di Bell, lo stato di ciascun qubit preso isolatamente non descrive tutte le proprietà della coppia.

Se misuriamo entrambi nella base computazionale, otteniamo:

- `00` con probabilità **50%**;
- `11` con probabilità **50%**;
- `01` e `10` con probabilità **0%** (modello ideale).

I risultati sono correlati, ma **la sola correlazione nella base computazionale non basta a dimostrare sperimentalmente l'entanglement**: anche alcune miscele classiche producono la stessa tabella di probabilità. Per distinguerle occorre osservare coerenza e correlazioni in altre basi (per esempio tramite misure appropriate o test di Bell).

È utile confrontare:

$$
\frac{|10\rangle+|00\rangle}{\sqrt2}
=\frac{|1\rangle+|0\rangle}{\sqrt2}\otimes|0\rangle
$$

che è **separabile**, con:

$$
\frac{|11\rangle+|00\rangle}{\sqrt2}=|\Phi^+\rangle,
$$

che è **entangled**. Esistono infiniti stati entangled; i quattro stati di Bell sono un insieme particolare di quattro stati massimamente entangled che formano una base ortonormale:

$$
|\Phi^{\pm}\rangle=\frac{|00\rangle\pm|11\rangle}{\sqrt2},
\qquad
|\Psi^{\pm}\rangle=\frac{|01\rangle\pm|10\rangle}{\sqrt2}.
$$

## 6. Dal circuito a tre coppie allo stato di sei qubit

Nel nostro caso partiamo da sei qubit inizializzati nello stato $|000\rangle_a|000\rangle_b$.

Applicando H ai tre qubit di $a$ otteniamo una sovrapposizione uniforme di tutti gli otto valori binari del registro $a$, mentre il registro $b$ è ancora a zero:

$$
|\psi_1\rangle=
\frac{1}{\sqrt8}\sum_{x=0}^{7}|x\rangle_a|000\rangle_b.
$$

Le tre CNOT copiano **i valori di base computazionale** dal controllo al bersaglio, ma agiscono in modo coerente: non eseguono una copia universale di uno stato quantistico sconosciuto (che è impossibile per il teorema di non-clonazione).

Il risultato finale è:

$$
\boxed{
|\Psi\rangle=
\frac{1}{\sqrt8}\sum_{x=0}^{7}|x\rangle_a|x\rangle_b
}
$$

ossia, per esteso:

$$
\begin{aligned}
|\Psi\rangle=\frac{1}{\sqrt8}(&|000\rangle_a|000\rangle_b
+|001\rangle_a|001\rangle_b\\
&+|010\rangle_a|010\rangle_b
+|011\rangle_a|011\rangle_b\\
&+|100\rangle_a|100\rangle_b
+|101\rangle_a|101\rangle_b\\
&+|110\rangle_a|110\rangle_b
+|111\rangle_a|111\rangle_b).
\end{aligned}
$$

La stessa preparazione si scrive come **prodotto tensoriale di tre coppie di Bell**:

$$
|\Psi\rangle = |\Phi^+\rangle_{a_0b_0}
\otimes|\Phi^+\rangle_{a_1b_1}
\otimes|\Phi^+\rangle_{a_2b_2}.
$$

Quindi abbiamo **tre coppie indipendenti**, ciascuna entangled al proprio interno. Questo non è lo stesso stato di uno stato GHZ a sei qubit.

## 7. Interpretazione esatta dell'output Workbench

Output osservato nell'esperimento:

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

### 7.1 Perché `0.353553`?

Ci sono **otto termini ortogonali equiprobabili**, e devono avere una probabilità totale pari a 1. Se ogni ampiezza è $c$:

$$
8|c|^2=1
\quad\Longrightarrow\quad
|c|=\frac1{\sqrt8}=\frac1{2\sqrt2}\approx0.353553.
$$

Il numero stampato dal simulatore è dunque una **ampiezza**, non una probabilità del 35,3553%.

La notazione Python `0.353553+0.000000j` significa che il coefficiente è complesso, ma in questo esperimento ha parte immaginaria nulla (`j^2=-1`). Le fasi restano importanti in generale, anche quando questi coefficienti risultano reali.

### 7.2 Perché `0.125000`?

Per la **regola di Born**, la probabilità è il modulo quadro dell'ampiezza:

$$
P(x,x)=\left|\frac1{\sqrt8}\right|^2
=\frac18=0.125=12.5\%.
$$

Le otto probabilità sommano a 1: $8\cdot0.125=1$. Tutti gli altri **56** possibili esiti di sei bit (`64−8`) hanno probabilità zero nel modello ideale e, per questo, non compaiono nell'output mostrato.

### 7.3 Perché `|7|7>` non significa che un qubit vale 7?

Workbench stampa i registri di **tre qubit** come interi decimali compresi tra 0 e 7. Gli stessi risultati in binario sono:

| Workbench | Registro `a` (3 bit) | Registro `b` (3 bit) | Probabilità |
|---|---|---|---:|
| `\|0\|0>` | `000` | `000` | 12,5% |
| `\|1\|1>` | `001` | `001` | 12,5% |
| `\|2\|2>` | `010` | `010` | 12,5% |
| `\|3\|3>` | `011` | `011` | 12,5% |
| `\|4\|4>` | `100` | `100` | 12,5% |
| `\|5\|5>` | `101` | `101` | 12,5% |
| `\|6\|6>` | `110` | `110` | 12,5% |
| `\|7\|7>` | `111` | `111` | 12,5% |

**In termini statistici**, il registro `a` ha distribuzione uniforme sugli otto valori, così come `b`, ma i due sono perfettamente correlati: nella base computazionale $P(a=b)=1$ e $P(a\ne b)=0$.

### 7.4 Si è verificato davvero un risultato casuale?

**No.** Il nostro script chiama:

```python
qpu.print_state_vector()
qpu.print_probabilities()
```

Queste istruzioni mostrano lo stato e le probabilità **senza eseguire una misurazione**. Non producono campioni casuali e non fanno collassare lo stato.

Se aggiungessimo una misurazione con `read()` e registrassimo molti tentativi, ogni coppia di valori uguali dovrebbe comparire **circa** nel 12,5% dei casi, con normali fluttuazioni statistiche. Ma **questa non è una prova eseguita** nel progetto attuale.

## 8. Perché H e CNOT non sono semplici porte digitali?

Il diagramma ricorda uno schema di logica digitale, ma **il significato fisico è diverso**.

| Logica elettronica classica | Circuito quantistico ideale |
|---|---|
| Bit 0/1 rappresentato da livelli logici o stati elettrici | Qubit descritto da ampiezze complesse |
| Una porta NOT cambia `0 ↔ 1` | Pauli-X scambia $|0\rangle$ e $|1\rangle$ e agisce linearmente sulle sovrapposizioni |
| Una porta logica classica opera sui valori di bit | H manipola ampiezze e fasi; CNOT può generare entanglement |
| Un'uscita letta non richiede necessariamente il collasso dello stato | La misura quantistica produce un esito e modifica lo stato |
| Correlazioni ottenibili anche con bit classici | Le correlazioni quantistiche coerenti possono manifestarsi in più basi |

In particolare, **Hadamard non è una porta logica digitale standard** che “genera un bit casuale”: è una trasformazione unitaria reversibile. E la **CNOT** agisce coerentemente sui coefficienti della sovrapposizione.

## 9. Fisica fotonica: come si potrebbe rappresentare un qubit con la luce?

PsiQuantum sviluppa una piattaforma basata sulla **fotonica integrata in silicio**, non su un normale circuito di transistor che contiene questi sei qubit. La tecnologia combina componenti ottici per generare, guidare, manipolare e rilevare fotoni e componenti elettronici per il controllo e la lettura. [PsiQuantum — Quantum Computing](https://www.psiquantum.com/quantum-computing); [articolo su *Nature*](https://doi.org/10.1038/s41586-025-08820-7).

### 9.1 Codifica dual-rail (due modi ottici)

Un esempio importante è la codifica **dual-rail**: un qubit logico è rappresentato dalla presenza di un singolo fotone in **uno di due modi ottici** (per esempio due guide d'onda):

$$
|0\rangle_L\equiv|1,0\rangle_{\text{modi}},
\qquad
|1\rangle_L\equiv|0,1\rangle_{\text{modi}}.
$$

Qui il ket a due cifre sulla destra descrive **l'occupazione dei due modi** (uno/zero fotoni), **non** due qubit separati. Questo è diverso dalle linee orizzontali dei nostri registri in Circuit Designer: quelle linee rappresentano **qubit logici**, non necessariamente guide d'onda fisiche.

Una sovrapposizione del qubit può corrispondere, nel modello dual-rail, a una **sovrapposizione coerente dei due percorsi ottici** per il fotone.

### 9.2 Che cosa corrisponde alla Hadamard?

In una realizzazione ottica dual-rail, un **accoppiatore ottico bilanciato** (*beam splitter* / directional coupler) può mescolare coerentemente le ampiezze dei due modi. Insieme ad appropriate **fasi ottiche** può realizzare l'azione logica di H (a convenzioni di fase e segni vicino).

Il componente non “sceglie casualmente un percorso” durante l'evoluzione ideale: produce ampiezze coerenti che possono interferire successivamente.

### 9.3 E la CNOT fotonica?

La CNOT è un'operazione logica a due qubit. In ottica fotonica **non si ottiene semplicemente collegando due fili o accendendo un transistor**. Realizzare operazioni entangling richiede risorse ulteriori, interferenza a più fotoni, misure e/o schemi opportunamente progettati.

PsiQuantum studia un approccio **fusion-based quantum computing**, nel quale le **misure di fusione** e gli stati di risorsa entangled giocano un ruolo centrale nella computazione. Il nostro simbolo CNOT nel simulatore rappresenta quindi l'**effetto logico ideale**, non lo schema ottico esecutivo di un dispositivo CNOT deterministico. [PsiQuantum — Architecture](https://www.psiquantum.com/architecture).

### 9.4 Dove entra l'elettronica?

Anche quando l'informazione quantistica è codificata nella luce, l'apparato richiede elettronica e infrastruttura di controllo:

- **pilotaggio e stabilizzazione** delle sorgenti ottiche e dei circuiti integrati;
- **regolazione delle fasi** e comando degli switch/modulatori ottici, tramite attuatori e circuiti di controllo;
- **rivelazione** dei fotoni mediante opportuni sensori (anche superconducting single-photon detectors nelle piattaforme studiate);
- **acquisizione e processamento** dei segnali di rivelazione e **feed-forward**, cioè operazioni condizionate dai risultati precedenti;
- sincronizzazione, temporizzazione, interconnessioni, alimentazione e gestione termica.

Queste funzioni non sono simulate in dettaglio da `qpu.print_state_vector()`. Lo script esegue **algebra quantistica a livello logico**, non simulazione elettro-ottica di rumore, perdite di fotoni, ritardi o dissipazione.

> In un esempio **puramente ideale** dual-rail, sei qubit rappresentati con un fotone ciascuno richiederebbero dodici modi ottici. Questo **non** è un preventivo di fotoni, dispositivi o risorse hardware per l'architettura reale di PsiQuantum, che richiede ulteriori risorse e codifiche.

## 10. Che cosa dimostrano i risultati e che cosa no

**Dimostrano, all'interno del modello ideale usato, che:**

1. H crea una sovrapposizione uniforme dei tre qubit del registro di controllo.
2. Le CNOT preservano la coerenza e stabiliscono le tre correlazioni fra coppie corrispondenti.
3. Il vettore di stato risultante ha otto ampiezze non nulle, uguali a $1/\sqrt8$.
4. La distribuzione dei risultati della misura computazionale contiene solo coppie di registri uguali, con probabilità $1/8$ ciascuna.

**Non dimostrano ancora che:**

- un chip fisico abbia prodotto o misurato questo stato;
- le porte reali siano prive di errori, perdite e decoerenza;
- i valori 12,5% siano frequenze sperimentali già misurate;
- i rail grafici `1,2,...,n` siano stati espansi in un numero arbitrario di qubit;
- lo stesso schema sia automaticamente compilabile in risorse fotoniche fisiche.

## 11. Glossario essenziale

| Termine | Significato nel progetto |
|---|---|
| **Qubit** | Unità informativa quantistica, con stato in uno spazio complesso a due dimensioni. |
| **Ket** $|\psi\rangle$ | Notazione di Dirac per uno stato. |
| **Ampiezza** | Coefficiente complesso dello stato quantistico. |
| **Regola di Born** | La probabilità si ottiene dal modulo quadro dell'ampiezza. |
| **Sovrapposizione** | Combinazione coerente di stati di base. |
| **Fase relativa** | Differenza di fase fra ampiezze; influenza l'interferenza. |
| **Hadamard (H)** | Porta reversibile che trasforma stati di base in sovrapposizioni. |
| **CNOT** | Porta X controllata che può produrre entanglement. |
| **Stato di Bell** | Stato massimamente entangled di due qubit. |
| **Entanglement** | Non separabilità dello stato di più qubit in stati individuali puri. |
| **Prodotto tensoriale $\otimes$** | Composizione degli spazi/stati dei sottosistemi. |
| **Rail (Construct)** | Linea grafica riferita a un qubit o componente di registro nel diagramma. |
| **Dual-rail (fotonica)** | Codifica fisica di un qubit attraverso due modi ottici; uso distinto dal termine grafico `rail`. |
| **State vector** | Insieme delle ampiezze dello stato simulato. |
| **Measurement / `read()`** | Operazione che campiona un risultato e aggiorna lo stato simulato. |

## 12. Riferimenti e approfondimenti

**Documentazione software**

- [PsiQDK Workbench — Getting Started](https://docs.construct.psiquantum.com/psiqdk-workbench/Getting-Started.html)
- [PsiQDK Workbench — Basic Gates](https://docs.construct.psiquantum.com/psiqdk-workbench/new-tutorials/Basic-Gates.html)
- [PsiQDK Workbench — Measurements](https://docs.construct.psiquantum.com/psiqdk-workbench/new-tutorials/Measurements.html)
- [Statevector Simulation](https://docs.construct.psiquantum.com/psiqdk-workbench/howtos/Run-Statevector-Simulation.html)
- [What is a `.circuit` file?](https://docs.construct.psiquantum.com/circuit-designer/resources/circuits_filetype.html)

**Tecnologia e realizzazione fisica**

- [PsiQuantum — Quantum Computing](https://www.psiquantum.com/quantum-computing)
- [PsiQuantum — Quantum Architecture](https://www.psiquantum.com/architecture)
- [PsiQuantum et al., *A manufacturable platform for photonic quantum computing*, Nature 641 (2025)](https://doi.org/10.1038/s41586-025-08820-7)

---

**Documento aggiornato:** 22 novembre 2026. Parte matematica riferita al circuito e all'output realmente ottenuti; parte fotonica/elettronica fornita come spiegazione tecnologica generale, **non** come descrizione di un esperimento hardware condotto nel progetto.
