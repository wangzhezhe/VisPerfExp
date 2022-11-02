#!/bin/bash
rm -rf ./IntransitVarySeedsNum_data

mkdir IntransitVarySeedsNum_data
cd IntransitVarySeedsNum_data

# soft link for the cloverleaf
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par
# soft link for the reader
ln -s ../../../../install/visReader/reader reader


# generate config file
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/ascent_actions_relay_adios_SST.yaml ascent_actions.yaml
sed -i "s/endstep: 10/endstep: 200/" ascent_actions.yaml
# if we use the cloverleaf_in the end step is 600 

# this is for fides writer
cp ${scriptsDir}/adios2.xml adios2.xml
# this is for the fides write operation
cp ${scriptsDir}/cloverleaf.json cloverleaf.json

#NUM_SEEDS_LIST="512 1024 2048 4096"
NUM_SEEDS_LIST="1000"
#MESH_SIZE_LIST="51"

for NUM_SEEDS in ${NUM_SEEDS_LIST}
do
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
mpirun -n 2 ./reader \
--file=out.bp \
--read-method=SST \
--visualization-op=advect \
--seed-method=box \
--advect-seed-box-extents=1.5,2.5,1.5,2.5,0,8.0 \
--advect-num-seeds=${NUM_SEEDS} \
--advect-num-steps=1000 \
--record-trajectories=false \
--advect-step-size=0.1 \
--field-name=velocity \
--sst-json-file=./cloverleaf.json &> ./reader.log &

echo "start reader, prepar sim"
# start the sim to get the data
# sed -i "s/64/${MESH_SIZE}/" clover.in

echo "start sim, executing"
mpirun -n 10 ./cloverleaf3d_par &> ./sim.log

mv sim.log sim.log.${NUM_SEEDS}
mv timing.vis.0.out timing.vis.0.${NUM_SEEDS}.out
mv reader.log reader.log.${NUM_SEEDS}
echo "ok for ${NUM_SEEDS}"
done

#TODO, wait the reader to finish and exit the reader
#Maybe write a file disk to indicate the reader finish

for MESH_SIZE in ${MESH_SIZE_LIST}
do
echo "check adios filter time in sim.log.${MESH_SIZE}"
cat sim.log.${MESH_SIZE} |grep "ascent_execution_time" | cut -d " " -f 8
echo "check in transit processing time in timing.vis.0.${MESH_SIZE}.out"
cat timing.vis.0.${MESH_SIZE}.out |grep "render" | cut -d " " -f 4
done

