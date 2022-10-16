#!/bin/bash
 
#BSUB -P csc143
#BSUB -W 00:59
#BSUB -nnodes 1

#BSUB -J InTranVarySeeds_32S_4R
#BSUB -o InTranVarySeeds_32S_4R.%J.out
#BSUB -e InTranVarySeeds_32S_4R%J.err 


# letting in transit using more resources?

CURRDIR=$(pwd)
DATA_DIRNAME=InTranVarySeeds_32S_4R_Data

rm -r $CURRDIR/$DATA_DIRNAME
mkdir -p $CURRDIR/$DATA_DIRNAME

cd $MEMBERWORK/csc143

rm -rf $DATA_DIRNAME
mkdir $DATA_DIRNAME
cd $DATA_DIRNAME

ln -s $CURRDIR/../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par
ln -s $CURRDIR/../../../install/visReader/reader reader

# generate config file
# copy them into the current working dir
scriptsDir=$CURRDIR/../../../../commonScripts
cp ${scriptsDir}/ascent_actions_relay_adios_SST.yaml ascent_actions.yaml

# this is for fides writer
cp ${scriptsDir}/adios2.xml adios2.xml
# this is for the fides write operation
cp ${scriptsDir}/cloverleaf.json cloverleaf.json
cp ${scriptsDir}/clover.in_default clover.in

# large seeds number may take too longtime to execute, limit the endstep here
sed -i "s/end_step=200/end_step=50/" clover.in


NUM_SEEDS_LIST="1000 10000 100000 1000000 10000000"
#NUM_SEEDS_LIST="1000000 10000000"
# 1000000 seeds may takes around 1800 seconds, around 0.5 hour

for NUM_SEEDS in ${NUM_SEEDS_LIST}
do

echo "test the seeds number ${NUM_SEEDS}"

# copy new ascent action every time
cp ${scriptsDir}/ascent_actions_relay_adios_SST.yaml ascent_actions.yaml
sed -i "s/endstep: 10/endstep: 50/" ascent_actions.yaml
sed -i "s/num_seeds: 512/num_seeds: ${NUM_SEEDS}/" ascent_actions.yaml
sed -i "s/record_trajectories: true/record_trajectories: false/" ascent_actions.yaml

# using 1 reader
jsrun -n 1 ./reader --file=out.bp --read-method=SST --visualization-op=advect --seed-method=box --advect-seed-box-extents=0,10,0,10,0,10 --advect-num-seeds=2048 --field-name=velocity --sst-json-file=./cloverleaf.json &> ./reader.log &

# using 32 sim
jsrun -n 32 ./cloverleaf3d_par &> sim.log

mkdir -p log_$NUM_SEEDS

mv reader.log log_$NUM_SEEDS
mv sim.log log_$NUM_SEEDS
mv timing.*.out log_$NUM_SEEDS

# copy things back
cp -r log_$NUM_SEEDS $CURRDIR/$DATA_DIRNAME
done


