# the installing scripts only contains vtkh vtkm and visreader

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
    -DVTKm_ENABLE_OPENMP=OFF \
    -DVTKm_ENABLE_LOGGING=ON \
    -DVTKm_ENABLE_RENDERING=OFF \
    -DVTKm_ENABLE_TESTING=OFF 
    cmake --build ${VTKM_BUILD_DIR} -j${build_jobs}

    echo "**** Installing vtk-m"
    cmake --install ${VTKM_BUILD_DIR}
fi
echo "====> Installing vtk-m, ok"


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
    -DCMAKE_BUILD_TYPE=Release \
    -DVTKm_DIR=${VTKM_INSTALL_DIR}/lib/cmake/vtkm-2.0
    
    cd $HERE

    # build and install
    echo "**** Building intransit reader"
    cmake --build ${INTRAN_READER_INSTALL_DIR} -j${build_jobs}

echo "====> building intransit reader, ok"

# make sure the new added library path is located at the start 
echo "try to add library path by executing:"
echo "export LD_LIBRARY_PATH=${VTKM_INSTALL_DIR}/lib:\
${VTKH_INSTALL_DIR}/lib:${LD_LIBRARY_PATH}"
