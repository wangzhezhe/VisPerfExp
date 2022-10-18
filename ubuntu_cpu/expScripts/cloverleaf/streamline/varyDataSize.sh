# compare how advection time change with different mesh size

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
cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
sed -i "s/write_streamlines: false/write_streamlines: true/" ascent_actions.yaml
sed -i "s/step_size: 0.01/step_size: 0.1/" ascent_actions.yaml
sed -i "s/num_steps: 512/num_steps: 1000/" ascent_actions.yaml


# #1.26*1.26*1.26 approximates to 2
MESH_SIZE_LIST="64 80 100 126"
#MESH_SIZE_LIST="64"

for MESH_SIZE in ${MESH_SIZE_LIST}
do
echo "test the mesh size ${MESH_SIZE}"
cp ${scriptsDir}/clover.in_default clover.in
#cp ${scriptsDir}/clover.in_jet clover.in

sed -i "s/64/${MESH_SIZE}/" clover.in
mpirun -n 4 ./cloverleaf3d_par > sim.${MESH_SIZE}.log
mv timing.0.out timing.0.${MESH_SIZE}.out

cat timing.0.${MESH_SIZE}.out |grep ParticleAdvectionFilter |cut -d " " -f 2

done
