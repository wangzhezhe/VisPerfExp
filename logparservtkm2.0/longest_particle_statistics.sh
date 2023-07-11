#!/bin/bash

DIRPATH=/gpfs/alpine/csc143/proj-shared/pugmire/forJay/VisPerfExp/ubuntu_cpu_vtkm2.0/runDIR/weak-weak-output3/

#max_alive_id 95361 max_alive_id_traversed_blocks 7
python3 parser_particles_all_statistics.py 128 $DIRPATH/fusion.A.b128.n4.r128.B_p5000_s50/ 95361
#max_alive_id 540040 max_alive_id_traversed_blocks 127
echo "\n"
python3 parser_particles_all_statistics.py 128 $DIRPATH/fusion.A.b128.n4.r128.B_p5000_s2000/ 540040
echo "\n"


#max_alive_id 250661 max_alive_id_traversed_blocks 7
python3 parser_particles_all_statistics.py 128 $DIRPATH/astro.A.b128.n4.r128.B_p5000_s50/ 250661
echo "\n"
#max_alive_id 89999 max_alive_id_traversed_blocks 239
python3 parser_particles_all_statistics.py 128 $DIRPATH/astro.A.b128.n4.r128.B_p5000_s2000/ 89999
echo "\n"
#max_alive_id 588148 max_alive_id_traversed_blocks 17
python3 parser_particles_all_statistics.py 128 $DIRPATH/fishtank.A.b128.n4.r128.B_p5000_s50/ 588148
echo "\n"
#max_alive_id 625027 max_alive_id_traversed_blocks 213
python3 parser_particles_all_statistics.py 128 $DIRPATH/fishtank.A.b128.n4.r128.B_p5000_s2000/ 625027
echo "\n"
#max_alive_id 265253 max_alive_id_traversed_blocks 11
python3 parser_particles_all_statistics.py 128 $DIRPATH/clover.A.b128.n4.r128.B_p5000_s50/ 265253
echo "\n"
#max_alive_id 110861 max_alive_id_traversed_blocks 184
python3 parser_particles_all_statistics.py 128 $DIRPATH/clover.A.b128.n4.r128.B_p5000_s2000/ 110861
echo "\n"
#max_alive_id 440056 max_alive_id_traversed_blocks 7
python3 parser_particles_all_statistics.py 128 $DIRPATH/syn.A.b128.n4.r128.B_p5000_s50/ 440056
echo "\n"
#max_alive_id 400556 max_alive_id_traversed_blocks 192
python3 parser_particles_all_statistics.py 128 $DIRPATH/syn.A.b128.n4.r128.B_p5000_s2000/ 400556

