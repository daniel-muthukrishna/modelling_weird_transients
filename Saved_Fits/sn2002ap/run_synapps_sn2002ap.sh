#!/bin/sh
export OMP_NUM_THREADS=2
mpirun -npernode 22 synapps sn2002ap.yaml

