

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

There are errors such as 

```
cloverleaf3d_par: /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-m/include/vtkm-1.0/vtkm/filter/particleadvection/AdvectorBaseAlgorithm.h:430: void vtkm::filter::particleadvection::AdvectorBaseAlgorithm<DataSetIntegratorType, ResultType>::Update(std::vector<vtkm::Particle>&, const std::vector<vtkm::Particle>&, const std::unordered_map<int, std::vector<int> >&) [with DataSetIntegratorType = vtkm::filter::particleadvection::DataSetIntegrator; ResultType = vtkm::worklet::StreamlineResult<vtkm::Particle>]: Assertion `particles.size() == idsMap.size()' failed.

Loguru caught a signal: SIGABRT
Stack trace:
26      0x200009134264 __libc_start_main + 180
25      0x200009134078 /lib64/power9/libc.so.6(+0x24078) [0x200009134078]
24          0x100027f8 ./cloverleaf3d_par() [0x100027f8]
23          0x10028a70 ./cloverleaf3d_par() [0x10028a70]
22          0x10030078 ./cloverleaf3d_par() [0x10030078]
21          0x10048de0 ./cloverleaf3d_par() [0x10048de0]
20      0x20000015ee24 ascent_execute + 52
19      0x20000015d61c ascent::Ascent::execute(conduit::Node const&) + 396
18      0x200000170f1c ascent::AscentRuntime::Execute(conduit::Node const&) + 1004
17      0x200001486574 flow::Workspace::execute() + 980
16      0x20000033ed18 ascent::runtime::filters::VTKHParticleAdvection::execute() + 5432
15      0x200002556f80 vtkh::Filter::Update() + 940
14      0x2000029ecdd4 vtkh::Streamline::DoExecute() + 1336
13      0x2000029ee558 /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-h/lib/libvtkh_filters_mpi.so(+0x74e558) [0x2000029ee558]
12      0x2000029f0124 /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-h/lib/libvtkh_filters_mpi.so(+0x750124) [0x2000029f0124]
11      0x2000029f2464 /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-h/lib/libvtkh_filters_mpi.so(+0x752464) [0x2000029f2464]
10      0x2000029f3d60 /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-h/lib/libvtkh_filters_mpi.so(+0x753d60) [0x2000029f3d60]
9       0x2000029f6170 /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-h/lib/libvtkh_filters_mpi.so(+0x756170) [0x2000029f6170]
8       0x2000029f823c /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-h/lib/libvtkh_filters_mpi.so(+0x75823c) [0x2000029f823c]
7       0x2000029fadb0 /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-h/lib/libvtkh_filters_mpi.so(+0x75adb0) [0x2000029fadb0]
6       0x2000029fd540 /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-h/lib/libvtkh_filters_mpi.so(+0x75d540) [0x2000029fd540]
5       0x2000029ffa04 /gpfs/alpine/proj-shared/csc143/zhewang/VisPerfExp/summit_cpu/install/vtk-h/lib/libvtkh_filters_mpi.so(+0x75fa04) [0x2000029ffa04]
4       0x200009147014 __assert_fail + 100
3       0x200009146f70 /lib64/power9/libc.so.6(+0x36f70) [0x200009146f70]
2       0x200009133a2c abort + 356
1       0x200009153618 gsignal + 216
0       0x2000000504d8 __kernel_sigtramp_rt64 + 0
2022-10-02 10:30:17.095 (   2.588s) [main thread     ]                       :0     FATL| Signal: SIGABRT
```

If the vtkh or vtkm code is updated for the software stack, just remove `VisPerfExp/summit_cpu/src/install/vtk-h` and `VisPerfExp/summit_cpu/src/install/vtk-m`, then execute the `/bin/bash install.sh` under the `VisPerfExp/summit_cpu` dir.