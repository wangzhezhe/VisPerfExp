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

# ticksize=20
# labelSize=26
# legendSize=22

ticksize=8
labelSize=6
legendSize=11

# using barh_list_adv and barh_list_comm to compute the other overhead
def get_barh_other_overhead(barh_list_advec, barh_list_comm, debug=False):

    #print("len(barh_list_advec)",len(barh_list_advec),"len(barh_list_comm)",len(barh_list_comm))
    if len(barh_list_comm)==0 and len(barh_list_advec)==0:
        return []
    barh_list_other_overhead=[]
    #print("barh_list_advec",barh_list_advec[0:10])
    #print("barh_list_comm",barh_list_comm[0:10])
    # two pointer i, j
    i=0
    j=0
    
    # the distance between curr bar start and last bar end should be other overhead
    last_bar_end=0
    curr_bar_star=0

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
        # when the end of the list is smalller then current comm or the length is amost to zero
        # when the adv is before the comm
        if barh_list_advec[i][0]+barh_list_advec[i][1] < barh_list_comm[j][0] or (math.fabs(barh_list_advec[i][0]+barh_list_advec[i][1]- barh_list_comm[j][0])<0.000001):
            last_bar_end = barh_list_advec[i][0]+barh_list_advec[i][1]
            i=i+1
            continue
        # when the comm is before the adv
        if barh_list_comm[j][0]+barh_list_comm[j][1] < barh_list_advec[i][0] or (math.fabs(barh_list_comm[j][0]+barh_list_comm[j][1] - barh_list_advec[i][0])<0.000001):
            last_bar_end = barh_list_comm[j][0]+barh_list_comm[j][1]
            j=j+1
            continue
        
    # when either i and j end
    # there is remaining i
    while i<len(barh_list_advec):
        if debug:
            print("remainig i",i)
        curr_bar_start=barh_list_advec[i][0]
        barh_list_other_overhead.append((last_bar_end,curr_bar_start-last_bar_end))
        last_bar_end=curr_bar_start+barh_list_advec[i][1]
        i+=1

    # there is remaining j
    # the curr bar start should be the end of previous one
    while j<len(barh_list_comm):
        if debug:
            print("remainig j",j)
        curr_bar_start=barh_list_comm[j][0]
        barh_list_other_overhead.append((last_bar_end,curr_bar_start-last_bar_end))
        # update the ladt bar end
        last_bar_end=curr_bar_start+barh_list_comm[j][1]
        j+=1


    return barh_list_other_overhead

        




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
    bar_height=0.08
    # give some place for legend
    figsize_y = procs*bar_height
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
    usToms=1000
    plt.xticks([0,figsize_x/4,figsize_x/2,3*figsize_x/4,figsize_x], [0,int(filter_time/4/usToms),int(filter_time/2/usToms), int(3*filter_time/4/usToms),int(filter_time/usToms)],fontsize=ticksize)
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
            ax.broken_barh(xranges=barh_list_comm,yrange=(rank*bar_height,bar_height),facecolors='white',alpha=0.35,edgecolor='None')          
            
            barh_other_overhead=get_barh_other_overhead(barh_list_advec,barh_list_comm)
            ax.broken_barh(xranges=barh_other_overhead,yrange=(rank*bar_height,bar_height),facecolors='tab:red',alpha=0.35,edgecolor='None')          

            # print(barh_list_advec)
            # print(barh_list_comm)
            # print(barh_other_overhead)
            

            # customize the legend
            legend_elems = [Patch(facecolor='tab:blue', edgecolor='None', label='Advec'),
                            Patch(facecolor='white', alpha=0.35, edgecolor='black', label='Comm and Wait'),
                            Patch(facecolor='tab:red', alpha=0.35, edgecolor='None', label='Other overhead'),]
            #when using automatic legend position
            #legend = plt.legend(handles=legend_elems, loc='upper center', ncol=3, fontsize=labelSize)
            #for large one
            #legend = plt.legend(handles=legend_elems,bbox_to_anchor=(0.8, 1.1),ncol=3, fontsize=labelSize)
            legend = plt.legend(handles=legend_elems,bbox_to_anchor=(0.8, 1.4),ncol=3, fontsize=labelSize)
            
            ax.add_artist(legend)
        else:
            # no label here
            ax.broken_barh(xranges=barh_list_advec,yrange=(rank*bar_height,bar_height),facecolors='tab:blue',edgecolor='None')
            ax.broken_barh(xranges=barh_list_comm,yrange=(rank*bar_height,bar_height),facecolors='white',alpha=0.35,edgecolor='None')
            barh_other_overhead=get_barh_other_overhead(barh_list_advec,barh_list_comm)
            ax.broken_barh(xranges=barh_other_overhead,yrange=(rank*bar_height,bar_height),facecolors='tab:red',alpha=0.35,edgecolor='None')          

    # get some space for legend in the center
    ax.broken_barh(xranges=[(0,1)],yrange=(procs*bar_height,bar_height),facecolors='None',edgecolor='None')
    plt.xlabel('Time(ms)', fontsize=ticksize)
    plt.ylabel('Rank', fontsize=ticksize)
    file_name = "gantt_chart_"+dirname+".png"
    fig.savefig(file_name,bbox_inches='tight', dpi=1200)
    print("generate file: ", file_name)
