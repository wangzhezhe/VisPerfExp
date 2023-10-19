#!/bin/bash

# allocate four node
# check there is no running runtask-simmit.sh before run
CURRDIR=$(pwd)

cd $MEMBERWORK/csc143

mkdir -p ./weak-weak-output-optimization

cd ./weak-weak-output-optimization

if [ ! -f "visitReaderAdev" ];then
# not exist
ln -s $CURRDIR/../summit_vtkm2.0_cpu/install/visReader/visitReaderAdev visitReaderAdev
fi

# copy config file
cp $CURRDIR/assign_options.config .

#echo "execute job"

jsrun -n8 -r2 -a16 -c16 -g0 -bpacked:1 ./visitReaderAdev \
--vtkm-device serial \
--file=/gpfs/alpine/csc143/proj-shared/pugmire/forJay/VisPerfExp/ubuntu_cpu_vtkm2.0/runDIR/resample2/astro.4_4_8.visit \
--advect-num-steps=2000 \
--advect-num-seeds=5000 \
--seeding-method=domainrandom \
--advect-seed-box-extents=0.010000,0.990000,0.010000,0.990000,0.010000,0.990000 \
--field-name=velocity \
--advect-step-size=0.005000 \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--communication=async_probe \
--assign-strategy=file &> readerlog.out