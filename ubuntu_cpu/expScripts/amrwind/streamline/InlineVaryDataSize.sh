#!/bin/bash
# rm -rf ./InlineVaryDataSizeData

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir -p InlineVaryDataSizeData
cd InlineVaryDataSizeData
ln -s ../../../../install/amr-wind/bin/amr_wind amr_wind

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



#MESH_SIZE_LIST="64 128 256 512 1024"

SEEDS_NUM_LIST="1000"

for SEEDS_NUM in ${SEEDS_NUM_LIST}
do

echo "processing the ${SEEDS_NUM}"

cp ${scriptsDir}/ascent_actions_streamline_amrwind_box.yaml ascent_actions.yaml

# update the seeds num
sed -i "s/num_seeds: 512/num_seeds: ${SEEDS_NUM}/" ascent_actions.yaml
sed -i "s/num_steps: 512/num_steps: 1000/" ascent_actions.yaml

sed -i "s/record_trajectories: 'true'/record_trajectories: 'false'/" ascent_actions.yaml
#sed -i "s/seed_bounding_box_xmax: 0.28/seed_bounding_box_xmax: 0.18/" ascent_actions.yaml


# execute
mpirun -n 2 ./amr_wind damBreak.i &> amrwindlog.out

# processing log
logdir=${SEEDS_NUM}_4procs_log
mkdir ${logdir}
mv amrwindlog.out ${logdir}
mv timing.*.out ${logdir}
mv counter* ${logdir}
mv damBreak.i ${logdir}
echo "ok for ${SEEDS_NUM}"
done

# TODO, show the advec time

#for SEEDS_NUM in ${SEEDS_NUM_LIST}
#do
#echo "checking the ${SEEDS_NUM}"
#cat ${SEEDS_NUM}.timing/timing.0.out |grep ParticleAdvectionFilter |cut -d " " -f 2
#done 