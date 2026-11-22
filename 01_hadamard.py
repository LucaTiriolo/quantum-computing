
from psiqdk.workbench import QPU, Qubits

# Creiamo un simulatore quantistico con un qubit
qpu = QPU(num_qubits=1)

# Allochiamo un qubit, inizialmente nello stato |0>
qubit = Qubits(1, "q", qpu=qpu)

print("=== STATO INIZIALE ===")
qpu.print_state_vector()

# Applichiamo la porta Hadamard
qubit[0].had()

print("\n=== DOPO HADAMARD ===")
qpu.print_state_vector()

print("\n=== PROBABILITA ===")
qpu.print_probabilities()

# Applichiamo Hadamard una seconda volta
qubit[0].had()

print("\n=== DOPO LA SECONDA HADAMARD ===")
qpu.print_state_vector()

print("\n=== PROBABILITA FINALI ===")
qpu.print_probabilities()

# Misuriamo il qubit
risultato = qubit.read()
print("\nRisultato della misurazione:", risultato)
