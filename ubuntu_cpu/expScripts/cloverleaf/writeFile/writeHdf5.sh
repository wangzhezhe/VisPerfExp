# compare how advection time change with different mesh size

#!/bin/bash
rm -rf ./writeHdf5_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir writeHdf5_data
cd writeHdf5_data
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par

# generate config file
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/ascent_actions_relay_hdf5.yaml ascent_actions.yaml

# #1.26*1.26*1.26 approximates to 2
#MESH_SIZE_LIST="64 80 100 126"
#MESH_SIZE_LIST="64 128 256"
MESH_SIZE_LIST="64"

for MESH_SIZE in ${MESH_SIZE_LIST}
do
echo "test the mesh size ${MESH_SIZE}"
#cp ../../../../src/ascent/src/examples/proxies/cloverleaf3d-ref/clover.in_nozzle clover.in
cp ${scriptsDir}/clover.in_jet clover.in
#cp ${scriptsDir}/clover.in_nozzle clover.in
#cp ${scriptsDir}/clover.in_balloffury clover.in

#sed -i "s/visit_initial_delay=300/visit_initial_delay=600/" clover.in
#sed -i "s/end_step=600/end_step=700/" clover.in
#sed -i "s/256/${MESH_SIZE}/" clover.in
#sed -i "s/128/${MESH_SIZE}/" clover.in

mpirun -n 10 ./cloverleaf3d_par &> sim.log

# put the output in specific dir
dirName=log_${MESH_SIZE}_8procs
mkdir ${dirName}
mv sim.log ${dirName}
mv timing.*.out ${dirName}
mv testoutput* ${dirName}
# also put config here to better trace the results
cp clover.in ${dirName}
cp ascent_actions.yaml ${dirName}
done