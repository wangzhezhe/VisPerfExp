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

for MESH_SIZE in ${MESH_SIZE_LIST}
do
cp ${scriptsDir}/clover.in_default clover.in
# start the reader firstly
./reader --file=out.bp --read-method=SST --visualization-op=volume --sst-json-file=cloverleaf.json
# start the sim to get the data
sed -i "s/64/${MESH_SIZE}/" clover.in
# TODO, how to close the client properly?
./cloverleaf3d_par &> ./sim.log


mv sim.log sim.log.${MESH_SIZE}
mv timing.0.out timing.0.${MESH_SIZE}.out
echo "ok for ${MESH_SIZE}"
done


for MESH_SIZE in ${MESH_SIZE_LIST}
do
echo "check timing.0.${MESH_SIZE}.out"
cat timing.0.${MESH_SIZE}.out |grep ExecScene |cut -d " " -f 2
done
