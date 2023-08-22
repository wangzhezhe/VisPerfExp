#!/bin/bash

rm -rf ./visreader_test_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir visreader_test_synthetic_data
cd visreader_test_synthetic_data
ln -s ../../install/visReader/visitReaderAdev visitReaderAdev

# for cloverleaf data
DATADIR=/home/zw/dataset/synthetic
DATANAME="fb_syn_symm_100_100_100.2_2_2.128_128_128.visit"
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
--vtkm-log-level Info \
--vtkm-device openmp \
--file=$DATASET \
--field-name=velocity \
--advect-seed-box-extents=0,99,0,99,0,99 \
--seeding-method=boxfixed \
--seeding-sample=20,20,20 \
--advect-num-steps=${STEP} \
--advect-step-size=0.1 \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--communication=sync

done
done


