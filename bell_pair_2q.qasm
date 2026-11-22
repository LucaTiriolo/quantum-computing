
OPENQASM 3.0;
include "stdgates.inc";

// Due qubit: a e b
qubit a;
qubit b;

// Sovrapposizione del primo qubit
h a;

// Entanglement tra a e b
cx a, b;
