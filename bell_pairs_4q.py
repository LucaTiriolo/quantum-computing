
import sys

from qiskit import qasm3
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

# Il file .qasm viene passato da riga di comando
file_qasm = sys.argv[1]

# Carichiamo direttamente il circuito di Composer
circuit = qasm3.load(file_qasm)

print("=== CIRCUITO IMPORTATO ===")
print(circuit.draw(output="text"))

# Calcoliamo lo stato quantistico ideale
state = Statevector.from_instruction(circuit)

print("\n=== PROBABILITÀ TEORICHE ===")
for bits, p in sorted(state.probabilities_dict().items()):
    if p > 1e-10:
        print(f"|{bits}> = {p * 100:.2f}%")

# Aggiungiamo le misurazioni solo alla copia
measured = circuit.copy()
measured.measure_all()

simulator = AerSimulator()
result = simulator.run(measured, shots=1024).result()

print("\n=== MISURAZIONI SIMULATE ===")
for bits, count in sorted(result.get_counts().items()):
    print(f"|{bits}> = {count}")
