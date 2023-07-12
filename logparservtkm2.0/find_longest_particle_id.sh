#!/bin/bash

#set -e
#set -x

DIRPATH=/gpfs/alpine/csc143/proj-shared/pugmire/forJay/VisPerfExp/ubuntu_cpu_vtkm2.0/runDIR/weak-weak-output3/

python3 parser_particles_finding.py 128 $DIRPATH/fusion.A.b128.n4.r128.B_p5000_s50/
echo " "
python3 parser_particles_finding.py 128 $DIRPATH/fusion.A.b128.n4.r128.B_p5000_s2000/
echo " "
python3 parser_particles_finding.py 128 $DIRPATH/astro.A.b128.n4.r128.B_p5000_s50/
echo " "
python3 parser_particles_finding.py 128 $DIRPATH/astro.A.b128.n4.r128.B_p5000_s2000/
echo " "
python3 parser_particles_finding.py 128 $DIRPATH/fishtank.A.b128.n4.r128.B_p5000_s50/
echo " "
python3 parser_particles_finding.py 128 $DIRPATH/fishtank.A.b128.n4.r128.B_p5000_s2000/
echo " "
python3 parser_particles_finding.py 128 $DIRPATH/clover.A.b128.n4.r128.B_p5000_s50/
echo " "
python3 parser_particles_finding.py 128 $DIRPATH/clover.A.b128.n4.r128.B_p5000_s2000/
echo " "
python3 parser_particles_finding.py 128 $DIRPATH/syn.A.b128.n4.r128.B_p5000_s50/
echo " "
python3 parser_particles_finding.py 128 $DIRPATH/syn.A.b128.n4.r128.B_p5000_s2000/
