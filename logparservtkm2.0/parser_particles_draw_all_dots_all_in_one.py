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

labelSize = 23
tickSize = 23
legendsize=21

def draw_dots_one_data(ax,procs,dirPath, data_name):

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

    ax.tick_params(axis='y', labelsize=tickSize)
    ax.tick_params(axis='x', labelsize=tickSize)
    #ax.set_xlabel(data_name, fontsize=labelSize)

    ax.title.set_text(data_name)
    ax.title.set_fontsize(labelSize)

    if "fusion" in dirPath:
        ax.set_ylabel('Number of traveded blocks', fontsize=labelSize)
    else:
        ax.set_yticks([])

    ax.set_ylim(0,400)
    # the size of particle should reflect actual particle numbers
    #scale = 0.5
    #bin_list_oob_avg = sum(bin_list_oob)/len(bin_list_oob)
    ax.set_aspect('auto')

    for p in all_particles:
        #psize = 200.0*(p[4]/max_gang_size)
        psize = pow(1.8,12*p[4]/max_gang_size)
        #print(psize)
        # compute psize
        if p[3]=='b':
            #bin_index= int(p[1]/bin_length)
            #psize = psize*scale*bin_list_oob[bin_index]/bin_list_oob_avg
            ax.scatter(p[1],p[2],s=psize, c='blue', alpha=0.05)
        elif p[3]=='z':
            ax.scatter(p[1],p[2],s=psize,c='red', alpha=0.05)
        else:
            ax.scatter(p[1],p[2],s=psize,c='green', alpha=0.05)


# parse the timetrace log and draw the gantt chart
if __name__ == "__main__":
    
    if len(sys.argv)!=3:
        print("<binary> <procs> <dirpath for all data>")
        exit()

    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    simSycle=0
    dirPath=sys.argv[2]


    dataname=["fusion.A.b128.n4.r128.B_p5000_s2000",
              "astro.A.b128.n4.r128.B_p5000_s2000",
              "fishtank.A.b128.n4.r128.B_p5000_s2000_id625027",
              "clover.A.b128.n4.r128.B_p5000_s2000",
              "syn.A.b128.n4.r128.B_p5000_s2000"]

    official_name = ["Tokamak","Supernova","Hydraulics","CloverLeaf3D","Synthetic"]
   
    figsize_x = 6
    figsize_y = 5.5
    fig, axs = plt.subplots(nrows=1, ncols=5, figsize=(figsize_x*5,figsize_y)) 

    for index, data in enumerate(dataname):
        dirname_complete = dirPath+"/"+data
        print("dirname",dirname_complete,"index",index)
        draw_dots_one_data(axs[index],procs,dirname_complete, official_name[index])
    
    #fig.subplots_adjust(top=1.0)

    legend_elem_1 = [Line2D([0], [0], marker='o', color='w', label='Out of bounds',
                        facecolor='blue', markersize=legendsize),
                     Line2D([0], [2], marker='o', color='w', label='Zero velocity',
                        facecolor='red', markersize=legendsize),
                     Line2D([0], [4], marker='o', color='w', label='Max step',
                        facecolor='green', markersize=legendsize)]
    
    fig.legend(handles=legend_elem_1, bbox_to_anchor=(0.62,1.08), ncol=3, fontsize=legendsize)
    fig.text(0.5, 0.0, 'Particle life time/Filter execution time', ha='center',fontsize=labelSize)
    fig.savefig("particles_all_dots_all.png",bbox_inches='tight')
    fig.savefig("particles_all_dots_all.pdf",bbox_inches='tight')

    #fig.savefig("particles_all_dots_all.png",bbox_inches='tight')
    #fig.savefig("particles_all_dots_all.pdf",bbox_inches='tight')



    