# compare how advection time change with different data size for writting bp file


#!/bin/bash
rm -rf ./varyDataSize_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir varyDataSize_data
cd varyDataSize_data
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par

# generate config file
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/ascent_actions_relay_adios_BP.yaml ascent_actions.yaml

MESH_SIZE_LIST="51 64 80 100 126 158"
#MESH_SIZE_LIST="51"

for MESH_SIZE in ${MESH_SIZE_LIST}
do
cp ${scriptsDir}/clover.in_default clover.in
# double quota for replacing the variable
sed -i "s/64/${MESH_SIZE}/" clover.in
./cloverleaf3d_par &> ./temp.log
mv temp.log temp.log.${MESH_SIZE}
echo "ok for ${MESH_SIZE}"
done


for MESH_SIZE in ${MESH_SIZE_LIST}
do
echo "check temp.log.${MESH_SIZE}"
cat temp.log.${MESH_SIZE} |grep ascent_execution_time | cut -d " " -f 8
done