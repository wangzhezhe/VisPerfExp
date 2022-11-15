#!/bin/bash

rm -rf ./visitReaderAdev_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir visitReaderAdev_data
cd visitReaderAdev_data
ln -s ../../../../install/visReader/visitReaderAdev visitReaderAdev

DATASET=/home/zw/dataset/cloverleaf/x_clover_650.2_2_2.visit

./visitReaderAdev \
--file=$DATASET \
--field-name=velocity \
--advect-seed-box-extents=1.5,2.5,1.5,2.5,0.1,7.9 \
--advect-num-steps=1000 \
--advect-num-seeds=1000 \
--advect-step-size=0.1 \
--record-trajectories=true \
--output-results=true \
--sim-code=cloverleaf


