#compare how different seeds box influences the exec time

#!/bin/bash
rm -rf ./varySeedsBox_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir varySeedsBox_data
cd varySeedsBox_data
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par

# generate config file
scriptsDir=../../../../../commonScripts

cp ${scriptsDir}/clover.in_default clover.in

# small
cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
sed -i 's/: 0.0/: 4.0/' ascent_actions.yaml
sed -i 's/: 10.0/: 6.0/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.4_6.out

# medium
cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
sed -i 's/: 0.0/: 2.0/' ascent_actions.yaml
sed -i 's/: 10.0/: 8.0/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.2_8.out

# large
cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.0_10.out

echo "check timing.0.4_6.out"
cat timing.0.4_6.out |grep ParticleAdvectionFilter |cut -d " " -f 2

echo "check timing.0.2_8.out"
cat timing.0.2_8.out |grep ParticleAdvectionFilter |cut -d " " -f 2

echo "check timing.0.0_10.out"
cat timing.0.0_10.out |grep ParticleAdvectionFilter |cut -d " " -f 2

