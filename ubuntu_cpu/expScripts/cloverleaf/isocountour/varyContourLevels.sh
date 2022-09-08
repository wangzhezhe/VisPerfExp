#!/bin/bash
rm -rf ./varyContourLevels_data

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir varyContourLevels_data
cd varyContourLevels_data
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par

# generate config file
scriptsDir=../../../../../commonScripts

cp ${scriptsDir}/clover.in_default clover.in

#2
cp ${scriptsDir}/ascent_actions_contour.yaml ascent_actions.yaml
sed -i 's/levels: 5/levels: 2/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.2.out

#4
cp ${scriptsDir}/ascent_actions_contour.yaml ascent_actions.yaml
sed -i 's/levels: 5/levels: 4/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.4.out

#8
cp ${scriptsDir}/ascent_actions_contour.yaml ascent_actions.yaml
sed -i 's/levels: 5/levels: 8/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.8.out

#16
cp ${scriptsDir}/ascent_actions_contour.yaml ascent_actions.yaml
sed -i 's/levels: 5/levels: 16/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.16.out

#32
cp ${scriptsDir}/ascent_actions_contour.yaml ascent_actions.yaml
sed -i 's/levels: 5/levels: 32/' ascent_actions.yaml
./cloverleaf3d_par
mv timing.0.out timing.0.32.out


LEVEL_NUM_LIST="2 4 8 16 32"

for LEVEL_NUM in ${LEVEL_NUM_LIST}
do
echo "check timing.0.${LEVEL_NUM}.out"
cat timing.0.${LEVEL_NUM}.out |grep ContourFilter |cut -d " " -f 2
done