set -e

#setting up necessary env on cori
HERE=`pwd`

build_jobs=8
source $HERE/settings.sh
SOFTWARE_SRC_DIR="$HERE/src"
SOFTWARE_BUILD_DIR="$HERE/build"
SOFTWARE_INSTALL_DIR="$HERE/install"

if [ ! -d $SOFTWARE_SRC_DIR ];
    then
    mkdir $SOFTWARE_SRC_DIR
fi
echo "SOFTWARE_SRC_DIR: $SOFTWARE_SRC_DIR"

if [ ! -d $SOFTWARE_BUILD_DIR ];
    then
    mkdir $SOFTWARE_BUILD_DIR
fi
echo "SOFTWARE_BUILD_DIR: $SOFTWARE_BUILD_DIR"

echo "====> Installing hdf5"
HDF5_SRC_DIR="$SOFTWARE_SRC_DIR/hdf5"
HDF5_BUILD_DIR="$SOFTWARE_BUILD_DIR/hdf5"
HDF5_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/hdf5"

if [ ! -d ${hdf5_src_dir} ]; then
  echo "**** Downloading hdf5-1.12.2.tar.gz "
  curl -L $HDF5_REPO -o hdf5-1.12.2.tar.gz 
  tar -xzf hdf5-1.12.2.tar.gz 
fi

echo "**** Configuring HDF5"
cmake -S $HDF5_SRC_DIR -B ${HDF5_BUILD_DIR} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=${HDF5_INSTALL_DIR}

echo "**** Building HDF5"
cmake --build ${HDF5_BUILD_DIR} -j${build_jobs}
echo "**** Installing HDF5"
cmake --install ${HDF5_INSTALL_DIR}


echo "====> Installing conduit"
CONDUIT_SRC_DIR="$SOFTWARE_SRC_DIR/conduit"
CONDUIT_BUILD_DIR="$SOFTWARE_BUILD_DIR/conduit"
CONDUIT_INSTALL_DIR="$SOFTWARE_INSTALL_DIR/conduit"

# TODO, make sure the hdf5 is installed here

# checking the existance of the conduit
if [ -d $CONDUIT_SRC_DIR ]; then
    echo "====> skip, $CONDUIT_SRC_DIR already exists," \
             "please remove it if you want to reinstall it"
else
    # clone and install by cmake
    cd $SOFTWARE_SRC_DIR
    curl -L CONDUIT_REPO -o conduit-v0.8.4-src-with-blt.tar.gz
    tar -xzf conduit-v0.8.4-src-with-blt.tar.gz
    
    # execute cmake
    cmake -B $CONDUIT_BUILD_DIR -S $CONDUIT_SRC_DIR \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=${CONDUIT_INSTALL_DIR} \
    -DENABLE_FORTRAN=ON \
    -DENABLE_MPI=ON \
    -DENABLE_PYTHON=OFF \
    -DENABLE_TESTS=${enable_tests} \
    -DHDF5_DIR=${hdf5_install_dir}
fi


echo "====> Installing vtk-m"
echo "====> Installing vtk-h"
echo "====> Installing adios"
echo "====> Installing fides"
echo "====> Installing ascent"
echo "====> Installing amr-wind"
