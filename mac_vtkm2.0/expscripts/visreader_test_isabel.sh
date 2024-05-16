#!/bin/bash

# rm -rf ./visreader_test_astro_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir -p visreader_test_isabel_data

cd visreader_test_isabel_data

#python3 ../../../frontier_vktm2.0_cpu/data_placement/generate_assignment_rrb.py 8 4

ln -s ../../install/visReader/visitReaderAdev visitReaderAdev

# for cloverleaf data
DATADIR=/Users/zw1/Documents/Datasets/IsabelData/IsabelCycle1to10
DATANAME="fb_cycle_01_replaced.2_2_2.128_128_64.visit"
DATASET=${DATADIR}/$DATANAME

PARTICLE_LIST="1000"
STEP_LIST="2000"

# the mpirun will oversubscribe the omp threads
# if we do not set the OMP_NUM_THREADS
# try to set it explicitly
export OMP_NUM_THREADS=1

for STEP in ${STEP_LIST}
do
for PARTICLE in ${PARTICLE_LIST}
do

# cover the existing plan file
# remember to set the assign strategy option

# try to not use the serial backend
# there are seg fault in arrayhandle copy some time

# execute tasks
mpirun -n 8 --bind-to none -x OMP_NUM_THREADS=1 ./visitReaderAdev \
--file=$DATASET \
--field-name=Velocity \
--advect-seed-box-extents=.01,499.0,0.01,499.0,0.01,99.0 \
--seeding-method=domainrandom \
--advect-num-seeds=$PARTICLE \
--advect-num-steps=${STEP} \
--advect-step-size=0.1 \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--output-seeds=false \
--assign-strategy=roundroubin \
--block-manual-id=false \
--communication=async_probe
done
done


