#!/bin/bash

rm -rf ./visreader_varydatasize_clover_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir visreader_varydatasize_clover_data
cd visreader_varydatasize_clover_data
ln -s ../../../../install/visReader/visitReaderAdev visitReaderAdev


# for cloverleaf data
DATADIR=/home/zw/dataset/cloverleaf
#DATANAME_LIST="fb_clover_128_128_256.650.2_2_2.16_16_32.visit fb_clover_128_128_256.650.2_2_2.32_32_64.visit fb_clover_128_128_256.650.2_2_2.64_64_128.visit fb_clover_128_128_256.650.2_2_2.128_128_256.visit"
#DATANAME_LIST="fb_syn_symm_100_100_100.2_2_2.16_16_16.visit"

DATANAME_LIST="fb_clover_128_128_256.650.1_1_1.16_16_32.visit fb_clover_128_128_256.650.1_1_1.32_32_64.visit fb_clover_128_128_256.650.1_1_1.64_64_128.visit fb_clover_128_128_256.650.1_1_1.128_128_256.visit fb_clover_128_128_256.650.1_1_1.256_256_512.visit"


for DATANAME in ${DATANAME_LIST}
do

DATASET=${DATADIR}/$DATANAME

mpirun -n 2 ./visitReaderAdev \
--file=$DATASET \
--field-name=velocity \
--advect-seed-box-extents=0,4,0,4,0,8 \
--advect-num-steps=1000 \
--advect-num-seeds=1000 \
--advect-step-size=0.1 \
--record-trajectories=true \
--output-results=true \
--sim-code=cloverleaf &> reader.log

# draw figure
python3  ~/cworkspace/VisPerfExp/commonScripts/parse/parse_timetrace_multisteps.py 2 1 . &> ana.log

# copy results into the specific dir
logdir=log_${DATANAME}
mkdir -p ${logdir}
mv reader.log ${logdir}
mv ana.log ${logdir}
mv *.png ${logdir}
mv timetrace.* ${logdir}
mv counter.* ${logdir}
mv *vtk ${logdir}

done

