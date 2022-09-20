# compare how advection time changes with different numbers of seeds
# we run this script on interactive node of the gpu machine

#!/bin/bash
rm -rf ./varySeedsNum_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir varySeedsNum_data
cd varySeedsNum_data
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par

# generate config file
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/clover.in_default clover.in

#32
cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
sed -i 's/num_seeds: 512/num_seeds: 32/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.32.out

#64
cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
sed -i 's/num_seeds: 512/num_seeds: 64/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.64.out

#128
cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
sed -i 's/num_seeds: 512/num_seeds: 128/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.128.out

#256
cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
sed -i 's/num_seeds: 512/num_seeds: 256/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.256.out

#512
cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
sed -i 's/num_seeds: 512/num_seeds: 512/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.512.out

#1024
cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
sed -i 's/num_seeds: 512/num_seeds: 1024/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.1024.out


SEED_NUM_LIST="32 64 128 256 512 1024"

for SEED_NUM in ${SEED_NUM_LIST}
do
echo "check timing.0.${SEED_NUM}.out"
cat timing.0.${SEED_NUM}.out |grep ParticleAdvectionFilter |cut -d " " -f 2
done
