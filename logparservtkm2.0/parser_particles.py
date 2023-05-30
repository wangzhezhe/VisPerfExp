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

# parse the timetrace log and draw the gantt chart
if __name__ == "__main__":
    
    if len(sys.argv)!=3:
        print("<binary> <procs> <dirpath>")
        exit()

    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    simSycle=0
    dirPath=sys.argv[2]

    # get total exeuction time
    filter_start="FilterStart_"+str(simSycle)+" "
    filter_end="FilterEnd_"+str(simSycle)+" "
    
    file_name = dirPath+"/timetrace."+str(0)+".out"
    fo=open(file_name, "r")
    for line in fo:
        line_strip=line.strip()
        split_str= line_strip.split(" ")
        if filter_start in line_strip:
            filter_start_time = float(split_str[1])       
        if filter_end in line_strip:
            filter_end_time = float(split_str[1])
    fo.close()

    filter_time = filter_end_time-filter_start_time

    print("filter execution time is", filter_time)

    
    # go through each particle files
    # each particle, store id, life time, traversed blocks number, die reason
    all_particles=[]
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        print(file_name)

        fo=open(file_name, "r")

        cycle_identifier ="s"+str(simSycle)
       
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")
            #print(split_str)
            if cycle_identifier in line_strip:
                # id, lifetime/total execution time, traversed number of blocks, die reason
                particle=[int(split_str[1]),float(split_str[3])/filter_time,float(split_str[5]),split_str[2]]
                all_particles.append(particle)
        
        fo.close()

    print("collected particle number:", len(all_particles))

    # go through each particle and draw them on a 2d plot with color
    figsize_x = 8
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_x)) 
    psize = 15

    ax.set_xlabel('Particle lifeTime/Filter execution time', fontsize='large')
    ax.set_ylabel('Number of traveded blocks', fontsize='large')



    for p in all_particles:
        if p[3]=='b':
            plt.scatter(p[1],p[2],s=psize, c='blue')
           
        elif p[3]=='z':
            plt.scatter(p[1],p[2],s=psize,c='red')
        else:
            plt.scatter(p[1],p[2],s=psize,c='green')


    legend_elem_1 = [Line2D([0], [0], marker='o', color='w', label='Out of bounds',
                        markerfacecolor='blue', markersize=8),
                     Line2D([0], [2], marker='o', color='w', label='Zero velocity',
                        markerfacecolor='red', markersize=8),
                     Line2D([0], [4], marker='o', color='w', label='Max step',
                        markerfacecolor='green', markersize=8)]

    legend1 = plt.legend(handles=legend_elem_1, loc='upper center', ncol=3, fontsize=12)

    fig.savefig("particles.png",bbox_inches='tight')