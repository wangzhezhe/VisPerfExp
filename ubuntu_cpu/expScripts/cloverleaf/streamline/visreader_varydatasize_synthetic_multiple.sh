#!/bin/bash

rm -rf ./visreader_varydatasize_synthetic_multiple_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir visreader_varydatasize_synthetic_multiple_data
cd visreader_varydatasize_synthetic_multiple_data
ln -s ../../../../install/visReader/visitReaderAdev visitReaderAdev

# for synthetic data
DATADIR=/home/zw/dataset/synthetic
DATANAME_LIST="fb_syn_symm_multiple_100_100_100.2_2_2.16_16_16.visit fb_syn_symm_multiple_100_100_100.2_2_2.32_32_32.visit fb_syn_symm_multiple_100_100_100.2_2_2.64_64_64.visit fb_syn_symm_multiple_100_100_100.2_2_2.128_128_128.visit fb_syn_symm_multiple_100_100_100.2_2_2.256_256_256.visit"
#DATANAME_LIST="fb_syn_symm_multiple_100_100_100.2_2_2.16_16_16.visit"

for DATANAME in ${DATANAME_LIST}
do

DATASET=$DATADIR/$DATANAME

mpirun -n 8 ./visitReaderAdev \
--file=$DATASET \
--field-name=velocity \
--advect-seed-box-extents=0,10,0,10,0,10 \
--advect-num-steps=1000 \
--advect-num-seeds=100 \
--advect-step-size=0.1 \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf &> reader.log

# draw figure
python3  ~/cworkspace/VisPerfExp/commonScripts/parse/parse_timetrace_multisteps.py 8 1 . &> ana.log

# copy results into the specific dir
logdir=log_${DATANAME}
mkdir -p ${logdir}
mv reader.log ${logdir}
mv ana.log ${logdir}
mv *.png ${logdir}
mv timetrace.* ${logdir}
mv counter.* ${logdir}

done

