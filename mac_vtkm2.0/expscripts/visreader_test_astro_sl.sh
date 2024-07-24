#!/bin/bash

# rm -rf ./visreader_test_astro_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir -p visreader_test_astro_data_sl

cd visreader_test_astro_data_sl

#python3 ../../../frontier_vktm2.0_cpu/data_placement/generate_assignment_rrb.py 8 4

ln -s ../../install/visReader/visitReaderAdev visitReaderAdev
ln -s ../../install/visReader/workloadEstimation/StreamlineMPI2 StreamlineMPI2


# for cloverleaf data
DATADIR=/Users/zhewang/DataSets
DATANAME="astro.2_2_2.visit"
DATASET=${DATADIR}/$DATANAME

PARTICLE_LIST="1000"
STEP_LIST="1000"

STEPSIZE_ASTRO=0.005000
MAXSTEPS=2000
NUM_SIM_POINTS_PER_DOM=1000
NUM_TEST_POINTS=50
NXYZ=4

# the mpirun will oversubscribe the omp threads
# if we do not set the OMP_NUM_THREADS
# try to set it explicitly
export OMP_NUM_THREADS=1

for STEP in ${STEP_LIST}
do
for PARTICLE in ${PARTICLE_LIST}
do

# executing sl filter to get results
mpirun -n 8 --bind-to none -x OMP_NUM_THREADS=1 ./StreamlineMPI2 \
$DATASET \
velocity \
$STEPSIZE_ASTRO \
$MAXSTEPS \
$NUM_TEST_POINTS \
$NUM_SIM_POINTS_PER_DOM \
$NXYZ &> sl2_estimate.log

done
done


