#!/bin/bash

set -e

#setting up necessary env on cori
module purge
module load cgpu cuda gcc openmpi
module load cmake/3.22.1

HERE=`pwd`
build_jobs=4
source $HERE/settings.sh
SOFTWARE_SRC_DIR="$HERE/src"
SOFTWARE_BUILD_DIR="$HERE/build"
SOFTWARE_INSTALL_DIR="$HERE/install"

if [ ! -d $SOFTWARE_SRC_DIR ];
    then
    mkdir $SOFTWARE_SRC_DIR
fi
echo "SOFTWARE_SRC_DIR: $SOFTWARE_SRC_DIR"

echo "====> Installing hdf5-1.12.2"
HDF5_SRC_DIR="$SOFTWARE_SRC_DIR/hdf5-1.12.2"
HDF5_BUILD_DIR="$SOFTWARE_BUILD_DIR/hdf5-1.12.2"
HDF5_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/hdf5-1.12.2"

if [ ! -f hdf5-1.12.2.tar.gz ]; then
  curl -L $HDF5_REPO -o hdf5-1.12.2.tar.gz
fi

if [ ! -d ${HDF5_SRC_DIR} ]; then
  echo "**** Downloading hdf5-1.12.2.tar.gz "
  tar -xzf hdf5-1.12.2.tar.gz -C $SOFTWARE_SRC_DIR
fi

if [ ! -d ${HDF5_INSTALL_DIR} ]; then
echo "**** Configuring HDF5"
cmake -S ${HDF5_SRC_DIR} -B ${HDF5_BUILD_DIR} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=${HDF5_INSTALL_DIR} \
  -DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_COMPILER=gcc

echo "**** Building HDF5"
cmake --build ${HDF5_BUILD_DIR} -j${build_jobs}
echo "**** Installing HDF5"
cmake --install ${HDF5_BUILD_DIR}
fi

echo "====> Installing hdf5-1.12.2 ok"

echo "====> Installing conduit"
CONDUIT_SRC_DIR="$SOFTWARE_SRC_DIR/conduit-${conduit_version}"
CONDUIT_BUILD_DIR="$SOFTWARE_BUILD_DIR/conduit-${conduit_version}"
CONDUIT_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/conduit-${conduit_version}"

# TODO, make sure the hdf5 is installed here

# checking the existance of the conduit
if [ -d $CONDUIT_INSTALL_DIR ]; then
    echo "====> skip, $CONDUIT_INSTALL_DIR already exists," \
             "please remove it if you want to reinstall it"
else
    # clone and install by cmake
    if [ ! -d $CONDUIT_SRC_DIR ]; then
    curl -L $CONDUIT_REPO -o ${conduit_tarball}
    tar -xzf ${conduit_tarball} -C $SOFTWARE_SRC_DIR
    fi

    # execute cmake
    if [ ! -d $CONDUIT_INSTALL_DIR ]; then 
    cmake -B ${CONDUIT_BUILD_DIR} -S ${CONDUIT_SRC_DIR}/src \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=${CONDUIT_INSTALL_DIR} \
    -DENABLE_FORTRAN=ON \
    -DENABLE_MPI=ON \
    -DENABLE_PYTHON=OFF \
    -DHDF5_DIR=${HDF5_INSTALL_DIR} \
    -DENABLE_TESTS=OFF \
    -DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_COMPILER=gcc


    echo "**** Building conduit"
    cmake --build ${CONDUIT_BUILD_DIR} -j${build_jobs}
    echo "**** Installing conduit"
    cmake --install ${CONDUIT_BUILD_DIR}
    fi 
fi

echo "====> Installing conduit, ok"
echo "====> Installing vtk-m"

VTKM_SRC_DIR="$SOFTWARE_SRC_DIR/vtk-m"
VTKM_BUILD_DIR="$SOFTWARE_BUILD_DIR/vtk-m"
VTKM_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/vtk-m"

# check the install dir
if [ -d $VTKM_INSTALL_DIR ]; then
    echo "====> skip, $VTKM_INSTALL_DIR already exists," \
             "please remove it if you want to reinstall it"
else
    echo $VTKM_SRC_DIR
    echo $VTKM_BUILD_DIR
    echo $VTKM_INSTALL_DIR
    # check vktm source dir
    if [ ! -d $VTKM_SRC_DIR ]; then
    # clone the source
    cd $SOFTWARE_SRC_DIR
    git clone $VTKM_REPO
    cd $VTKM_SRC_DIR
    git checkout 2021-performanceStudy
    fi
    
    cd $HERE

    # build and install
    echo "**** Building vtk-m"

    # TODO, the gpu version can be different here
    # we only use the cpu version here
    cmake -B ${VTKM_BUILD_DIR} -S ${VTKM_SRC_DIR} \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=ON \
    -DVTKm_USE_DEFAULT_TYPES_FOR_ASCENT=ON \
    -DVTKm_USE_DOUBLE_PRECISION=ON \
    -DVTKm_USE_64BIT_IDS=OFF \
    -DCMAKE_INSTALL_PREFIX=${VTKM_INSTALL_DIR} \
    -DVTKm_ENABLE_MPI=ON \
    -DVTKm_ENABLE_OPENMP=OFF \
    -DVTKm_ENABLE_RENDERING=ON \
    -DVTKm_ENABLE_CUDA=ON \
    -DVTKm_ENABLE_TESTING=OFF \
    -DVTKm_CUDA_Architecture=volta \
    -DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_COMPILER=gcc
    
    cmake --build ${VTKM_BUILD_DIR} -j${build_jobs}

    echo "**** Installing vtk-m"
    cmake --install ${VTKM_BUILD_DIR}
fi
echo "====> Installing vtk-m, ok"


echo "====> Installing vtk-h"
VTKH_SRC_DIR="$SOFTWARE_SRC_DIR/vtk-h"
VTKH_BUILD_DIR="$SOFTWARE_BUILD_DIR/vtk-h"
VTKH_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/vtk-h"



if [ -d $VTKH_INSTALL_DIR ]; then
    echo "====> skip, $VTKH_INSTALL_DIR already exists," \
             "please remove it if you want to reinstall it"
else
    echo $VTKH_SRC_DIR
    echo $VTKH_BUILD_DIR
    echo $VTKH_INSTALL_DIR
    # check vktm source dir
    if [ ! -d $VTKH_SRC_DIR ]; then
    # clone the source
    cd $SOFTWARE_SRC_DIR
    git clone --recursive $VTKH_REPO
    cd $VTKH_SRC_DIR
    git checkout 2021-performanceStudy
    git submodule init
    git submodule update
    fi
    
    cd $HERE

    # build and install
    # static libraries are required when building with cuda
    echo "**** Building vtk-h"

    cmake -B ${VTKH_BUILD_DIR} -S ${VTKH_SRC_DIR}/src \
    -DVTKM_DIR=${VTKM_INSTALL_DIR} \
    -DENABLE_MPI=ON \
    -DENABLE_SERIAL=OFF \
    -DENABLE_TESTS=OFF \
    -DENABLE_GTEST=OFF \
    -DCMAKE_INSTALL_PREFIX=${VTKH_INSTALL_DIR} \
    -DBUILD_SHARED_LIBS=OFF \
    -DENABLE_LOGGING=ON \
    -DENABLE_CUDA=ON \
    -DCMAKE_CUDA_ARCHITECTURES=70 \
    -DBLT_CXX_STD=c++14 \
    -DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_COMPILER=gcc
    
    
    cmake --build ${VTKH_BUILD_DIR} -j${build_jobs}

    echo "**** Installing vtk-m"
    cmake --install ${VTKH_BUILD_DIR}
fi
echo "====> Installing vtk-h, ok"


echo "====> Installing adios"
ADIOS_SRC_DIR="$SOFTWARE_SRC_DIR/ADIOS2"
ADIOS_BUILD_DIR="$SOFTWARE_BUILD_DIR/ADIOS2"
ADIOS_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/ADIOS2"

if [ -d $ADIOS_INSTALL_DIR ]; then
    echo "====> skip, $ADIOS_INSTALL_DIR already exists," \
             "please remove it if you want to reinstall it"
else
    # check vktm source dir
    if [ ! -d $ADIOS_SRC_DIR ]; then
    # clone the source
    cd $SOFTWARE_SRC_DIR
    git clone $ADIOS2_REPO
    cd $ADIOS_SRC_DIR
    git checkout $ADIOS2_COMMIT
    fi
    
    cd $HERE

    # build and install
    echo "**** Building adios2"

    # TODO, the gpu version can be different here
    # we only use the cpu version here

    cmake -B ${ADIOS_BUILD_DIR} -S ${ADIOS_SRC_DIR} \
    -DCMAKE_BUILD_TYPE=Release \
    -DADIOS2_RUN_INSTALL_TEST=OFF \
    -DBUILD_TESTING=OFF \
    -DCMAKE_INSTALL_PREFIX=${ADIOS_INSTALL_DIR} \
    -DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_COMPILER=gcc
    
    cmake --build ${ADIOS_BUILD_DIR} -j${build_jobs}

    echo "**** Installing vtk-m"
    cmake --install ${ADIOS_BUILD_DIR}
fi
echo "====> Installing adios,ok"


echo "====> Installing fides"
FIDES_SRC_DIR="$SOFTWARE_SRC_DIR/fides"
FIDES_BUILD_DIR="$SOFTWARE_BUILD_DIR/fides"
FIDES_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/fides"


if [ -d $FIDES_INSTALL_DIR ]; then
    echo "====> skip, $FIDES_INSTALL_DIR already exists," \
             "please remove it if you want to reinstall it"
else
    # check vktm source dir
    if [ ! -d $FIDES_SRC_DIR ]; then
    # clone the source
    cd $SOFTWARE_SRC_DIR
    git clone $FIDES_REPO
    fi

    cd $FIDES_SRC_DIR
    git checkout 2021_performanceStudy

    cmake -B ${FIDES_BUILD_DIR} -S ${FIDES_SRC_DIR} \
    -DADIOS2_DIR=${ADIOS_INSTALL_DIR}/lib64/cmake/adios2 \
    -DVTKm_DIR=${VTKM_INSTALL_DIR}/lib/cmake/vtkm-1.0 \
    -DCMAKE_INSTALL_PREFIX=${FIDES_INSTALL_DIR} \
    -DENABLE_MPI=ON \
    -DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_COMPILER=gcc
    
    cd $HERE

    # build and install
    echo "**** Building fides"
    
    cmake --build ${FIDES_BUILD_DIR} -j${build_jobs}

    echo "**** Installing fides"
    cmake --install ${FIDES_BUILD_DIR}
fi
echo "====> Installing fides, ok"

echo "====> Installing ascent"
ASCENT_SRC_DIR="$SOFTWARE_SRC_DIR/ascent"
ASCENT_BUILD_DIR="$SOFTWARE_BUILD_DIR/ascent"
ASCENT_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/ascent"


if [ -d $ASCENT_INSTALL_DIR ]; then
    echo "====> skip, $ASCENT_INSTALL_DIR already exists," \
             "please remove it if you want to reinstall it"
else
    # check vktm source dir
    if [ ! -d $ASCENT_SRC_DIR ]; then
    # clone the source
    cd $SOFTWARE_SRC_DIR
    git clone --recursive $ASCENT_REPO
    fi

    cd $ASCENT_SRC_DIR
    git checkout performanceStudy
    git submodule init
    git submodule update
    
    # statlic likbrary for cuda build
    cmake -B ${ASCENT_BUILD_DIR} -S ${ASCENT_SRC_DIR}/src \
    -DCONDUIT_DIR=${CONDUIT_INSTALL_DIR} \
    -DENABLE_PYTHON=OFF \
    -DCMAKE_INSTALL_PREFIX=${ASCENT_INSTALL_DIR} \
    -DENABLE_ADIOS2=ON \
    -DADIOS2_DIR=${ADIOS_INSTALL_DIR}/lib64/cmake/adios2 \
    -DFIDES_DIR=${FIDES_INSTALL_DIR} \
    -DVTKM_DIR=${VTKM_INSTALL_DIR} \
    -DASCENT_VTKH_ENABLED=ON \
    -DVTKH_DIR=${VTKH_INSTALL_DIR} \
    -DENABLE_SERIAL=OFF \
    -DENABLE_MPI=ON \
    -DENABLE_TESTS=OFF \
    -DENABLE_EXAMPLES=ON \
    -DENABLE_LOGGING=ON \
    -DCMAKE_INSTALL_PREFIX=${ASCENT_INSTALL_DIR} \
    -DBUILD_SHARED_LIBS=OFF \
    -DENABLE_CUDA=ON \
    -DCMAKE_CUDA_ARCHITECTURES=70 \
    -DBLT_CXX_STD=c++14 \
    -DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_COMPILER=gcc
    
    cd $HERE

    # build and install
    echo "**** Building ascent"
    cmake --build ${ASCENT_BUILD_DIR} -j${build_jobs}

    echo "**** Installing ascent"
    cmake --install ${ASCENT_BUILD_DIR}
fi


echo "====> Installing ascent, ok"


echo "====> Installing amr-wind"
AMRWIND_SRC_DIR="$SOFTWARE_SRC_DIR/amr-wind"
AMRWIND_BUILD_DIR="$SOFTWARE_BUILD_DIR/amr-wind"
AMRWIND_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/amr-wind"


if [ -d $AMRWIND_INSTALL_DIR ]; then
    echo "====> skip, $AMRWIND_INSTALL_DIR already exists," \
             "please remove it if you want to reinstall it"
else
    # check vktm source dir
    if [ ! -d $AMRWIND_SRC_DIR ]; then
    # clone the source
    cd $SOFTWARE_SRC_DIR
    git clone --recursive $AMRWIND_REPO
    fi

    cd $AMRWIND_SRC_DIR
    git checkout Visualization_Performance_Study
    git submodule init
    git submodule update
    
    # there are some issues if we do not build the unit tests
    cmake -B ${AMRWIND_BUILD_DIR} -S ${AMRWIND_SRC_DIR} \
    -DCMAKE_BUILD_TYPE=Release \
    -DAMR_WIND_ENABLE_ASCENT=ON \
    -DAMR_WIND_ENABLE_MPI=ON \
    -DAMR_WIND_ENABLE_HYPRE:BOOL=OFF \
    -DAscent_DIR=${ASCENT_INSTALL_DIR}/lib/cmake/ascent \
    -DADIOS2_DIR=${ADIOS_INSTALL_DIR} \
    -DFides_DIR=${FIDES_INSTALL_DIR}/lib/cmake/fides \
    -DAMR_WIND_ENABLE_ADIOS2=ON \
    -DAMR_WIND_ENABLE_FIDES=ON \
    -DAMR_WIND_ENABLE_UNIT_TESTS=OFF \
    -DCMAKE_INSTALL_PREFIX=${AMRWIND_INSTALL_DIR} \
    -DAMR_WIND_ENABLE_CUDA=ON \
    -DCMAKE_CUDA_ARCHITECTURES=70 \
    -DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_COMPILER=gcc
    
    cd $HERE

    # build and install
    echo "**** Building ascent"
    cmake --build ${AMRWIND_BUILD_DIR} -j${build_jobs}

    echo "**** Installing ascent"
    cmake --install ${AMRWIND_BUILD_DIR}
fi
echo "====> Installing amr-wind, ok"


echo "====> Installing intransit reader"
INTRAN_READER_SRC_DIR="$SOFTWARE_SRC_DIR/in_transit_reader/visReader"
# use the install dir as the build dir
INTRAN_READER_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/in_transit_reader"

if [ -d $INTRAN_READER_INSTALL_DIR ]; then
    echo "====> skip, $INTRAN_READER_INSTALL_DIR already exists," \
             "please remove it if you want to reinstall it"
else
    # check vktm source dir
    if [ ! -d $INTRAN_READER_SRC_DIR ]; then
    # clone the source
    cd $SOFTWARE_SRC_DIR
    git clone --recursive $INTRANSIT_READER_REPO
    fi
    # use the master branch

    cmake -B ${INTRAN_READER_INSTALL_DIR} -S ${INTRAN_READER_SRC_DIR} \
    -DFides_DIR=${FIDES_INSTALL_DIR}/lib/cmake/fides \
    -DVTKm_DIR=${VTKM_INSTALL_DIR}/lib/cmake/vtkm-1.0 \
    -DVTKH_DIR=${VTKH_INSTALL_DIR} \
    -DADIOS2_DIR=${ADIOS_INSTALL_DIR}/lib64/cmake/adios2 \
    -DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_COMPILER=gcc
    
    cd $HERE

    # build and install
    echo "**** Building intransit reader"
    cmake --build ${INTRAN_READER_INSTALL_DIR} -j${build_jobs}
fi
echo "====> building intransit reader, ok"

echo "try to add library path by executing:"
echo "export LD_LIBRARY_PATH=\${LD_LIBRARY_PATH}:${VTKM_INSTALL_DIR}/lib:\
${ADIOS_INSTALL_DIR}/lib64:\
${FIDES_INSTALL_DIR}/lib:\
${ASCENT_INSTALL_DIR}/lib:\
${CONDUIT_INSTALL_DIR}/lib:\
${VTKH_INSTALL_DIR}/lib:\
${HDF5_INSTALL_DIR}/lib:\
/opt/cray/pe/gcc-libs/"
