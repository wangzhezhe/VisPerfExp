### Installing

prerequest commands:
cmake
curl
tar

```
module load cray-python
module swap PrgEnv-intel PrgEnv-gnu
module load cmake
ulimit -c unlimited

/bin/bash install.sh

# update the env for finding the .so file
# the <library path> will be generated by install.sh script after the installation completes
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:<library path>

# Then executing assocaited scripts using the sbatch
```