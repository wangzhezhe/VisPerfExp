#!/bin/bash
rm -rf ./IntransitLoadBP_data

mkdir IntransitLoadBP_data
cd IntransitLoadBP_data

# soft link for the cloverleaf
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par
# soft link for the reader
ln -s ../../../../install/visReader/reader reader

# generate config file
scriptsDir=../../../../../commonScripts

# this is for fides writer
cp ${scriptsDir}/adios2_BP.xml adios2.xml
# this is for the fides write operation
cp ${scriptsDir}/cloverleaf.json cloverleaf.json

NUM_SEEDS=1000

echo "test the seeds number ${NUM_SEEDS}"
#cp ${scriptsDir}/clover.in_default clover.in
cp ${scriptsDir}/clover.in_jet clover.in
sed -i "s/end_step=600/end_step=600/" clover.in
#sed -i "s/64/256/" clover.in

# start the reader firstly
# issue, the reader does not exist as expected
#./reader --file=out.bp --read-method=SST --visualization-op=volume --sst-json-file=cloverleaf.json &> ./reader.log &

#mpirun -n 4 ./reader --file=out.bp --read-method=SST --visualization-op=advect --seed-method=box --advect-seed-box-extents=0,10,0,10,0,10 --advect-num-seeds=512 --field-name=velocity --sst-json-file=./cloverleaf.json &> ./reader.log &

# if use the jet configuration
BPDir=/home/zw/cworkspace/VisPerfExp/ubuntu_cpu/expScripts/cloverleaf/writeFile/varyDataSizeBP_data

mpirun -n 4 ./reader \
--read-method=BP4 \
--file=${BPDir}/output/out.bp \
--visualization-op=advect \
--seed-method=box \
--advect-seed-box-extents=1.5,2.5,1.5,2.5,0,8.0 \
--advect-num-seeds=${NUM_SEEDS} \
--advect-num-steps=1000 \
--record-trajectories=false \
--advect-step-size=0.1 \
--field-name=velocity \
--record-trajectories=false \
--sst-json-file=./cloverleaf.json 

echo "start reader, prepar sim"



