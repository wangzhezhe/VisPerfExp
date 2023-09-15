from os import system
from os.path import exists
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import ticker
import statistics
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# go through particle file which records all necessary information when a particle terminates
# finding one that satisfies specific constraints
# max execution time
# or ids statyin in specific executionime-#traversing block region
if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("<binary> <procs> <dirpath>")
        exit()

    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    simSycle=0
    dirPath=sys.argv[2]

    dirname = dirPath.split("/")[-2]
    print("dirname:",dirname)
    
    particle_send_begin=0
    particle_send_end=0
    particle_send_acc=0
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle_tracing_details."+str(rank)+".out"
        #print(file_name)

        fo=open(file_name, "r")
        
        #SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")
            if split_str[0]=="ParticleSendBegin":
                particle_send_begin=int(split_str[4])

            if split_str[0]=="ParticleSendEnd":
                particle_send_end=int(split_str[4])
                particle_send_acc=particle_send_acc+(particle_send_end-particle_send_begin)
                #print(particle_send_end,particle_send_begin)

        
    
    print("particle_send_acc",particle_send_acc)