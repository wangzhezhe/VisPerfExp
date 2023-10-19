#!/bin/bash

cp assign_options.config /home/zw/cworkspace/VisPerfExp/ubuntu_cpu_vtkm2.0/expscripts/

cd /home/zw/cworkspace/VisPerfExp/ubuntu_cpu_vtkm2.0/expscripts/

/bin/bash visreader_test_astro.sh &>log.temp

