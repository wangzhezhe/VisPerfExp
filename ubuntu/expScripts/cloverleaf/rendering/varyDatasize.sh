#!/bin/bash
rm -rf ./varyDataSize_data

# create soft link
mkdir varyDataSize_data
cd varyDataSize_data
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par

# generate config file
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/ascent_actions_volumerender.yaml ascent_actions.yaml


#1.2*1.2*1.2 approximate to 2

#51*51*51
cp ${scriptsDir}/clover.in_default clover.in
sed -i 's/64/51/' clover.in
./cloverleaf3d_par
mv timing.0.out timing.0.51.out

#64*64*64
cp ${scriptsDir}/clover.in_default clover.in
#default value is 64
./cloverleaf3d_par
mv timing.0.out timing.0.64.out

#80*80*80
cp ${scriptsDir}/clover.in_default clover.in
sed -i 's/64/80/' clover.in
./cloverleaf3d_par
mv timing.0.out timing.0.80.out

#100*100*100
cp ${scriptsDir}/clover.in_default clover.in
sed -i 's/64/100/' clover.in
mv timing.0.out timing.0.100.out

#126*126*126
cp ${scriptsDir}/clover.in_default clover.in
sed -i 's/64/126/' clover.in
mv timing.0.out timing.0.126.out