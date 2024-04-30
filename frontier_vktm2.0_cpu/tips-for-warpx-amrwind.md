
using the gcc as the default compiler

for example, on frontier:

module load gcc

### Building ascent

Remember to set using MPI
The installing script can be found here
This is the basic version
https://github.com/Alpine-DAV/ascent/blob/develop/scripts/build_ascent/build_ascent.sh

we need to do some updates based on this version:
unset the unnecessary packages, such as catalyst
enable the MPI
unset the verbose setting

when build the hdf5 with MPI
adding following parameter
-DHDF5_ENABLE_PARALLEL=ON

this will be used by warpx

### When installing the warpx

openPMD backend can be h5, adios or json

The associated command with hd5f can be in this pattern

cmake .. -DHDF5_DIR=/ccs/home/zw241/cworkspace/ascent/ascent/scripts/build_ascent/install/hdf5-1.14.1-2/cmake/ -DopenPMD_USE_HDF5=ON

This is a question descussion regarding the openPMD output

https://github.com/ECP-WarpX/WarpX/issues/4602


The laser accelaration config
https://github.com/ECP-WarpX/WarpX/tree/development/Examples/Physics_applications/laser_acceleration


The laser Ion config

https://github.com/ECP-WarpX/WarpX/tree/development/Examples/Physics_applications/laser_ion

loading necessary .so file

export LD_LIBRARY_PATH=/ccs/home/zw241/cworkspace/ascent/install/hdf5-1.14.1-2/lib:/ccs/home/zw241/cworkspace/ascent/install/vtk-m-v2.1.0/lib:/ccs/home/zw241/cworkspace/ascent/install/camp-2022.10.1/lib:/ccs/home/zw241/cworkspace/ascent/install/mfem-4.5.2/lib:/ccs/home/zw241/cworkspace/ascent/install/umpire-2022.10.0/lib:/ccs/home/zw241/cworkspace/ascent/install/raja-v2022.10.4/lib:${LD_LIBRARY_PATH}

The pattern for naming binary of warpx might be good
when having each capbility, it add dot with something
for example
warpx.3d.MPI.OMP.DP.PDP.ASCENT.OPMD.QED
is buit by MPI OMP ASCENT etc

ok to run binary at the build dir
there are some issues to find proper library to run things at the install dir

### When installing the amrwind

looking at details here

https://github.com/wangzhezhe/VisPerfExp/tree/main/ubuntu_cpu/expScripts/amrwind