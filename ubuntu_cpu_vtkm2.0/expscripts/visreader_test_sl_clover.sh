#!/bin/bash

# rm -rf ./visreader_test_astro_data

# this one is used to test some details of the streamline
# for single data 

# create soft link
rm -rf ./visreader_test_sl_clover
mkdir -p visreader_test_sl_clover

cd visreader_test_sl_clover

ln -s ../../install/visReader/visitReaderAdev visitReaderAdev
ln -s ../../install/visReader/workloadEstimation/StreamlineMPI2 StreamlineMPI2


# for cloverleaf data
DATADIR=/home/ubuntu/dataset
DATANAME="fb_cv_0.2_2_2.128_128_128.visit"
DATASET=${DATADIR}/$DATANAME

PARTICLE_LIST="1000"
STEP_LIST="1000"

STEPSIZE_ASTRO=0.005
MAXSTEPS=2000
NUM_SIM_POINTS_PER_DOM=1000
NUM_TEST_POINTS=30
NXYZ=2
WIDTH_PCT=0.1

echo "NUM_TEST_POINTS:"$NUM_TEST_POINTS
echo "NXYZ:"$NXYZ
echo "WIDTH_PCT:"$WIDTH_PCT

# Step 1 run with one block per rank
NUM_NODE=1
# the total blocks should same with the total number of ranks
NUM_RANK=8
NUM_BLOCKS=8

# the mpirun will oversubscribe the omp threads
# if we do not set the OMP_NUM_THREADS
# try to set it explicitly
export OMP_NUM_THREADS=1

for STEP in ${STEP_LIST}
do
for PARTICLE in ${PARTICLE_LIST}
do

# executing sl filter to get results
#mpirun -n 2 --bind-to none -x OMP_NUM_THREADS=1 ./StreamlineMPI2 \
#mpirun -n 2 --bind-to none ./StreamlineMPI2 \
mpirun -np 8 --bind-to none -x OMP_NUM_THREADS=1 ./StreamlineMPI2 \
$DATASET \
mesh_mesh/velocity \
$STEPSIZE_ASTRO \
$MAXSTEPS \
$NUM_TEST_POINTS \
$NUM_SIM_POINTS_PER_DOM \
$NXYZ \
true 

#&> sl2_estimate.log

done
done


