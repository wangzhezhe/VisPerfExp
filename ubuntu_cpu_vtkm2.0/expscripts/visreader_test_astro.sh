#!/bin/bash

rm -rf ./visreader_test_astro_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir visreader_test_astro_data
cd visreader_test_astro_data
ln -s ../../install/visReader/visitReaderAdev visitReaderAdev

# for cloverleaf data
DATADIR=/home/zw/dataset/astro
DATANAME="astro.2_2_2.visit"
DATASET=${DATADIR}/$DATANAME

PARTICLE_LIST="1000"
STEP_LIST="500"

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
--vtkm-device openmp \
--file=$DATASET \
--field-name=velocity \
--advect-seed-box-extents=.01,.99,0.01,.99,0.01,.99 \
--seeding-method=domainrandom \
--advect-num-seeds=10 \
--advect-num-steps=${STEP} \
--advect-step-size=0.01 \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--communication=sync \
--trace_particle_id=10 \
--output-seeds=true \

done
done


