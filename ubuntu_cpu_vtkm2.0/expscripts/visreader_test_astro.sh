#!/bin/bash

rm -rf ./visreader_test_astro_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir visreader_test_astro_data

cp assign_options.config ./visreader_test_astro_data

cd visreader_test_astro_data
ln -s ../../install/visReader/visitReaderAdev visitReaderAdev


# for cloverleaf data
DATADIR=/home/zw/dataset/astro
DATANAME="astro.2_2_2.visit"
DATASET=${DATADIR}/$DATANAME

PARTICLE_LIST="5000"
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
--vtkm-device openmp \
--file=$DATASET \
--field-name=velocity \
--advect-seed-box-extents=.01,.99,0.01,.99,0.01,.99 \
--seeding-method=domainrandom \
--advect-num-seeds=$PARTICLE \
--advect-num-steps=${STEP} \
--advect-step-size=0.01 \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--communication=async_probe \
--trace_particle_id=32774 \
--output-seeds=false \
--num-recievers=64 \
--num-particles-per-packet=128 \
--block-duplicate=false \


done
done


