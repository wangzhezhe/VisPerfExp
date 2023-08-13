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



def get_particle_list_sorted(data_dir, particle_id):

    procs = 128
    step = 0
    
    particle_list=[]
    comm_start_list=[]
    comm_time_list=[]
    actual_comm_list=[]
    send_end_list=[]

    advect_start_time=0
    advect_step_before=0
    advect_steps_whole=0
    advect_steps_whole=0
    
    for proc in range(0,procs,1):
        file_name = data_dir+"particle_tracing_details."+str(proc)+".out"
        #print(file_name)
        fo=open(file_name, "r")
        
        advect_start_time=0
        advect_step_before=0
        advect_steps_whole=0
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")
                   
            # Event,SimCycle,BlockID(RankId),ParticleID,CurrTime,AdvectedSteps,ParticleNum,PrevParticleNum
            if str(step)==split_str[1] :
                #print(split_str)
                if split_str[0]=="WORKLET_Start":
                    advect_start_time=float(split_str[4])
                    advect_step_before=float(split_str[5])
                if split_str[0]=="WORKLET_End":
                    advect_end_time=float(split_str[4])
                    advect_step_after=float(split_str[5])
                    blockid = int(split_str[2])
                    pnum = int(split_str[6])
                    # start time, end time, advec steps, blockid
                    advect_steps_whole=advect_steps_whole+advect_step_after-advect_step_before
                    particle_list.append([advect_start_time,advect_end_time,advect_step_after-advect_step_before,blockid,pnum])

                if split_str[0]=="GANG_COMM_START":
                    comm_start_time=float(split_str[4])
                    #print("comm_start_time",comm_start_time)
                    comm_start_list.append(comm_start_time)
                if split_str[0]=="GANG_COMM_END":
                    comm_end_time=float(split_str[4])
                    comm_time_list.append((comm_start_time,comm_end_time-comm_start_time))
                    actual_comm_list.append(comm_end_time-comm_start_time)
                    send_end_list.append(comm_end_time)


    #sorting all particle list
    #print(particle_list)
    particle_list_sorted=sorted(particle_list, key=lambda x: x[0])
    return particle_list_sorted


if __name__ == "__main__":

    # dataset dir and id
    
    syn_dir="/gpfs/alpine/scratch/zw241/csc143/weak-weak-output4/syn.A.b128.n4.r128.B_p5000_s2000_id365728/"
    syn_id="365728"
    
    clover_dir="/gpfs/alpine/scratch/zw241/csc143/weak-weak-output4/clover.A.b128.n4.r128.B_p5000_s2000_id275499/"
    clover_id="275499"
    
    fishtank_dir="/gpfs/alpine/scratch/zw241/csc143/weak-weak-output4/fishtank.A.b128.n4.r128.B_p5000_s2000_id588164/"
    fishtank_id="588164"

    supernova_dir="/gpfs/alpine/scratch/zw241/csc143/weak-weak-output4/astro.A.b128.n4.r128.B_p5000_s2000_id208001/"
    supernova_id="208001"

    fusion_dir="/gpfs/alpine/scratch/zw241/csc143/weak-weak-output4/fusion.A.b128.n4.r128.B_p5000_s2000_id582493/"
    fusion_id="582493"

    dataset_dir=[syn_dir,clover_dir,fishtank_dir,supernova_dir,fusion_dir]
    particle_id=[syn_id,clover_id,fishtank_id,supernova_id,fusion_id]


    particle_list_sorted_all=[]
    max_particle_live_time=0

    for dir_id_pair in zip(dataset_dir,particle_id):
        print(dir_id_pair[0],dir_id_pair[1])
        #draw figure using one x axis and y axis
        #figure out the longest filter execution time
        # get advect_bar
        # get blockid_list
        particle_list_sorted = get_particle_list_sorted(dir_id_pair[0],dir_id_pair[1])
        particle_list_sorted_all.append(particle_list_sorted)
        #print(particle_list_sorted)
        print("long particle time", particle_list_sorted[-1][1])
        max_particle_live_time=max(max_particle_live_time,particle_list_sorted[-1][1])

    
    # make sure the x coordinates 
    # then draw each bar separately
    figsize_x=8
    bar_height=0.6
    figsize_y=bar_height*5+0.5
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))
    print("max_particle_live_time",max_particle_live_time)
    plt.xticks([0,figsize_x/4,figsize_x/2,3*figsize_x/4,figsize_x], [0,round(max_particle_live_time/4,2),round(max_particle_live_time/2,2), round(3*max_particle_live_time/4,2),round(max_particle_live_time,2)])
    plt.yticks(bar_height*np.array(list(range(0, 5, 1)))+0.5*bar_height-0.05,["Synthetic","CloverLeaf3D","Hydraulics","Supernova","Tokamak"])
    ax.set_xlabel('Time(ms)', fontsize='large')

    for data_index in range(0,5,1):
        # get advection time
        advected_bar=[]
        blockid_list=[]
        advect_whole=0
        for p in particle_list_sorted_all[data_index]:
            #compute the width of each bar
            advect_spent_time=p[1]-p[0]
            width = (1.0*advect_spent_time)/(1.0*max_particle_live_time)

            # use start position
            advected_bar.append((figsize_x*(p[0]*1.0/max_particle_live_time),width*figsize_x))
            blockid_list.append(p[3])

        # compute color map
        block_list_set = set(blockid_list)
        distinct_block_ids = len(block_list_set)
    
        print("distinct_block_ids len",distinct_block_ids)
        print("distinct block ids set", block_list_set)

        #colors = plt.cm.jet(np.linspace(0,1,distinct_block_ids))
        colors = plt.cm.viridis(np.linspace(0,1,distinct_block_ids))

        #map block id to 0-distinct_block_ids-1
        colordic={}
        #key is the block id
        #val is the color id from 0 to distinct_block_ids-1
        block_index = 0
        for _, val in enumerate(blockid_list):
            # if key exist, continue
            if val in colordic.keys():
                continue
            else:    
            # if key not exist, create a new pair, index++
                colordic[val]=block_index
                block_index=block_index+1
        
        color_list=[]
        # go through each value in the block id list
        # find a uniq color for it
        for id,val in enumerate(blockid_list):
            #print(id, val)
            color_list.append(colors[colordic[val]])
        

        ax.broken_barh(xranges=advected_bar,yrange=(bar_height*data_index,bar_height-0.1),color=color_list,edgecolor="none")


    fig.savefig("particle_gantt_five_datasets.png",bbox_inches='tight')