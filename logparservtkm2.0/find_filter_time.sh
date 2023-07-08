#!/bin/bash

# get the current dir path and data dir path
HERE=`pwd`   
DATADIR=/gpfs/alpine/csc143/proj-shared/pugmire/forJay/VisPerfExp/ubuntu_cpu_vtkm2.0/runDIR/weak-weak-output3

# list data dir in the dedicated list
# assuming there are all kinds of dirs in the data dir
# otherwise, we need to use -d to decide if it is a dir
for d in $DATADIR/*/; do
    #use basename to cut out the last part of the dir
    baseDir="$(basename $d)"
    #the dir name is sth like this syn.A.b64.n2.r64.G_p1_s500
    #we choose the first part from it, the cut is always a good way
    #to cut things if string is in a standard way such as using . to split all strings
    DATASET="$(echo $baseDir | cut -d "." -f 1)"
   
    echo $DATASET         
    currdir="$HERE/$baseDir"

    # constructing commands used for executing
    args="parser_find_filter_time.py $d"
     
    # otherwise, we echo the command line
    # and execute associated python command based on it
    echo $args
    python3 $args
    
done