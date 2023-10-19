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
import math

def get_barh_other_overhead(barh_list_advec, barh_list_comm):
    barh_list_other_overhead=[]
    #print("barh_list_advec",barh_list_advec[0:10])
    #print("barh_list_comm",barh_list_comm[0:10])
    # two pointer i, j
    i=0
    j=0
    
    last_bar_end=0
    curr_bar_star=0
    print("len(barh_list_advec)",len(barh_list_advec),"len(barh_list_comm)",len(barh_list_comm))

    while(i<len(barh_list_advec) and j<len(barh_list_comm)):
        #print("debug i, j",i,j)
        if i==0 and j==0:
            last_bar_end=0
        #if i==203 and j==202:
        #   print("debug", barh_list_advec[i],barh_list_comm[j])
        #   exit(0)
    
        curr_bar_star=min(barh_list_advec[i][0],barh_list_comm[j][0])
        barh_list_other_overhead.append((last_bar_end,curr_bar_star-last_bar_end))
     
        # move i j and update last bar end position 
        if barh_list_advec[i][0]+barh_list_advec[i][1] < barh_list_comm[j][0] or (math.fabs(barh_list_advec[i][0]+barh_list_advec[i][1]- barh_list_comm[j][0])<0.000001):
            last_bar_end = barh_list_advec[i][0]+barh_list_advec[i][1]
            i=i+1
            continue
        elif barh_list_comm[j][0]+barh_list_comm[j][1] < barh_list_advec[i][0] or (math.fabs(barh_list_comm[j][0]+barh_list_comm[j][1] - barh_list_advec[i][0])<0.000001):
            last_bar_end = barh_list_comm[j][0]+barh_list_comm[j][1]
            j=j+1
            continue
        else:
            print("debug issue data", barh_list_advec[i],barh_list_comm[j])
            i+=1
            j+=1
            continue
        
    # when either i and j end, put last one
    while i<len(barh_list_advec):
        curr_bar_start=barh_list_advec[i][0]
        barh_list_other_overhead.append((last_bar_end,curr_bar_start-last_bar_end))
        last_bar_end=curr_bar_start+barh_list_advec[i][1]
        i+=1


    while j<len(barh_list_comm):
        curr_bar_start=barh_list_comm[j][0]
        last_bar_end=curr_bar_start+barh_list_comm[j][1]
        barh_list_other_overhead.append((last_bar_end,curr_bar_start-last_bar_end))
        j+=1


    return barh_list_other_overhead

def get_particle_list_sorted(data_dir, particle_id):

    procs = 128
    step = 0
    
    particle_path=[]
    comm_start_list=[]
    comm_time_list=[]
    actual_comm_list=[]
    send_end_list=[]

    advect_start_time=0
    advect_step_before=0
    advect_steps_whole=0
    advect_steps_whole=0
    blockid=0
    for proc in range(0,procs,1):
        file_name = data_dir+"particle_tracing_details."+str(proc)+".out"
        #print(file_name)
        fo=open(file_name, "r")
        
        advect_start_time=0
        advect_end_time=0
        advect_step_before=0
        advect_steps_whole=0
        recvok_time=0
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")
                   
            # Event,SimCycle,BlockID(RankId),ParticleID,CurrTime,AdvectedSteps,ParticleNum,PrevParticleNum
            if str(step)==split_str[1] :
                #print(split_str)
                if split_str[0]=="RECVOK":
                    recvok_time=float(split_str[4])
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

                if split_str[0]=="GANG_COMM_START":
                    comm_start_time=float(split_str[4])
                    #print("comm_start_time",comm_start_time)
                    comm_start_list.append(comm_start_time)
                if split_str[0]=="GANG_COMM_END":
                    comm_end_time=float(split_str[4])
                    comm_time_list.append((comm_start_time,comm_end_time-comm_start_time))
                    actual_comm_list.append(comm_end_time-comm_start_time)
                    send_end_list.append(comm_end_time)
                    # put one path into the path list once the gang comm end
                    #print([recvok_time,advect_start_time,advect_end_time,comm_start_time,blockid])
                    particle_path.append([recvok_time,advect_start_time,advect_end_time,comm_start_time,blockid,comm_end_time])

    #sorting all particle list
    #print(particle_list)
    particle_path_sorted=sorted(particle_path, key=lambda x: x[0])
    return particle_path_sorted


if __name__ == "__main__":

    # dataset dir and id

    #dir = "/Users/zw1/Downloads/0914/"
    dir = "/Users/zw1/Downloads/0928_async_iprobe/"

    
    syn_dir=dir+"syn.A.b128.n4.r128.B_p5000_s2000_id365728/"
    syn_id="365728"
    
    clover_dir=dir+"clover.A.b128.n4.r128.B_p5000_s2000_id275499/"
    clover_id="275499"
    
    fishtank_dir=dir+"fishtank.A.b128.n4.r128.B_p5000_s2000_id625027/"
    fishtank_id="625027"

    astro_dir=dir+"astro.A.b128.n4.r128.B_p5000_s2000_id418463/"
    astro_id="418463"

    fusion_dir=dir+"fusion.A.b128.n4.r128.B_p5000_s2000_id582493/"
    fusion_id="582493"

    astro_dir_temp=dir+"astro.A.b128.n4.r128.B_p5000_s2000_id418463/"
    astro_id_temp="418463"

    dataset_dir=[syn_dir,clover_dir,fishtank_dir,astro_dir,fusion_dir]
    
    particle_id=[syn_id,clover_id,fishtank_id,astro_id,fusion_id]

    dataset_dir_test=[astro_dir_temp]
    particle_id_test=[astro_id_temp]


    particle_list_sorted_all=[]
    max_particle_live_time=0
    particle_live_time_list=[]
    for dir_id_pair in zip(dataset_dir,particle_id):
        print(dir_id_pair[0],dir_id_pair[1])
        #draw figure using one x axis and y axis
        #figure out the longest filter execution time
        # get advect_bar
        # get blockid_list
        particle_list_sorted = get_particle_list_sorted(dir_id_pair[0],dir_id_pair[1])
        #if dir_id_pair[1]=="418463":
        print(particle_list_sorted[:2])
        particle_list_sorted_all.append(particle_list_sorted)
        #print(particle_list_sorted)
        print("long particle time", particle_list_sorted[-1][5])
        #choose the largest one among five data sets
        max_particle_live_time=max(max_particle_live_time,particle_list_sorted[-1][5])
        particle_live_time_list.append(particle_list_sorted[-1][5])

    # make sure the x coordinates 
    # then draw each bar separately
    figsize_x=20.0
    bar_height=0.7
    figsize_y=bar_height*5+0.5
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))
    # TODO, use the end of the comm as the particle alive time, do not use the filter time here
    print("max_particle_live_time",max_particle_live_time)
    
    usTos=1000000
    #plt.xticks([0,figsize_x/4,figsize_x/2,3*figsize_x/4,figsize_x], [0,round((max_particle_live_time/4/usTos),2),round((max_particle_live_time/2/usTos),2), round((3*max_particle_live_time/4/usTos),2),round((max_particle_live_time/usTos),2)])
    plt.xticks([0,figsize_x/4,figsize_x/2,3*figsize_x/4,figsize_x], [0,round((max_particle_live_time/4/usTos)),round((max_particle_live_time/2/usTos)), round((3*max_particle_live_time/4/usTos)),round((max_particle_live_time/usTos))])
    
    ax.set_yticks(bar_height*np.array(list(range(0, 5, 1)))+0.5*bar_height-0.05,["Synthetic","CloverLeaf3D","Hydraulics","Supernova","Tokamak"])
    
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20)
    ax.set_xlabel('Time(s)', fontsize=20)

    for data_index in range(0,5,1):
        # get advection time
        advected_bar=[]
        blockid_list=[]
        comm_wait_bar=[]
        advect_whole=0
        last_comm_start=0
        for p in particle_list_sorted_all[data_index]:
            #[recvok_time,advect_start_time,advect_end_time,comm_start_time,blist]
            #compute the width of each bar
            advect_spent_time=p[2]-p[1]
            width = (1.0*advect_spent_time)/(1.0*max_particle_live_time)

            # use start position
            advected_bar.append((figsize_x*(p[1]*1.0/max_particle_live_time),figsize_x*width))
            blockid_list.append(p[4])
            
            comm_wait_time = 0
            if int(p[0])==0:
                comm_wait_time = 0
            else:
                comm_wait_time = p[0]-last_comm_start
            
            #print("comm start",last_comm_start,"recv time", p[0], "comm_wait_time", comm_wait_time)
            comm_wiat_bar_width = (1.0*comm_wait_time)/(1.0*max_particle_live_time)
            comm_wait_bar.append((figsize_x*(last_comm_start*1.0/(1.0*max_particle_live_time)),figsize_x*comm_wiat_bar_width))
            
            last_comm_start = p[3]

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
        ax.broken_barh(xranges=comm_wait_bar,yrange=(bar_height*data_index,bar_height-0.1),facecolors='white',alpha=0.25, edgecolor="None")
        barh_other_overhead=get_barh_other_overhead(advected_bar,comm_wait_bar)
        print(len(barh_other_overhead))
        ax.broken_barh(xranges=barh_other_overhead,yrange=(bar_height*data_index,bar_height-0.1),facecolors='tab:red',alpha=0.25,edgecolor='None')          
        # add a small vertical line at the end
        # get the end of position
        # parameter is x and yrange
        final_line_pos = figsize_x*particle_live_time_list[data_index]*1.0/(1.0*max_particle_live_time)
        ax.vlines(final_line_pos,bar_height*data_index-0.05,bar_height*data_index+0.65,colors='k')

    fig.savefig("particle_gantt_five_datasets_white_wait.png",bbox_inches='tight')
    fig.savefig("particle_gantt_five_datasets_white_wait.pdf",bbox_inches='tight')