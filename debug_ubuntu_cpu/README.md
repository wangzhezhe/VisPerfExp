

### build

install the reader, vtkm, vtkh fides and adios.

```
$git clone https://github.com/wangzhezhe/VisPerfExp.git
$cd VisPerfExp
$git checkout debug_streamline
$cd debug_ubuntu_cpu
$/bin/bash install.sh
```

update the library path shown at the end of the install script


### get data and run


get data from summit

```
$mkdir testrun
$cd testrun
$scp -r <userid>@summit.olcf.ornl.gov:/gpfs/alpine/proj-shared/csc143/zhewang/datasets/debugStreamline/out.bp .
```
prepare the config files

```
$cp ../../commonScripts/cloverleaf.json .
$ln ../install/visReader/reader reader
```

run the reader for the streamline

```
mpirun -n 32 ./reader --file=./out.bp --read-method=BP4 --visualization-op=advect --seed-method=box --advect-seed-box-extents=0,10,0,10,0,10 --advect-num-seeds=2048 --field-name=velocity --sst-json-file=./cloverleaf.json
```

The seeds coordinates can be checked by file such as 

generatedBoxOfSeeds_step0.out for each step.
