#!/bin/bash
rm -rf ./defaultData

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir defaultData
cd defaultData
ln -s ../../../../install/amr-wind/bin/amr_wind amr_wind

# generate config file for amd wind
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/damBreak.i damBreak.i

sed -i "s/time.max_step                =   100000/time.max_step                =   120/" damBreak.i
# do not use the plot integrated with the sim
sed -i "s/time.plot_interval            =  5/time.plot_interval            =  121/" damBreak.i
sed -i "s/0.2855/0.18/" damBreak.i

# both the original mesh size and the level of the adaptive mesh size incluence 
# the execution time of the simulaion computation
# we set the simulation computation time as 1 now
cp ${scriptsDir}/ascent_actions_relay_hdf5.yaml ascent_actions.yaml

# execute
mpirun -n 8 ./amr_wind damBreak.i
