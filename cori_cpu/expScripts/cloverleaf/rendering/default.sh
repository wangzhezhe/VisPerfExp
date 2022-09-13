#!/bin/bash
rm -rf ./defaultdata

# create soft link
mkdir defaultdata
cd defaultdata
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par

# generate config file
cp ../../../../../commonScripts/clover.in_default clover.in
cp ../../../../../commonScripts/ascent_actions_volumerender.yaml ascent_actions.yaml

# execute
srun -C haswell -n 32 ./cloverleaf3d_par
