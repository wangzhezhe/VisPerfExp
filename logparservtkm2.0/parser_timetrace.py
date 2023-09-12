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

# parse the timetrace log and draw the gantt chart
if __name__ == "__main__":
    
    if len(sys.argv)!=4:
        print("<binary> <procs> <step/cycle> <dirpath>")
        exit()

    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    step=int(sys.argv[2])
    dirPath=sys.argv[3]
    
    # the dirname should end with /
    dirname = dirPath.split("/")[-2]
    print("dirname",dirname)

    figsize_x = 6
    bar_height=0.07
    # give some place for legend
    figsize_y = procs*bar_height+2.5
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))  

    print("dpi is ", fig.dpi)
    ax.set_xlim(0,figsize_x)
    
    # how to set this value properly?
    minWidth=0.00001
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
            filter_time = filter_end_time
    fo.close()

    print("filter_time",filter_time)
    print("tick ", 0,round(filter_time/4,2),round(filter_time/2,2), round(3*filter_time/4,2),round(filter_time,2))
    print("tick pos", 0,figsize_x/4,figsize_x/2,3*figsize_x/4,figsize_x)
    plt.xticks([0,figsize_x/4,figsize_x/2,3*figsize_x/4,figsize_x], [0,round(filter_time/4,2),round(filter_time/2,2), round(3*filter_time/4,2),round(filter_time,2)],fontsize=15)
    #ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.3f}"))

    proc_id=list(range(0, procs, 4))
    # tick position in figure and tick text value
    # do not tick every rank
    plt.yticks(bar_height*np.array(proc_id)+0.5*bar_height,proc_id, fontsize=15)

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
                comm_spent_time=comm_end_time_relative-comm_start_time_relative
                width = (comm_spent_time)/filter_time
                #use start position
                if width<0:
                    print("comm error",comm_end_time_relative, comm_start_time_relative)
                if width*figsize_x>=minWidth:
                    #if rank==0:
                    #    print("comm start", comm_start_time_relative, "comm end", comm_end_time_relative)
                    #    print("fig start", figsize_x*(comm_start_time_relative/filter_time), "width", width*figsize_x)
                    barh_list_comm.append((figsize_x*(comm_start_time_relative/filter_time),width*figsize_x))            

        fo.close()

        #list_advec_all.append(barh_list_advec)
        #list_comm_all.append(barh_list_comm)

        # draw the gant case
        if rank==0:
            # use label here
            #ax.broken_barh(xranges=barh_list_advec,yrange=(rank*bar_height,bar_height-0.1),facecolors='tab:blue',label='Advec')
            #ax.broken_barh(xranges=barh_list_comm,yrange=(rank*bar_height,bar_height-0.1),facecolors='tab:red',alpha=0.2,label='Comm_Wait')          
            ax.broken_barh(xranges=barh_list_advec,yrange=(rank*bar_height,bar_height),facecolors='tab:blue',edgecolor='None')
            ax.broken_barh(xranges=barh_list_comm,yrange=(rank*bar_height,bar_height),facecolors='tab:red',alpha=0.35,edgecolor='None')          
            # customize the legend
            legend_elems = [Patch(facecolor='tab:blue', edgecolor='None', label='Advec'),
                            Patch(facecolor='tab:red', alpha=0.35, edgecolor='None', label='Comm and Wait'),
                            Patch(facecolor='white', edgecolor='black', label='Other overhead'),]
            legend = plt.legend(handles=legend_elems, loc='upper center', ncol=3, fontsize=10)
            ax.add_artist(legend)
        else:
            # no label here
            ax.broken_barh(xranges=barh_list_advec,yrange=(rank*bar_height,bar_height),facecolors='tab:blue',edgecolor='None')
            ax.broken_barh(xranges=barh_list_comm,yrange=(rank*bar_height,bar_height),facecolors='tab:red',alpha=0.35,edgecolor='None')

    # get some space for legend in the center
    ax.broken_barh(xranges=[(0,1)],yrange=(procs*bar_height,bar_height),facecolors='None',edgecolor='None')
    plt.xlabel('Time(ms)', fontsize=15)
    plt.ylabel('Rank', fontsize=15)
    fig.savefig("gantt_worklet_"+dirname+".png",bbox_inches='tight', dpi=600)