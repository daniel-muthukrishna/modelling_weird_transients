#!/bin/sh
export OMP_NUM_THREADS=2
mpirun -npernode 20 synapps DES16X3bdj_VLT_20160924.yaml

