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
import matplotlib.colors as colors

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
    
    ## This is for another figure that use the number of particles as y axis
    number_bin = 10
    bin_length = 1.0/(1.0*number_bin)
    bin_list_oob = [0]*number_bin
    bin_list_zero = [0]*number_bin
    bin_list_maxstep = [0]*number_bin
    
    max_num_traversed = 0
    
    all_particles_ratio_oob=[]
    all_particles_num_traverse_oob=[]
    all_particles_ratio_zero=[]
    all_particles_num_traverse_zero=[]
    all_particles_ratio_maxstep=[]
    all_particles_num_traverse_maxstep=[]

    max_ratio=0
    max_pid=0
    max_num_traversed_blocks=0

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
                ratio = float(split_str[3])/filter_time
                #particle=[int(split_str[1]),ratio,int(split_str[5]),split_str[2]]
                reason = split_str[2]
                if max_num_traversed_blocks<int(split_str[5]):
                    max_num_traversed_blocks = max(max_num_traversed_blocks,int(split_str[5]))
                    #print(split_str)
                if(max_ratio<ratio):
                    max_ratio = max(max_ratio,ratio)
                    max_pid = split_str[1]
                if reason == 'b':
                    all_particles_ratio_oob.append(ratio)
                    all_particles_num_traverse_oob.append(int(split_str[5]))
                elif reason == 'z':
                    all_particles_ratio_zero.append(ratio)
                    all_particles_num_traverse_zero.append(int(split_str[5]))
                else:
                    all_particles_ratio_maxstep.append(ratio)
                    all_particles_num_traverse_maxstep.append(int(split_str[5]))

        fo.close()
    print(len(all_particles_ratio_oob),len(all_particles_ratio_zero),len(all_particles_ratio_maxstep))
    print("collected particle number :", len(all_particles_ratio_oob)+len(all_particles_ratio_zero)+len(all_particles_ratio_maxstep))
    print("max_num_traversed_blocks",max_num_traversed_blocks)
    # for historgram drawing giving more space
    max_y=max_num_traversed_blocks+20

    nbin_x=100
    nbin_y=100
    
    fig, ax = plt.subplots()
    
    ax.set_xlabel('Particle lifeTime/Filter execution time', fontsize='large')
    ax.set_ylabel('Number of traveded blocks', fontsize='large')


    plt.hist2d(all_particles_ratio_maxstep,
                all_particles_num_traverse_maxstep,
                cmin=1,
                bins=(nbin_x, nbin_y),
                range=[[0,1.0],[0,max_y]],
                norm=colors.LogNorm(1, len(all_particles_ratio_maxstep)),
                cmap='Greens')

    plt.hist2d(all_particles_ratio_oob,
                all_particles_num_traverse_oob,
                cmin=1,
                bins=(nbin_x, nbin_y),
                range=[[0,1],[0,max_y]],
                norm=colors.LogNorm(1, len(all_particles_ratio_maxstep)),
                cmap='Blues')
    
    
    plt.hist2d(all_particles_ratio_zero,
                all_particles_num_traverse_zero,
                cmin=1,
                bins=(nbin_x, nbin_y),
                range=[[0,1],[0,max_y]],
                norm=colors.LogNorm(1, len(all_particles_ratio_zero)),
                cmap='Reds')


    
    legend_elem_1 = [Patch(label='Out of bounds (Background color)',
                        facecolor='blue', alpha=0.6),
                     Patch(label='Zero velocity (Background color)',
                        facecolor='red', alpha=0.6),
                     Patch(label='Max step (Background color)',
                        facecolor='green', alpha=0.6)]

    legend1 = plt.legend(handles=legend_elem_1, loc='upper right', ncol=1, fontsize=9)


    fig.savefig("particles_histogram2d_"+dirname+".png", bbox_inches='tight')

    print("max_ratio", max_ratio, "max_pid", max_pid)