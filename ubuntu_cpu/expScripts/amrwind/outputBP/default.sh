#!/bin/bash

mkdir -p defaultData
cd defaultData


ln -s ../../../../install/amr-wind/bin/amr_wind amr_wind
ln -s ../../../../install/visReader/reader reader

# generate config file for amd wind
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/damBreak.i damBreak.i
# the bbox for the damBreak is geometry.prob_hi = 0.2855 0.0571 0.08565
# update the step
sed -i "s/time.max_step                =   100000/time.max_step                =  6/" damBreak.i
# do not use the plot integrated with the sim
sed -i "s/time.plot_interval            =  5/time.plot_interval            =  7/" damBreak.i
# decrease the size of the box
#sed -i "s/0.2855/0.18/" damBreak.i
sed -i "s/ascent.output_frequency = 10/ascent.output_frequency = 1/" damBreak.i

cp ${scriptsDir}/ascent_actions_relay_adios_BP.yaml ascent_actions.yaml
sed -i "s/endstep: 10/endstep: 7/" ascent_actions.yaml

# this is necessary to make adios things works
cp ${scriptsDir}/adios2_BP.xml adios2.xml
cp ${scriptsDir}/dam.json dam.json

# remove previous adios file
rm -r output

mpirun -n 12 ./amr_wind damBreak.i

# reader
BPDir=/home/zw/cworkspace/VisPerfExp/ubuntu_cpu/expScripts/amrwind/outputBP/defaultData
NUM_SEEDS=1000
PROCNUM=12

mpirun -n ${PROCNUM} ./reader \
--read-method=BP4 \
--file=${BPDir}/output/out.bp \
--visualization-op=advect \
--seed-method=box \
--advect-seed-box-extents=0.0,0.28,0.0,0.055,0.0,0.085 \
--advect-num-seeds=${NUM_SEEDS} \
--advect-num-steps=1000 \
--record-trajectories=false \
--advect-step-size=0.01 \
--field-name=velocityVector \
--record-trajectories=false \
--sst-json-file=./dam.json \
--sim-code=wind



