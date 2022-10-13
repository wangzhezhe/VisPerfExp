# Do the data based on the streamline filter
# and then write out the data as the hdf5 format

#!/bin/bash
rm -rf ./InlineStreamlineAndHdf5_data

# create soft link
mkdir InlineStreamlineAndHdf5_data
cd InlineStreamlineAndHdf5_data
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par

# generate config files
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/clover.in_default clover.in
cp ${scriptsDir}/ascent_actions_streamline_box_relay_hdf5.yaml ascent_actions.yaml

mpirun -n 4 ./cloverleaf3d_par
