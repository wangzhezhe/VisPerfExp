#!/bin/bash
 
#BSUB -P csc143
#BSUB -W 01:59
#BSUB -nnodes 25

#BSUB -J Inline_default_varyProcs
#BSUB -o R_Inline_default_varyProcs.%J.out
#BSUB -e R_Inline_default_varyProcs.%J.err 

CURRDIR=$(pwd)
DATA_DIRNAME=Inline_default_varyProcs

#rm -r $CURRDIR/$DATA_DIRNAME
mkdir -p $CURRDIR/$DATA_DIRNAME

cd $MEMBERWORK/csc143

rm -rf $DATA_DIRNAME
mkdir $DATA_DIRNAME
cd $DATA_DIRNAME

ln -s $CURRDIR/../../install/amr-wind/bin/amr_wind amr_wind

# generate config file
# copy them into the current working dir

# it hangs here if the number of process is larger than mesh size
scriptsDir=$CURRDIR/../../../commonScripts

NUM_PROCS_LIST="1024 512 256 128 64 32 16"
NUM_SEEDS_LIST="1000"

cp $CURRDIR/../../../commonScripts/damBreak.i damBreak.i
# the bbox for the damBreak is geometry.prob_hi = 0.2855 0.0571 0.08565
# update the step
sed -i "s/time.max_step                =   100000/time.max_step                =  100/" damBreak.i
# do not use the plot integrated with the sim
sed -i "s/time.plot_interval            =  5/time.plot_interval            =  101/" damBreak.i
# !! there is issue to run at large scale such as 16 if we change the x value
# sed -i "s/0.2855/0.18/" damBreak.i


for NUM_PROCS in ${NUM_PROCS_LIST}
do

echo "test the procs number ${NUM_PROCS}"

for NUM_SEEDS in ${NUM_SEEDS_LIST}
do

echo "test the seeds number ${NUM_SEEDS}"

cp ${scriptsDir}/ascent_actions_streamline_amrwind_box.yaml ascent_actions.yaml

# set the record trajectories as fals to do the particle advecation instead of streamline filter
sed -i "s/record_trajectories: true/record_trajectories: false/" ascent_actions.yaml
sed -i "s/num_seeds: 512/num_seeds: ${NUM_SEEDS}/" ascent_actions.yaml
sed -i "s/num_steps: 512/num_steps: 1000/" ascent_actions.yaml
sed -i "s/endstep: 10/endstep: 100/" ascent_actions.yaml

# execute
jsrun -n ${NUM_PROCS} ./amr_wind damBreak.i &> amrwindlog.out

# processing log
logdir=${NUM_PROCS}_${NUM_SEEDS}_log
mkdir -p ${logdir}
mv amrwindlog.out ${logdir}
mv timing.*.out ${logdir}
mv counter* ${logdir}
mv damBreak.i ${logdir}
mv ascent_actions.yaml ${logdir}

sleep 1

# copy things back
cp -r ${logdir} $CURRDIR/$DATA_DIRNAME
done
done
