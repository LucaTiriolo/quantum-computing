
OPENQASM 3.0;
include "stdgates.inc";

// Due registri di 2 qubit
qubit[2] a;
qubit[2] b;

// Prima coppia entangled
h a[0];
cx a[0], b[0];

// Seconda coppia entangled
h a[1];
cx a[1], b[1];
