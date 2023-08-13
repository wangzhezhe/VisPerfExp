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

# draw gantt chart from the perspective of tracing particles.
if __name__ == "__main__":
    
    if len(sys.argv)!=5:
        print("<binary> <procs> <step/cycle> <dirpath> <tracing_particle_id>")
        exit()

    procs=int(sys.argv[1])
    step=int(sys.argv[2])
    dirPath=sys.argv[3]
    tracing_particle_id=int(sys.argv[4])
    
    dirname = dirPath.split("/")[-2]

    # go through all files and sorting the particle according to advected steps
    particle_list=[]

    advect_whole=0
    advect_steps_whole=0
    comm_start_time=0
    comm_start_list=[]
    comm_end_time=0
    comm_time_list=[]
    actual_comm_list=[]
    recv_time_list=[]
    send_end_list=[]
    for proc in range(0,procs,1):
        file_name = dirPath+"/particle_tracing_details."+str(proc)+".out"
        fo=open(file_name, "r")
        
        advect_start_time=0
        advect_step_before=0

        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")
                   
            # for in-transit case, the rankid may not eauqls to proc number
            # Event,SimCycle,BlockID(RankId),ParticleID,CurrTime,AdvectedSteps
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
                if split_str[0]=="RECVOK":
                    recv_time_list.append(float(split_str[4]))


    #sorting all particle list
    particle_list_sorted=sorted(particle_list, key=lambda x: x[0])
    print(particle_list_sorted)
    particle_live_time = particle_list_sorted[-1][1]
    #print(particle_live_time)


    bar_height=0.2
    #figsize_x=20
    figsize_x=36
    figsize_y=bar_height*8
    
    #extract advected start/end time
    advected_bar=[]
    blockid_list=[]
    pnum_list=[]
    advected_bar_fourth_quantile=[]
    particle_live_time_last_quantile=3.0*particle_live_time/4.0
    advect_spent_time_sum=0
    for p in particle_list_sorted:
        advect_spent_time=p[1]-p[0]
        advect_spent_time_sum=advect_spent_time_sum+advect_spent_time
        advect_whole=advect_whole+advect_spent_time
        width = (1.0*advect_spent_time)/(1.0*particle_live_time)
        pnum_list.append(p[4])

        # use start position
        advected_bar.append((figsize_x*(p[0]*1.0/particle_live_time),width*figsize_x))
        blockid_list.append(p[3])
        
        # record the start position of last 1/4 element for zoomin figure
        if (p[0]>particle_live_time_last_quantile):
            distance_from_fourth_quantile=p[0]-particle_live_time_last_quantile
            width = (1.0*advect_spent_time)/(particle_live_time/4.0)
            advected_bar_fourth_quantile.append((figsize_x*(distance_from_fourth_quantile*1.0/(particle_live_time/4.0)),width*figsize_x))

    
    #create facecolors according to blockid_list
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
    index = 0
    for _, val in enumerate(blockid_list):
        # if key exist, continue
        if val in colordic.keys():
            continue
        else:    
        # if key not exist, create a new pair, index++
            colordic[val]=index
            index=index+1

    print("colordic", colordic)

    color_list=[]
    # go through each value in the block id list
    # find a uniq color for it
    for id,val in enumerate(blockid_list):
        #print(id, val)
        color_list.append(colors[colordic[val]])
    

    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))

    print("advect_spent_time_sum",advect_spent_time_sum)

    ax.broken_barh(xranges=advected_bar,yrange=(bar_height,2*bar_height-0.1),color=color_list,edgecolor="none")
    ax.set_xlabel('Time(ms)', fontsize='large')
    ax.set_ylabel('ParticleId='+str(tracing_particle_id), fontsize='large') 
    
    print(figsize_x,particle_live_time)
   
    plt.yticks([])
    plt.xticks([0.0,figsize_x/4.0,figsize_x/2.0,3.0*figsize_x/4.0,figsize_x], [0.0,particle_live_time/4.0,particle_live_time/2.0,3*particle_live_time/4.0,particle_live_time])
    
    print("recv_time_list",sorted(recv_time_list))
    recv_time_list_xpoints = [figsize_x*t/particle_live_time for t in recv_time_list]
    print("recv_time_list_xpoints",recv_time_list_xpoints)
    
    print("comm_start_list",sorted(comm_start_list))
    print("send_end_list", sorted(send_end_list))
    comm_start_list_xpoints= [figsize_x*t/particle_live_time for t in comm_start_list]

    #for v in recv_time_list_xpoints:
    #   plt.axvline(x = v, ls='--', lw=1, color = 'r', alpha=0.8)

    #for v in comm_start_list_xpoints:
    #   plt.axvline(x = v, ls='--', lw=1, color = 'b', alpha=0.8)

    fig.savefig("particle_gantt_"+dirname+".png",bbox_inches='tight')
    
    #print(advected_bar)
    print(blockid_list)
    #print("comm_start_list",comm_start_list)

 
    plt.clf()
    # show the last 1/4 quantile
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))
    ax.broken_barh(xranges=advected_bar_fourth_quantile,yrange=(bar_height,2*bar_height-0.1),color=color_list,edgecolor="none")
    ax.set_xlabel('Time(ms)', fontsize='large')
    ax.set_ylabel('ParticleId='+str(tracing_particle_id), fontsize='medium') 
       
    plt.yticks([])
    plt.xticks([0.0,figsize_x/2.0,figsize_x], [3*particle_live_time/4.0,14*particle_live_time/16.0,particle_live_time])
    
    
    fig.savefig("particle_gantt_zoomin.png",bbox_inches='tight')

    print("particle_live_time",particle_live_time,"advect_whole",advect_whole,"other",particle_live_time-advect_whole)
    print("advect_steps_whole",advect_steps_whole)

    print("pnum_list",pnum_list)    
    plt.clf()
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))
    ax.plot(pnum_list)
    ax.set_xlabel('Traverse number', fontsize='large')
    ax.set_ylabel('Size of batch', fontsize='medium') 
    fig.savefig("particle_pnum_list.png",bbox_inches='tight')

    plt.clf()
    ax.plot(actual_comm_list)
    print(actual_comm_list)
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))
    fig.savefig("particle_actual_comm_list.png",bbox_inches='tight')