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

    total_number_particles=[0]*procs
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        fo=open(file_name, "r")

        # go through all log entries
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")
            # the first sim sycle
            if split_str[0]=='s0':
                #print(split_str)
                total_number_particles[rank]=total_number_particles[rank]+1
        fo.close()

    print(total_number_particles)

    fig, ax = plt.subplots()

    ind = np.arange(procs)

    #ax.set_xticks([0,2,4,6])
    #ax.set_xticklabels(['zero','two','four','six'])

    ax.set_xlabel('Index of rank', fontsize='large')
    ax.set_ylabel('Total number of particles per rank', fontsize='large')   
    p = ax.bar(ind,total_number_particles,color='blue',alpha=0.8)
    fig.savefig("particles_total_number_per_rank.png",bbox_inches='tight')

