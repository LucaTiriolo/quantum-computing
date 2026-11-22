
import sys

from qiskit import qasm3
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

# Caricamento del circuito esportato da IBM Composer
file_qasm = sys.argv[1]
circuit = qasm3.load(file_qasm)

print("=== CIRCUITO IMPORTATO DA COMPOSER ===")
print(circuit.draw(output="text"))

# Calcolo delle probabilità ideali
state = Statevector.from_instruction(circuit)

print("\n=== PROBABILITÀ TEORICHE ===")
for bits, probability in sorted(state.probabilities_dict().items()):
    if probability > 1e-10:
        print(f"|{bits}> = {probability * 100:.2f}%")

# Simulazione delle misurazioni
measured = circuit.copy()
measured.measure_all()

simulator = AerSimulator()
result = simulator.run(measured, shots=1024).result()

print("\n=== 1024 MISURAZIONI SIMULATE ===")
for bits, count in sorted(result.get_counts().items()):
    print(f"|{bits}> = {count}")
