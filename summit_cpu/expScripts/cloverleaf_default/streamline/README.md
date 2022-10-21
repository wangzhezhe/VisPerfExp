

### Steps for reproducing the streamline issue

login to the summit

go to the work dir, such as

```
cd $PROJWORK/csc143/zhewang/VisPerfExp
```

try to allocate an interactive node

```
bsub -Is -W 1:00 -nnodes 1 -P csc143 $SHELL
```

load necessary module

```
module load gcc
module load cmake
```

install softwares

```
$ cd summit_cpu/
$ /bin/bash install.sh 
SOFTWARE_SRC_DIR: /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/src
====> Installing hdf5-1.12.2
====> Installing hdf5-1.12.2 ok
====> Installing conduit
====> skip, /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/conduit-v0.8.4 already exists, please remove it if you want to reinstall it
====> Installing conduit, ok
====> Installing vtk-m
====> skip, /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-m already exists, please remove it if you want to reinstall it
====> Installing vtk-m, ok
====> Installing vtk-h
====> skip, /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-h already exists, please remove it if you want to reinstall it
====> Installing vtk-h, ok
====> Installing adios
====> skip, /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/ADIOS2 already exists, please remove it if you want to reinstall it
====> Installing adios,ok
====> Installing fides
====> skip, /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/fides already exists, please remove it if you want to reinstall it
====> Installing fides, ok
====> Installing ascent
====> skip, /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/ascent already exists, please remove it if you want to reinstall it
====> Installing ascent, ok
====> Installing amr-wind
====> skip, /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/amr-wind already exists, please remove it if you want to reinstall it
====> Installing amr-wind, ok
====> Installing intransit reader
====> skip, /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/visReader already exists, please remove it if you want to reinstall it
====> building intransit reader, ok
try to add library path by executing:
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-m/lib:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/ADIOS2/lib:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/fides/lib:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/ascent/lib:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/conduit-v0.8.4/lib:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-h/lib:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/hdf5-1.12.2/lib

```

load the library printed out at the end of installation

```
$export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-m/lib:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/ADIOS2/lib:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/fides/lib:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/ascent/lib:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/conduit-v0.8.4/lib:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-h/lib:/gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/hdf5-1.12.2/lib
```

Execute the streamline exmaple

```
$ cd expScripts/cloverleaf/streamline
$ /bin/bash default.sh 
```
