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
sample_rate=1000

def draw_dots_one_data(ax,procs,dirPath, data_name):
    all_particles=[]
    i=0
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        fo=open(file_name, "r")
        cycle_identifier ="s"+str(simSycle)
        
        for line in fo:
            line_strip=line.strip()

            #not the valide particle log
            if cycle_identifier not in line_strip:
                continue
            
            i=i+1
            split_str= line_strip.split(",")
            
            if(i%sample_rate!=0):
                continue
            #print(split_str)
            
            # id, lifetime/total execution time, traversed number of blocks, die reason
            # SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks,AccBO,AccEO,AccAdv,AccAllAdv,AccWait,AccWB,NumSteps,NumSmallSteps,AccGangSize,AccPrevGangSize
            alivetime = float(split_str[3])
            acc_group_size = float(split_str[14])
            traveled_blocks = float(split_str[5])
            usTos = 1000000
            particle=[alivetime/usTos, acc_group_size]
            all_particles.append(particle)
        fo.close()

    print("collected particle number:", len(all_particles))
    
    # sort particles from small to large
    # all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    # label the points on figure
    for p in all_particles:
        ax.scatter(p[0],p[1],s=8, c='blue', alpha=0.05)

    if data_name=="Tokamak":
        ax.set_ylabel('Accumulated group sizes', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])

    ax.tick_params(axis='x', labelsize=tickSize)
    ax.title.set_text(data_name)
    #ax.set_ylim(0,np.log10(10000000))
    ax.set_ylim(0,10000000)


# parse the timetrace log and draw the gantt chart
if __name__ == "__main__":
    
    if len(sys.argv)!=3:
        print("<binary> <procs> <dirpath for all data>")
        exit()

    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    simSycle=0
    dirPath=sys.argv[2]


    dataname=["fusion.A.b128.n4.r128.B_p5000_s2000_id582493",
              "astro.A.b128.n4.r128.B_p5000_s2000_id418463",
              "fishtank.A.b128.n4.r128.B_p5000_s2000_id625027",
              "clover.A.b128.n4.r128.B_p5000_s2000_id275499",
              "syn.A.b128.n4.r128.B_p5000_s2000_id365728"]

    official_name = ["Tokamak","Supernova","Hydraulics","CloverLeaf3D","Synthetic"]
   
    figsize_x = 6
    figsize_y = 5.5
    fig, axs = plt.subplots(nrows=1, ncols=5, figsize=(figsize_x*5,figsize_y)) 

    for index, data in enumerate(dataname):
        dirname_complete = dirPath+"/"+data
        print("dirname",dirname_complete,"index",index)
        draw_dots_one_data(axs[index],procs,dirname_complete, official_name[index])
    
    #fig.subplots_adjust(top=1.0)

    # legend_elem_1 = [Line2D([0], [0], marker='o', color='w', label='Out of bounds',
    #                     markerfacecolor='blue', markersize=legendsize),
    #                  Line2D([0], [2], marker='o', color='w', label='Zero velocity',
    #                     markerfacecolor='red', markersize=legendsize),
    #                  Line2D([0], [4], marker='o', color='w', label='Max step',
    #                     markerfacecolor='green', markersize=legendsize)]
    
    #fig.legend(handles=legend_elem_1, bbox_to_anchor=(0.62,1.08), ncol=3, fontsize=legendsize)
    fig.text(0.5, 0.0, 'Alive time of particle (second)', ha='center',fontsize=labelSize)
    fig.savefig("particles_all_dots_all_alivetime_groupsize.png",bbox_inches='tight')
    fig.savefig("particles_all_dots_all_alivetime_groupsize.pdf",bbox_inches='tight')

    #fig.savefig("particles_all_dots_all.png",bbox_inches='tight')
    #fig.savefig("particles_all_dots_all.pdf",bbox_inches='tight')



    