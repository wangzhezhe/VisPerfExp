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

figsize_x=2*6
bar_height=0.08
ticksize=20
labelSize=26
legendSize=22

def get_barh_other_overhead(barh_list_advec, barh_list_comm):
    barh_list_other_overhead=[]
    #print("barh_list_advec",barh_list_advec[0:10])
    #print("barh_list_comm",barh_list_comm[0:10])
    # two pointer i, j
    i=0
    j=0
    
    last_bar_end=0
    curr_bar_star=0
    #print("len(barh_list_advec)",len(barh_list_advec),"len(barh_list_comm)",len(barh_list_comm))

    while(i<len(barh_list_advec) and j<len(barh_list_comm)):
        #print("debug i, j",i,j)
        if i==0 and j==0:
            last_bar_end=0
        # if i==392 and j==565:
        #    print("debug", barh_list_advec[i],barh_list_comm[j])
        #    exit(0)
    
        curr_bar_star=min(barh_list_advec[i][0],barh_list_comm[j][0])
        barh_list_other_overhead.append((last_bar_end,curr_bar_star-last_bar_end))
     
        # move i j and update last bar end position 
        if barh_list_advec[i][0]+barh_list_advec[i][1] < barh_list_comm[j][0] or (math.fabs(barh_list_advec[i][0]+barh_list_advec[i][1]- barh_list_comm[j][0])<0.000001):
            last_bar_end = barh_list_advec[i][0]+barh_list_advec[i][1]
            i=i+1
            continue
        if barh_list_comm[j][0]+barh_list_comm[j][1] < barh_list_advec[i][0] or (math.fabs(barh_list_comm[j][0]+barh_list_comm[j][1] - barh_list_advec[i][0])<0.000001):
            last_bar_end = barh_list_comm[j][0]+barh_list_comm[j][1]
            j=j+1
            continue
        
    # when either i and j end, put last one
    while i<len(barh_list_advec):
        curr_bar_start=barh_list_advec[i][0]
        barh_list_other_overhead.append((last_bar_end,curr_bar_start-last_bar_end))
        last_bar_end=curr_bar_start+barh_list_advec[i][1]
        i+=1


    while j<len(barh_list_advec):
        curr_bar_start=barh_list_comm[j][0]
        last_bar_end=curr_bar_start+barh_list_comm[j][1]
        barh_list_other_overhead.append((last_bar_end,curr_bar_start-last_bar_end))
        j+=1


    return barh_list_other_overhead

def draw_rank_gantt(ax, index, dirPath, officalname, procs):
    #print(index, dirPath, officalname)
    ax.set_xlim(0,figsize_x)
    ax.set_ylim(0,figsize_y)

    minWidth=0.000001
    filter_time=0

    # get filter time, use the rank0's filter time as the total one
    file_name = dirPath+"/timetrace."+str(0)+".out"
    fo=open(file_name, "r")
    filter_start_time=0.0
    filter_end="FilterEnd_"+str(step)+" "
    for line in fo:
        line_strip=line.strip()
        split_str= line_strip.split(" ")    
        if filter_end in line_strip:
            filter_end_time = float(split_str[1])
            filter_time = filter_end_time-0.0+100.0
    fo.close()
    usTos = 1000000
    usToms = 1000
    usTous = 1
    print("filter_time",filter_time)
    print("tick ", 0, int(filter_time/2/usTos),int(filter_time/usTos))
    print("tick pos", 0,figsize_x/4,figsize_x/2, 3*figsize_x/4,figsize_x)
    # x positions on labels and x ticks
    #ax.set_xticks([0,figsize_x/2,figsize_x], [0,round(filter_time/2/usTos,1),round(filter_time/usTos,1)],fontsize=ticksize)
    ax.set_xticks([0,figsize_x/2,figsize_x], [0,round(filter_time/2/usTos),round(filter_time/usTos)],fontsize=ticksize)
    
    #ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.3f}"))

    proc_id=list(range(0, procs, 8))
    # tick position in figure and tick text value
    # do not tick every rank
    if officalname=="Supernova":
        # only set the y label for the first one
        ax.set_yticks(bar_height*np.array(proc_id)+0.5*bar_height,proc_id, fontsize=ticksize)
    else:
        ax.set_yticks([])

    for rank in range(0,procs,1):
        file_name = dirPath+"/timetrace."+str(rank)+".out"
        print(file_name)
        fo=open(file_name, "r")
        #adevct_start="ParticleAdvectStart_"+str(step)+" "
        #adevct_end="ParticleAdvectEnd_"+str(step)+" "

        adevct_start="WORKLET_Start_"+str(step)+" "
        adevct_end="WORKLET_End_"+str(step)+" "

        comm_start="CommStart_"+str(step)
        comm_end="CommEnd_"+str(step)

        barh_list_advec=[]
        barh_list_comm=[]
        
        # read file again
        fo=open(file_name, "r")
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(" ")

            if adevct_start in line_strip:
                #print("advect line strip",line_strip)
                advect_start_time_relative=float(split_str[1])-filter_start_time
                #print("adevct start",int(split_str[1]))

            if adevct_end in line_strip:
                advect_end_time_relative=float(split_str[1])-filter_start_time
                advect_spent_time=advect_end_time_relative-advect_start_time_relative
                width = (advect_spent_time)/filter_time
                
                if width<0:
                    print("advec error",advect_end_time_relative, advect_start_time_relative)
                if width*figsize_x>=minWidth:
                    barh_list_advec.append((figsize_x*(advect_start_time_relative/filter_time),width*figsize_x))

            if comm_start == split_str[0]:
                comm_start_time_relative=float(split_str[1])-filter_start_time
            if comm_end == split_str[0]:
                comm_end_time_relative=float(split_str[1])-filter_start_time
                #print("comm",comm_end_time_relative-comm_start_time_relative)
                comm_spent_time=comm_end_time_relative-comm_start_time_relative
                width = (comm_spent_time)/filter_time
                #use start position
                if width<0:
                    print("comm error",comm_end_time_relative, comm_start_time_relative)
                if width*figsize_x>=minWidth:
                    #if rank==0:
                    #    print((figsize_x*(comm_start_time_relative/filter_time),width*figsize_x))
                    barh_list_comm.append((figsize_x*(comm_start_time_relative/filter_time),width*figsize_x))            

        fo.close()

        #list_advec_all.append(barh_list_advec)
        #list_comm_all.append(barh_list_comm)

        # draw the gant case
        # no label here
        
        ax.broken_barh(xranges=barh_list_advec,yrange=(rank*bar_height,bar_height),facecolors='tab:blue', edgecolor="none")
        ax.broken_barh(xranges=barh_list_comm,yrange=(rank*bar_height,bar_height),facecolors='white',alpha=0.35,edgecolor="none")


        barh_other_overhead=get_barh_other_overhead(barh_list_advec,barh_list_comm)
        ax.broken_barh(xranges=barh_other_overhead,yrange=(rank*bar_height,bar_height),facecolors='tab:red',alpha=0.35,edgecolor='None')          

    if officalname=="Supernova":
        ax.set_ylabel('Rank', fontsize=labelSize)
    
    #ax.set_xlabel(officalname, fontsize=labelSize)
    ax.title.set_text(officalname)
    ax.title.set_fontsize(labelSize)

# parse the timetrace log and draw the gantt chart
if __name__ == "__main__":
    
    if len(sys.argv)!=5:
        print("<binary> <procs> <step/cycle> <dirpath for all data> <unit>")
        exit()

    dataname=[ "astro_merge_76_77/astro.A.b128.n4.r128.B_p5000_s2000_id208001",
               "clover_merge_53_45/clover.A.b128.n4.r128.B_p5000_s2000_id275499"]

    official_name = ["Supernova","CloverLeaf3D"]
    
    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    step=int(sys.argv[2])
    dirPath=sys.argv[3]
    printUnit=sys.argv[4]
 
    # give some place for legend
    global figsize_y
    figsize_y = procs*bar_height

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(figsize_x,figsize_y))  

    for index, data in enumerate(dataname):
        draw_rank_gantt(axs[index],index,dirPath+"/"+data,official_name[index],procs)
    

    legend_elems = [Patch(facecolor='tab:blue', edgecolor='None', label='Advection'),
                            Patch(facecolor='white', edgecolor='black', alpha=0.35, label='Communication and Wait'),
                            Patch(facecolor='tab:red', edgecolor='None', alpha=0.35, label='Other overhead'),]
    fig.legend(handles=legend_elems, loc='upper center', ncol=3, fontsize=legendSize)

    if printUnit=="s":
        fig.text(0.5, 0.03, 'Time (seconds)', ha='center',fontsize=labelSize)
    if printUnit=="us":
        fig.text(0.5, 0.03, 'Time (us)', ha='center',fontsize=labelSize)
    fig.savefig("rank_gantt_all_merge_800.png",bbox_inches='tight',dpi=800)
    fig.savefig("rank_gantt_all_merge_100.png",bbox_inches='tight',dpi=100)
    fig.savefig("rank_gantt_all_merge.pdf",bbox_inches='tight')