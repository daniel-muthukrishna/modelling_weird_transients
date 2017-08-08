#!/bin/sh
export OMP_NUM_THREADS=2
mpirun -npernode 18 synapps DES16X3bdj_AAT_20161125.yaml

