#!/bin/bash

rm -rf ./visreader_execute_all_plans_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir visreader_execute_all_plans_data
cd visreader_execute_all_plans_data
ln -s ../../../../install/visReader/visitReaderAdev visitReaderAdev


# for cloverleaf data
DATADIR=/home/zw/dataset/cloverleaf
DATANAME="fb_clover_128_128_256.650.2_2_2.128_128_256.visit"
DATASET=${DATADIR}/$DATANAME

PARTICLE_LIST="1000"
STEP_LIST="1000"

# plans dir
PLANSDIR=/home/zw/cworkspace/VisPerfExp/ubuntu_cpu/expScripts/cloverleaf/streamline/visitReaderAdev_data/assignment

# the mpirun will oversubscribe the omp threads
# if we do not set the OMP_NUM_THREADS
# try to set it explicitly
export OMP_NUM_THREADS=1

for STEP in ${STEP_LIST}
do
for PARTICLE in ${PARTICLE_LIST}
do
# go through each plan
for PLANFILE in "$PLANSDIR"/*
do

echo "check plan file ${PLANFILE}"

# cover the existing plan file
# remember to set the assign strategy option

cp $PLANFILE assign_options.config

# execute tasks
mpirun -n 4 --bind-to none -x OMP_NUM_THREADS=1 ./visitReaderAdev \
--file=$DATASET \
--field-name=velocity \
--advect-seed-box-extents=0,4,0,4,0,8 \
--seeding-method=boxsample \
--seeding-sample=10,10,20 \
--advect-num-steps=${STEP} \
--advect-num-seeds=${PARTICLE} \
--advect-step-size=0.1 \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=file &> reader.log

# filter out key results
cat reader.log |grep "step 1 rank 0 adev go time"
cat reader.log |grep "1, VISapp_0_4, advect(particleadev)"

# draw figure
# python3  ~/cworkspace/VisPerfExp/commonScripts/parse/parse_timetrace_multisteps.py 8 1 . &> ana.log

# copy results into the specific dir
# logdir=log_${STEP}_${PARTICLE}
# mkdir -p ${logdir}
# mv reader.log ${logdir}
# mv ana.log ${logdir}
# mv *.png ${logdir}
# mv timetrace.* ${logdir}
# mv counter.* ${logdir}
# mv *vtk ${logdir}

done
done
done

