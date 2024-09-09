

refer to 

https://mochi.readthedocs.io/en/latest/hello-mochi.html#set-up-spack

https://github.com/mochi-hpc-experiments/platform-configurations/tree/main


git clone https://github.com/spack/spack.git

. spack/share/spack/setup-env.sh

git clone https://github.com/mochi-hpc/mochi-spack-packages.git

$ spack env create myenv ./src/VisPerfExp/ubuntu_cpu_vtkm2.0/install_mochi/spack.yaml

$ spack repo add ./mochi-spack-packages/
$ spack env activate myenv


spack compiler find

double check compler

spack compilers


make sure compiler is same with what we need

```
spack add mochi-margo %gcc@11.4.0
```

spack env rm myenv

after chaning the spack.yaml, we need to apply it to our environment, this is associated commands

spack env deactivate 
spack env rm myenv
spack env create myenv ./src/VisPerfExp/ubuntu_cpu_vtkm2.0/install_mochi/spack.yaml
spack env activate myenv
spack repo add ./mochi-spack-packages/
spack install --add mochi-thallium%gcc@11.4.0
