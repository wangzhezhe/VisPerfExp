#!/bin/bash
rm -rf ./varyImgsize_data

# create soft link
mkdir varyImgsize_data
cd varyImgsize_data
ln -s ../../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par

# generate config file
scriptsDir=../../../../../commonScripts
cp ${scriptsDir}/clover.in_default clover.in


#2048*2048
cp ${scriptsDir}/ascent_actions_volumerender.yaml ascent_actions.yaml
sed -i 's/output_r1/output_2048_2048_/' ascent_actions.yaml
sed -i 's/image_width: 1024/image_width: 2048/' ascent_actions.yaml
sed -i 's/image_height: 1024/image_height: 2048/' ascent_actions.yaml

./cloverleaf3d_par
cp timing.0.out timing.0.2048.2048.out 

#1024*2048
cp ${scriptsDir}/ascent_actions_volumerender.yaml ascent_actions.yaml
sed -i 's/output_r1/output_1024_2048_/' ascent_actions.yaml
sed -i 's/image_height: 1024/image_height: 2048/' ascent_actions.yaml

./cloverleaf3d_par
cp timing.0.out timing.0.1024.2048.out 


#1024*1024
cp ${scriptsDir}/ascent_actions_volumerender.yaml ascent_actions.yaml
sed -i 's/output_r1/output_1024_1024_/' ascent_actions.yaml
./cloverleaf3d_par
cp timing.0.out timing.0.1024.1024.out 


#1024*512
cp ${scriptsDir}/ascent_actions_volumerender.yaml ascent_actions.yaml
sed -i 's/image_width: 1024/image_width: 512/' ascent_actions.yaml
sed -i 's/output_r1/output_512_1024_/' ascent_actions.yaml

./cloverleaf3d_par

cp timing.0.out timing.0.512.1024.out 

#512*512
cp ${scriptsDir}/ascent_actions_volumerender.yaml ascent_actions.yaml
sed -i 's/image_width: 1024/image_width: 512/' ascent_actions.yaml
sed -i 's/image_height: 1024/image_height: 512/' ascent_actions.yaml
sed -i 's/output_r1/output_512_512_/' ascent_actions.yaml

./cloverleaf3d_par
cp timing.0.out timing.0.512.512.out 

#512*256
cp ${scriptsDir}/ascent_actions_volumerender.yaml ascent_actions.yaml
sed -i 's/image_width: 1024/image_width: 512/' ascent_actions.yaml
sed -i 's/image_height: 1024/image_height: 256/' ascent_actions.yaml
sed -i 's/output_r1/output_512_256_/' ascent_actions.yaml

./cloverleaf3d_par
cp timing.0.out timing.0.512.256.out 

#256*256
cp ${scriptsDir}/ascent_actions_volumerender.yaml ascent_actions.yaml
sed -i 's/image_width: 1024/image_width: 256/' ascent_actions.yaml
sed -i 's/image_height: 1024/image_height: 256/' ascent_actions.yaml
sed -i 's/output_r1/output_256_256_/' ascent_actions.yaml

./cloverleaf3d_par
cp timing.0.out timing.0.256.256.out 


echo "check timing.0.256.256.out"
cat timing.0.256.256.out |grep ExecScene |cut -d " " -f 2

echo "check timing.0.512.256.out"
cat timing.0.512.256.out |grep ExecScene |cut -d " " -f 2

echo "check timing.0.512.512.out"
cat timing.0.512.512.out |grep ExecScene |cut -d " " -f 2

echo "check timing.0.512.1024.out"
cat timing.0.512.1024.out |grep ExecScene |cut -d " " -f 2

echo "check timing.0.1024.1024.out"
cat timing.0.1024.1024.out |grep ExecScene |cut -d " " -f 2

echo "check timing.0.1024.2048.out"
cat timing.0.1024.2048.out |grep ExecScene |cut -d " " -f 2

echo "check timing.0.2048.2048.out"
cat timing.0.2048.2048.out |grep ExecScene |cut -d " " -f 2