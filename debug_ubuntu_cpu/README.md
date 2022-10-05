

### build

```
$cd debug_ubuntu_cpu
$/bin/bash install.sh
```

update the library path


### get data and run

```
$mkdir testrun
$cp ../../commonScripts/cloverleaf.json .
$ln ../install/visReader/reader reader
```
get data from summit

```
scp -r zw241@summit.olcf.ornl.gov:/gpfs/alpine/proj-shared/csc143/zhewang/datasets/debugStreamline/out.bp .
```

run the reader based streamline

```
mpirun -n 32 ./reader --file=./out.bp --read-method=BP4 --visualization-op=advect --seed-method=box --advect-seed-box-extents=0,10,0,10,0,10 --advect-num-seeds=2048 --field-name=velocity --sst-json-file=./cloverleaf.json
```