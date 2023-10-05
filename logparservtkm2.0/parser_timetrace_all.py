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


figsize_x=5*6
bar_height=0.08
ticksize=20
labelSize=26
legendSize=22

def draw_rank_gantt(ax, index, dirPath, officalname, procs):
    print(index, dirPath, officalname)
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
    usToms = 1000
    usTous = 1
    print("filter_time",filter_time)
    print("tick ", 0, int(filter_time/2/usToms),int(filter_time/usToms))
    print("tick pos", 0,figsize_x/4,figsize_x/2, 3*figsize_x/4,figsize_x)
    # x positions on labels and x ticks
    ax.set_xticks([0,figsize_x/2,figsize_x], [0,int(filter_time/2/usToms),int(filter_time/usToms)],fontsize=ticksize)
    #ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.3f}"))

    proc_id=list(range(0, procs, 8))
    # tick position in figure and tick text value
    # do not tick every rank
    if officalname=="Tokamak":
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
        ax.broken_barh(xranges=barh_list_comm,yrange=(rank*bar_height,bar_height),facecolors='tab:red',alpha=0.35,edgecolor="none")

    if officalname=="Tokamak":
        ax.set_ylabel('Rank', fontsize=labelSize)
    
    #ax.set_xlabel(officalname, fontsize=labelSize)
    ax.title.set_text(officalname)
    ax.title.set_fontsize(labelSize)

# parse the timetrace log and draw the gantt chart
if __name__ == "__main__":
    
    if len(sys.argv)!=5:
        print("<binary> <procs> <step/cycle> <dirpath for all data> <unit>")
        exit()

    # dataname=["fusion.A.b128.n4.r128.B_p5000_s2000",
    #           "astro.A.b128.n4.r128.B_p5000_s2000",
    #           "fishtank.A.b128.n4.r128.B_p5000_s2000_id625027",
    #           "clover.A.b128.n4.r128.B_p5000_s2000",
    #           "syn.A.b128.n4.r128.B_p5000_s2000"]

    dataname=["fusion.A.b128.n4.r128.B_p5000_s2000_id582493",
               "astro.A.b128.n4.r128.B_p5000_s2000_id418463",
               "fishtank.A.b128.n4.r128.B_p5000_s2000_id625027",
               "clover.A.b128.n4.r128.B_p5000_s2000_id275499",
               "syn.A.b128.n4.r128.B_p5000_s2000_id365728"]

    dataname_test=["fusion.A.b128.n4.r128.B_p5000_s2000"]

    official_name = ["Tokamak","Supernova","Hydraulics","CloverLeaf3D","Synthetic"]
    
    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    step=int(sys.argv[2])
    dirPath=sys.argv[3]
    printUnit=sys.argv[4]
 
    # give some place for legend
    global figsize_y
    figsize_y = procs*bar_height

    fig, axs = plt.subplots(nrows=1, ncols=5, figsize=(figsize_x,figsize_y))  

    for index, data in enumerate(dataname):
        draw_rank_gantt(axs[index],index,dirPath+"/"+data,official_name[index],procs)
    

    legend_elems = [Patch(facecolor='tab:blue', edgecolor='black', label='Advection'),
                            Patch(facecolor='tab:red', edgecolor='black', alpha=0.35, label='Communication and Wait'),
                            Patch(facecolor='white', edgecolor='black', label='Other overhead'),]
    fig.legend(handles=legend_elems, loc='upper center', ncol=3, fontsize=legendSize)

    if printUnit=="ms":
        fig.text(0.5, 0.03, 'Time (ms)', ha='center',fontsize=labelSize)
    if printUnit=="us":
        fig.text(0.5, 0.03, 'Time (us)', ha='center',fontsize=labelSize)
    #fig.savefig("rank_gantt_all.png",bbox_inches='tight',dpi=800)
    fig.savefig("rank_gantt_all.png",bbox_inches='tight',dpi=100)
    #fig.savefig("rank_gantt_all.pdf",bbox_inches='tight')