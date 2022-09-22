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

# Be careful, there are some issues for vtkm to compute the iso countour for the density field
# when we set the iso value larger than 2 , there are also issue
# the iso value for the attribute p looks good
cp ${scriptsDir}/ascent_actions_contour.yaml ascent_actions.yaml
sed -i "s/field: \"energy\"/field: \"p\"/" ascent_actions.yaml
sed -i "s/levels: 5/levels: 1/" ascent_actions.yaml

# how to change the size of the mesh in this case, for the default case
# the three dimenstions are not same

# execute
./amr_wind damBreak.i
