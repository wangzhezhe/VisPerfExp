from os import system
from os.path import exists
import sys
import math
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

    dirname = dirPath.split("/")[-2]
    print("dirname",dirname)

    # extract largest total exeuction time
    filter_start="FilterStart_"+str(simSycle)+" "
    filter_end="FilterEnd_"+str(simSycle)+" "
    
    for rank in range(0,procs,1):
        file_name = dirPath+"/timetrace."+str(rank)+".out"
        fo=open(file_name, "r")
        max_filter_time=0
        filter_time=0
        filter_start_time=0
        filter_end_time=0
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(" ")
            if filter_start in line_strip:
                filter_start_time = float(split_str[1])       
            if filter_end in line_strip:
                filter_end_time = float(split_str[1])
            filter_time = filter_end_time-filter_start_time
            max_filter_time = max(max_filter_time,filter_time)
        fo.close()
    
    print("filter execution time is", max_filter_time)

    # go through each particle files
    # each particle, store id, life time, traversed blocks number, die reason

    all_particles=[]
    max_gang_size=0.0
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        print(file_name)

        fo=open(file_name, "r")

        cycle_identifier ="s"+str(simSycle)

        i=0
        for line in fo:
            i=i+1
            line_strip=line.strip()
            split_str= line_strip.split(",")
            if(i%200!=0):
                continue
            #print(split_str)
            if cycle_identifier in line_strip:
                # id, lifetime/total execution time, traversed number of blocks, die reason
                # SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks,AccBO,AccEO,AccAdv,AccAllAdv,AccWait,AccWB,NumSteps,NumSmallSteps,AccGangSize,AccPrevGangSize

                ratio = float(split_str[3])/filter_time
                gang_size=float(split_str[14])
                if(gang_size>max_gang_size):
                    max_gang_size=gang_size
                particle=[int(split_str[1]),ratio,float(split_str[5]),split_str[2],gang_size]
                all_particles.append(particle)
        fo.close()

    print("collected particle number:", len(all_particles), "max gang size ", max_gang_size)

    # go through each particle and draw them on a 2d plot with color
    figsize_x = 8
    figsize_y = 7
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y)) 
    
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    ax.set_xlabel('Particle lifeTime/Filter execution time', fontsize=16)
    ax.set_ylabel('Number of traveded blocks', fontsize=16)
    ax.set_ylim(0,400)
    # the size of particle should reflect actual particle numbers
    #scale = 0.5
    #bin_list_oob_avg = sum(bin_list_oob)/len(bin_list_oob)

    for p in all_particles:
        #psize = 200.0*(p[4]/max_gang_size)
        psize = pow(1.8,12*p[4]/max_gang_size)
        #print(psize)
        # compute psize
        if p[3]=='b':
            #bin_index= int(p[1]/bin_length)
            #psize = psize*scale*bin_list_oob[bin_index]/bin_list_oob_avg
            plt.scatter(p[1],p[2],s=psize, c='blue', alpha=0.02)
        elif p[3]=='z':
            plt.scatter(p[1],p[2],s=psize,c='red', alpha=0.02)
        else:
            plt.scatter(p[1],p[2],s=psize,c='green', alpha=0.02)


    legend_elem_1 = [Line2D([0], [0], marker='o', color='w', label='Out of bounds',
                        markerfacecolor='blue', markersize=18),
                     Line2D([0], [2], marker='o', color='w', label='Zero velocity',
                        markerfacecolor='red', markersize=18),
                     Line2D([0], [4], marker='o', color='w', label='Max step',
                        markerfacecolor='green', markersize=18)]

    legend1 = plt.legend(handles=legend_elem_1, loc='upper center', ncol=3, fontsize=12)

    fig.savefig("particles_all_dots_"+dirname+".png",bbox_inches='tight')

    