#!/bin/bash
rm -rf ./defaultData

mkdir defaultData
cd defaultData
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par

# generate config file
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/clover.in_default clover.in


cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
sed -i 's/num_seeds: 512/num_seeds: 2048/' ascent_actions.yaml

jsrun -n 32 ./cloverleaf3d_par 
