The installation and exp scripts for the visulization performance study on ubuntu platform


### Depedency

git
cmake
opengl

### Installing and build


/bin/bash install.sh

Then exeport the necessary ld path at the end of executing install.sh, such as:

```
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/zw/cworkspace/src/performanceStudy/VisPerfExp/ubuntu_cpu/install/vtk-m/lib:/home/zw/cworkspace/src/performanceStudy/VisPerfExp/ubuntu_cpu/install/ADIOS2/lib:/home/zw/cworkspace/src/performanceStudy/VisPerfExp/ubuntu_cpu/install/fides/lib:/home/zw/cworkspace/src/performanceStudy/VisPerfExp/ubuntu_cpu/install/ascent/lib:/home/zw/cworkspace/src/performanceStudy/VisPerfExp/ubuntu_cpu/install/conduit-v0.8.4/lib:/home/zw/cworkspace/src/performanceStudy/VisPerfExp/ubuntu_cpu/install/vtk-h/lib:/home/zw/cworkspace/src/performanceStudy/VisPerfExp/ubuntu_cpu/install/hdf5-1.12.2/lib
```

