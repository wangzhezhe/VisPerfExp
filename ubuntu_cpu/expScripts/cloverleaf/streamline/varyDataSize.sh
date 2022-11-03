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


# #1.26*1.26*1.26 approximates to 2
#MESH_SIZE_LIST="64 80 100 126"
MESH_SIZE_LIST="64"

for MESH_SIZE in ${MESH_SIZE_LIST}
do
echo "test the mesh size ${MESH_SIZE}"
#cp ${scriptsDir}/clover.in_default clover.in
cp ${scriptsDir}/clover.in_jet clover.in

sed -i "s/64/${MESH_SIZE}/" clover.in
sed -i "s/end_step=600/end_step=300/" clover.in

cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
sed -i "s/write_streamlines: false/write_streamlines: true/" ascent_actions.yaml
sed -i "s/record_trajectories: true/record_trajectories: true/" ascent_actions.yaml
sed -i "s/step_size: 0.01/step_size: 0.1/" ascent_actions.yaml
sed -i "s/num_steps: 512/num_steps: 1000/" ascent_actions.yaml
sed -i "s/num_seeds: 512/num_seeds: 1000/" ascent_actions.yaml
sed -i "s/endstep: 10/endstep: 300/" ascent_actions.yaml

# set bounds of the seeds method
sed -i "s/xmin: 0.0/xmin: 1.5/" ascent_actions.yaml
sed -i "s/xmax: 10.0/xmax: 2.5/" ascent_actions.yaml

sed -i "s/ymin: 0.0/ymin: 1.5/" ascent_actions.yaml
sed -i "s/ymax: 10.0/ymax: 2.5/" ascent_actions.yaml

sed -i "s/zmin: 0.0/zmin: 0.0/" ascent_actions.yaml
sed -i "s/zmax: 10.0/zmax: 8.0/" ascent_actions.yaml



mpirun -n 2 ./cloverleaf3d_par &> sim.log
#mv timing.0.out timing.0.${MESH_SIZE}.out
#cat timing.0.${MESH_SIZE}.out |grep ParticleAdvectionFilter |cut -d " " -f 2

done
