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

    # go through all files and sorting the particle according to advected steps
    particle_list=[]

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
            if str(step)==split_str[1] and str(tracing_particle_id)==split_str[3] :
                #print(split_str)
                if split_str[0]=="ADVECTSTART":
                    advect_start_time=float(split_str[4])
                    advect_step_before=float(split_str[5])
                if split_str[0]=="ADVECTEND":
                    advect_end_time=float(split_str[4])
                    advect_step_after=float(split_str[5])
                    blockid = int(split_str[2])
                    # start time, end time, advec steps, blockid
                    particle_list.append([advect_start_time,advect_end_time,advect_step_after-advect_step_before,blockid])


    #sorting all particle list
    particle_list_sorted=sorted(particle_list, key=lambda x: x[0])
    print(particle_list_sorted)
    particle_live_time = particle_list_sorted[-1][1]
    #print(particle_live_time)


    bar_height=0.2
    figsize_x=20
    figsize_y=bar_height*8
    
    #extract advected start/end time
    advected_bar=[]
    blockid_list=[]
    advected_bar_fourth_quantile=[]
    particle_live_time_last_quantile=3.0*particle_live_time/4.0
    for p in particle_list_sorted:
        advect_spent_time=p[1]-p[0]
        width = (1.0*advect_spent_time)/(1.0*particle_live_time)

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

    
    #colors = plt.cm.jet(np.linspace(0,1,distinct_block_ids))
    colors = plt.cm.viridis(np.linspace(0,1,distinct_block_ids))

    color_list=[]
    # go through each value in the block id list
    # find a uniq color for it
    for id,val in enumerate(block_list_set):
        #print(id, val)
        color_list.append(colors[id])
    

    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))

    
    ax.broken_barh(xranges=advected_bar,yrange=(bar_height,2*bar_height-0.1),color=color_list)
    ax.set_xlabel('Time(ms)', fontsize='large')
    ax.set_ylabel('ParticleId='+str(tracing_particle_id), fontsize='large') 
    
    print(figsize_x,particle_live_time)
   
    plt.yticks([])
    plt.xticks([0.0,figsize_x/4.0,figsize_x/2.0,3.0*figsize_x/4.0,figsize_x], [0.0,particle_live_time/4.0,particle_live_time/2.0,3*particle_live_time/4.0,particle_live_time])
    
    
    fig.savefig("particle_gantt.png",bbox_inches='tight')
    
    #print(advected_bar)
    #print(blockid_list)

    plt.clf()
    # show the last 1/4 quantile
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))
    ax.broken_barh(xranges=advected_bar_fourth_quantile,yrange=(bar_height,2*bar_height-0.1),color=color_list)
    ax.set_xlabel('Time(ms)', fontsize='large')
    ax.set_ylabel('ParticleId='+str(tracing_particle_id), fontsize='large') 
       
    plt.yticks([])
    plt.xticks([0.0,figsize_x/2.0,figsize_x], [3*particle_live_time/4.0,14*particle_live_time/16.0,particle_live_time])
    
    
    fig.savefig("particle_gantt_zoomin.png",bbox_inches='tight')