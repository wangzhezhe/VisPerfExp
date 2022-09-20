#!/bin/bash
rm -rf ./IntrandefaultData

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir IntrandefaultData
cd IntrandefaultData
ln -s ../../../../install/amr-wind/bin/amr_wind amr_wind
# soft link for the reader
ln -s ../../../../install/in_transit_reader/reader reader

# generate config file for amd wind
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/damBreak.i damBreak.i
sed -i "s/time.max_step                =   100000/time.max_step                =   10/" damBreak.i


cp ${scriptsDir}/ascent_actions_relay_adios_SST.yaml ascent_actions.yaml

# prepare scritps for fides and adios
cp ${scriptsDir}/adios2.xml adios2.xml
cp ${scriptsDir}/dam.json dam.json

# start reader
# pay attention to the sim code, the default one is the cloverleaf
./reader --file=out.bp --read-method=SST --visualization-op=volume --sst-json-file=dam.json --sim-code=wind --field-name=density &> reader.log &

sleep 1

# execute
./amr_wind damBreak.i
