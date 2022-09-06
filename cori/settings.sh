#!/bin/bash

$HDF5_REPO=https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.2/src/hdf5-1.12.2.tar.gz
$CONDUIT_REPO=https://github.com/LLNL/conduit/releases/download/v0.8.4/conduit-v0.8.4-src-with-blt.tar.gz




vtk-m
git clone hxxps://gitlab.kitware.com/jameskress/vtk-m.git
git checkout 2021-performanceStudy
 
conduit
git clone --recursive hxxps://github.com/LLNL/conduit.git
 
fides
git clone  hxxps://gitlab.kitware.com/jameskress/fides.git
git checkout 2021_performanceStudy

adios2
eac152529d4d70470bd79a2319119eacd91ae3b2
git clone hxxps://github.com/ornladios/ADIOS2.git

vtk-h
git clone --recursive hxxps://github.com/jameskress/vtk-h.git
git checkout 2021-performanceStudy

 (important, otherwise there are vtkm issue)
git submodule init
git submodule update

ascent
git clone --recursive hxxps://github.com/jameskress/ascent.git
cd ascent
git checkout performanceStudy

My forked repo (added timer and debug message)
https://github.com/wangzhezhe/ascent/tree/performanceStudy
 
cheetah
git clone hxxps://github.com/CODARcode/cheetah.git
 
amr-wind
git clone hxxps://github.com/jameskress/amr-wind.git
git checkout Visualization_Performance_Study
git submodule init
git submodule update
