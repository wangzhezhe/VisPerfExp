#!/bin/bash
rm -rf ./InlinedefaultData

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir InlinedefaultData
cd InlinedefaultData
ln -s ../../../../install/amr-wind/bin/amr_wind amr_wind

# generate config file for amd wind
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/damBreak.i damBreak.i
sed -i "s/time.max_step                =   100000/time.max_step                =   20/" damBreak.i

# both the original mesh size and the level of the adaptive mesh size incluence 
# the execution time of the simulaion computation
# we set the simulation computation time as 1 now
cp ${scriptsDir}/ascent_actions_contour.yaml ascent_actions.yaml
sed -i "s/field: \"energy\"/field: \"density\"/" ascent_actions.yaml
# how to change the size of the mesh in this case, for the default case
# the three dimenstions are not same

# execute
./amr_wind damBreak.i
