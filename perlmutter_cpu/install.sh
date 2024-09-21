#!/bin/bash

set -e
HERE=`pwd`
build_jobs=6
source $HERE/../settings.sh
SOFTWARE_SRC_DIR="$HERE/src"
SOFTWARE_BUILD_DIR="$HERE/build"
SOFTWARE_INSTALL_DIR="$HERE/install"

if [ ! -d $SOFTWARE_SRC_DIR ];
    then
    mkdir $SOFTWARE_SRC_DIR
fi
echo "SOFTWARE_SRC_DIR: $SOFTWARE_SRC_DIR"


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
    git clone -b vtkm_trace $VTKM_REPO
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
    -DVTKm_ENABLE_OPENMP=ON \
    -DVTKm_ENABLE_LOGGING=ON \
    -DVTKm_ENABLE_RENDERING=OFF \
    -DVTKm_ENABLE_TESTING=OFF 
    cmake --build ${VTKM_BUILD_DIR} -j${build_jobs}

    echo "**** Installing vtk-m"
    cmake --install ${VTKM_BUILD_DIR}
fi
echo "====> Installing vtk-m, ok"


# build and install vtk
echo "====> Installing vtk"

VTK_SRC_DIR="$SOFTWARE_SRC_DIR/vtk"
VTK_BUILD_DIR="$SOFTWARE_BUILD_DIR/vtk"
VTK_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/vtk"

# check the install dir
if [ -d $VTK_INSTALL_DIR ]; then
    echo "====> skip, $VTK_INSTALL_DIR already exists," \
             "please remove it if you want to reinstall it"
else
    echo $VTK_SRC_DIR
    echo $VTK_BUILD_DIR
    echo $VTK_INSTALL_DIR

    if [ ! -d $VTK_SRC_DIR ]; then
    # clone the source
    cd $SOFTWARE_SRC_DIR
    git clone -b master $VTK_REPO
    fi

    # do not use vtkm under the vtk repo
    # use external vtkm
    cmake -B ${VTK_BUILD_DIR} -S ${VTK_SRC_DIR} \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DVTK_USE_MPI=ON \
    -DCMAKE_INSTALL_PREFIX=${VTK_INSTALL_DIR}

    cd $HERE

    # build and install
    echo "**** Building vtk"
    mkdir -p ${VTK_BUILD_DIR}
    cmake --build ${VTK_BUILD_DIR} -j${build_jobs}
    cmake --install ${VTK_BUILD_DIR}
fi


echo "====> Installing intransit reader"
INTRAN_READER_SRC_DIR="$SOFTWARE_SRC_DIR/visReader"
# use the install dir as the build dir
INTRAN_READER_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/visReader"


    # check vktm source dir
    if [ ! -d $INTRAN_READER_SRC_DIR ]; then
    # clone the source
    cd $SOFTWARE_SRC_DIR
    git clone -b use_latest_vtkm $INTRANSIT_READER_REPO

    fi
    # use the master branch

    cmake -B ${INTRAN_READER_INSTALL_DIR} -S ${INTRAN_READER_SRC_DIR} \
    -DCMAKE_BUILD_TYPE=Release -DVTKm_DIR=${VTKM_INSTALL_DIR}/lib/cmake/vtkm-2.0 \

    cd $HERE

    # build and install
    echo "**** Building intransit reader"
    cmake --build ${INTRAN_READER_INSTALL_DIR} -j${build_jobs}

echo "====> building intransit reader, ok"


echo "====> Installing loosely coupled workflow"
# set up spack env
cd $PSCRATCH
. /pscratch/sd/z/zw241/zw241/spack/share/spack/setup-env.sh
spack env activate mochi-env
# go to workflow dir
WF_SRC_DIR="$SOFTWARE_SRC_DIR/visReader/looselyworkflow"
WF_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/visReader/looselyworkflow"

mkdir -p ${WF_INSTALL_DIR}


cmake -B ${WF_INSTALL_DIR} -S ${WF_SRC_DIR} -DCMAKE_BUILD_TYPE=Release -DVTKm_DIR=${VTKM_INSTALL_DIR}/lib/cmake/vtkm-2.0 -DVTK_DIR=${VTK_INSTALL_DIR}/lib64/cmake/vtk-9.3 

cmake --build ${WF_INSTALL_DIR} -j${build_jobs}
spack env deactivate


# make sure the new added library path is located at the start
echo "try to add library path by executing:"
echo "export LD_LIBRARY_PATH=${VTKM_INSTALL_DIR}/lib:\
${VTKH_INSTALL_DIR}/lib:${LD_LIBRARY_PATH}"
