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


def search_particle(simSycleStr, procs, dirPath, particleId, ax):
    particle_path_list=[]
    for rank in range(0,procs,1):
            file_name = dirPath+"/particle_path."+str(rank)+".out"
            fo=open(file_name, "r")
        
            # go through all log entries
            for line in fo:
                line_strip=line.strip()
                split_str= line_strip.split(",")
                if(split_str[0]==simSycleStr and int(split_str[2])==particleId):
                    # advec step, alive time, current rank id
                    particle_path_list.append([int(split_str[3]),float(split_str[4]),int(split_str[1])])

            fo.close()
    
        #print(particle_path_list)
        #sort accoridng to advec step
    particle_path_list=sorted(particle_path_list, key=lambda x: x[0]) 
    particle_blockid=[]
    particle_advectstep=[]

    for p in particle_path_list:
        particle_advectstep.append(p[0])
        particle_blockid.append(p[2])


    #print(particle_advectstep)
    print(particle_blockid)
    #y is block id
    #x is advec step
    ax.plot(particle_advectstep,particle_blockid)


# parse the counter file
# x axis represents the rank value
# y axis represents the total number of particles processes by this rank 
# (the particle id is not unique)
if __name__ == "__main__":
    
    if len(sys.argv)!=3:
        print("<binary> <procs> <dirpath>")
        exit()

    procs=int(sys.argv[1])
    dirPath=sys.argv[2]

    simSycle=0
    simSycleStr = "s"+str(simSycle)

    # generating particle id
    particle_id_list=[*range(100, 200, 1)]
    
    print(particle_id_list)

    fig, ax = plt.subplots()
    #for p_id in particle_id_list:
    #    search_particle(simSycleStr,procs,dirPath,p_id,ax)
    
    search_particle(simSycleStr,procs,dirPath,275499,ax)
    

    ax.set_xlabel('Time(ms)', fontsize='large')
    ax.set_ylabel('Block (Rank) id', fontsize='large') 
    fig.savefig("parser_particles_path_blocks.png",bbox_inches='tight')

    

