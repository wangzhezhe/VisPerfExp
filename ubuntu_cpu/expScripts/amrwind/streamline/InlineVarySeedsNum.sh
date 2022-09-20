#!/bin/bash
rm -rf ./InlineVarySeedsNumData

# the data size basically decide how much clear the figure is
# for the same size of the data, it is more clear if we have a larger data mesh

# create soft link
mkdir InlineVarySeedsNumData
cd InlineVarySeedsNumData
ln -s ../../../../install/amr-wind/bin/amr_wind amr_wind

# generate config file for amd wind
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/damBreak.i damBreak.i
# the bbox for the damBreak is geometry.prob_hi = 0.2855 0.0571 0.08565

#SEEDS_NUM_LIST="64 128 256 512 1024"

SEEDS_NUM_LIST="64"

for SEEDS_NUM in ${SEEDS_NUM_LIST}
do

cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml
# update bbx
sed -i "s/seed_bounding_box_xmax: 10.0/seed_bounding_box_xmax: 0.28/" ascent_actions.yaml
sed -i "s/seed_bounding_box_ymax: 10.0/seed_bounding_box_ymax: 0.05/" ascent_actions.yaml
sed -i "s/seed_bounding_box_zmax: 10.0/seed_bounding_box_zmax: 0.08/" ascent_actions.yaml

# update the seeds num
sed -i "s/num_seeds: 512/num_seeds: ${SEEDS_NUM}/" ascent_actions.yaml

# execute
./amr_wind damBreak.i

# processing log
mkdir ${SEEDS_NUM}.timing
mv timing.*.out ${SEEDS_NUM}.timing/

echo "ok for ${SEEDS_NUM}"
done