#!/bin/bash

rm -rf ./visreader_varyworkload_seeding_clover_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir visreader_varyworkload_seeding_clover_data
cd visreader_varyworkload_seeding_clover_data
ln -s ../../../../install/visReader/visitReaderAdev visitReaderAdev


# for cloverleaf data
DATADIR=/home/zw/dataset/cloverleaf
DATANAME="fb_clover_128_128_256.650.2_2_2.128_128_256.visit"
DATASET=${DATADIR}/$DATANAME

PARTICLE_LIST="1600 3200 6400 12800 25600 51200 102400"
STEP_LIST="1000"

# the mpirun will oversubscribe the omp threads
# if we do not set the OMP_NUM_THREADS
# try to set it explicitly
export OMP_NUM_THREADS=1

for STEP in ${STEP_LIST}
do
for PARTICLE in ${PARTICLE_LIST}
do

mpirun -n 8 --bind-to none -x OMP_NUM_THREADS=1 ./visitReaderAdev \
--file=$DATASET \
--field-name=velocity \
--advect-seed-box-extents=1.5,2.5,1.5,2.5,3.0,5.0 \
--advect-num-steps=${STEP} \
--advect-num-seeds=${PARTICLE} \
--advect-step-size=0.1 \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf &> reader.log

# draw figure
python3  ~/cworkspace/VisPerfExp/commonScripts/parse/parse_timetrace_multisteps.py 8 1 . &> ana.log

# copy results into the specific dir
logdir=log_${STEP}_${PARTICLE}
mkdir -p ${logdir}
mv reader.log ${logdir}
mv ana.log ${logdir}
mv *.png ${logdir}
mv timetrace.* ${logdir}
mv counter.* ${logdir}
mv *vtk ${logdir}

done
done

