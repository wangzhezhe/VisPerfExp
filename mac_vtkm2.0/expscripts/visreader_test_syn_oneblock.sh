#!/bin/bash

# rm -rf ./visreader_test_astro_data

# this one is used to test some details of the streamline
# for single data 

# create soft link
mkdir -p visreader_test_syn_oneblock

cd visreader_test_syn_oneblock

#python3 ../../../frontier_vktm2.0_cpu/data_placement/generate_assignment_rrb.py 8 4

ln -s ../../install/visReader/visitReaderAdev visitReaderAdev
ln -s ../../install/visReader/workloadEstimation/StreamlineMPI2 StreamlineMPI2


# for cloverleaf data
DATADIR=/Users/zhewang/DataSets/DataSetForParticleAdvectionBlockAssignment/syn_one
DATANAME="syn.one.visit"
DATASET=${DATADIR}/$DATANAME

PARTICLE_LIST="1000"
STEP_LIST="1000"

STEPSIZE_SYN=0.0001
MAXSTEPS=2000
NUM_SIM_POINTS_PER_DOM=1000
NUM_TEST_POINTS=50
NXYZ=2

# the mpirun will oversubscribe the omp threads
# if we do not set the OMP_NUM_THREADS
# try to set it explicitly
export OMP_NUM_THREADS=1

for STEP in ${STEP_LIST}
do
for PARTICLE in ${PARTICLE_LIST}
do

# executing sl filter to get results
# mpirun -n 1 --bind-to none -x OMP_NUM_THREADS=1 ./StreamlineMPI2 \
mpirun -n 1 --bind-to none ./StreamlineMPI2 \
$DATASET \
velocity \
$STEPSIZE_SYN \
$MAXSTEPS \
$NUM_TEST_POINTS \
$NUM_SIM_POINTS_PER_DOM \
$NXYZ &> sl2_estimate.log

done
done


