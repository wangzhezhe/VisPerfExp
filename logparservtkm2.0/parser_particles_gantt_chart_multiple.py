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



def draw_particle_bar(procs, pid, index, ax, figsize_x, bar_height):
    print("pid",pid)
    particle_list=[]
    advect_start_time=0
    advect_step_before=0


    for proc in range(0,procs,1):
        file_name = dirPath+"/particle_tracing_details."+str(proc)+".out"
        fo=open(file_name, "r")

        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")
                   
            # for in-transit case, the rankid may not eauqls to proc number
            # Event,SimCycle,BlockID(RankId),ParticleID,CurrTime,AdvectedSteps
            if str(step)==split_str[1] and str(pid)==split_str[3] :
                #print(split_str)
                if split_str[0]=="ADVECTSTART":
                    advect_start_time=float(split_str[4])
                    advect_step_before=float(split_str[5])
                if split_str[0]=="ADVECTEND":
                    # Event,SimCycle,BlockID(RankId),ParticleID,CurrTime,AdvectedSteps
                    advect_end_time=float(split_str[4])
                    advect_step_after=float(split_str[5])
                    blockid = int(split_str[2])
                    # start time, end time, advec steps, blockid
                    particle_list.append([advect_start_time,advect_end_time,advect_step_after-advect_step_before,blockid])
   
    #sorting all particle list
    #print("particle_list",particle_list)
    particle_list_sorted=sorted(particle_list, key=lambda x: x[0])
    particle_live_time = particle_list_sorted[-1][1]
    #print(particle_live_time)

    #extract advected start/end time
    advected_bar=[]
    blockid_list=[]
    #print("particle_list_sorted",particle_list_sorted)
    for p in particle_list_sorted:
        advect_spent_time=p[1]-p[0]
        width = (1.0*advect_spent_time)/(1.0*particle_live_time)

        # use start position
        advected_bar.append((figsize_x*(p[0]*1.0/particle_live_time),width*figsize_x))
        blockid_list.append(p[3])

    #print(advected_bar)
    block_list_set = set(blockid_list)
    colors = plt.cm.viridis(np.linspace(0,1,procs))
    color_list=[]
    # go through each value in the block id list
    # find a uniq color for it
    for id,val in enumerate(block_list_set):
        #print(id, val)
        color_list.append(colors[id])
   

    ax.broken_barh(xranges=advected_bar,yrange=(index*bar_height,(index+1)*bar_height),color=color_list)
    if index==0:
        ax.set_xlabel('Time(ms)', fontsize='large')
    #ax.set_ylabel('ParticleId='+str(pid), fontsize='large') 
    
    #print(figsize_x,particle_live_time)
   


# draw gantt chart from the perspective of tracing particles.
if __name__ == "__main__":
    
    if len(sys.argv)!=4:
        print("<binary> <procs> <step/cycle> <dirpath>")
        exit()

    procs=int(sys.argv[1])
    step=int(sys.argv[2])
    dirPath=sys.argv[3]

    # go through all files and sorting the particle according to advected steps
    particle_id_list=[*range(0, 1000, 100)]
    #print("particle_id_list",particle_id_list)
    
    # set the figuer y size
    # each loop will add a new bar into the figure
    index=0
    bar_height=0.1
    figsize_x=12
    figsize_y=(len(particle_id_list)+1)*bar_height
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y)) 
    plt.yticks([])
    for pid in particle_id_list:
        draw_particle_bar(procs,pid,index,ax,figsize_x,bar_height)
        index=index+1

    
    fig.savefig("particle_gantt_multiples.png",bbox_inches='tight')