#!/bin/sh
export OMP_NUM_THREADS=2
mpirun -npernode 20 synapps sn2006jo.yaml

