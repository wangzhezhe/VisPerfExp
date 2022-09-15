#!/bin/bash
rm -rf ./IntransitVaryDataSize_data

mkdir IntransitVaryDataSize_data
cd IntransitVaryDataSize_data

# soft link for the cloverleaf
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par
# soft link for the reader
ln -s ../../../../install/in_transit_reader/reader reader


# generate config file
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/ascent_actions_relay_adios_SST.yaml ascent_actions.yaml
cp ${scriptsDir}/adios2.xml adios2.xml
cp ${scriptsDir}/cloverleaf.json cloverleaf.json
cp ${scriptsDir}/clover.in_default clover.in

MESH_SIZE_LIST="51 64 80 100 126 158"
#MESH_SIZE_LIST="51"

for MESH_SIZE in ${MESH_SIZE_LIST}
do
echo "test the mesh size ${MESH_SIZE}"
cp ${scriptsDir}/clover.in_default clover.in
# start the reader firstly
# issue, the reader does not exist as expected
./reader --file=out.bp --read-method=SST --visualization-op=volume --sst-json-file=cloverleaf.json &> ./reader.log &
echo "start reader, prepar sim"
# start the sim to get the data
sed -i "s/64/${MESH_SIZE}/" clover.in
echo "start sim, executing"
./cloverleaf3d_par &> ./sim.log
mv sim.log sim.log.${MESH_SIZE}
mv timing.vis.0.out timing.vis.0.${MESH_SIZE}.out
mv reader.log reader.log.${MESH_SIZE}
echo "ok for ${MESH_SIZE}"
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
