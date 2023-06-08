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

#        std::string infoStr = "ParticleAdvectInfo_" + std::to_string((int)(v.size())) + "_" + std::to_string(TotalAdvectedSteps);
#        this->tracer.TimeTraceToBuffer(infoStr);
# parse the timetrace log and draw the gantt chart
if __name__ == "__main__":
    
    if len(sys.argv)!=5:
        print("<binary> <procs> <step/cycle> <dirpath> <tracing_rank_id>")
        exit()

    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    step=int(sys.argv[2])
    dirPath=sys.argv[3]
    tracing_rank_id=int(sys.argv[4])

    figsize_x = 8
    bar_height=1
    # give some place for legend
    figsize_y = bar_height
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))  


    file_name = dirPath+"/timetrace."+str(tracing_rank_id)+".out"
    print(file_name)


    # setting identify string
    adevct_start="ParticleAdvectStart_"+str(step)+" "
    adevct_end="ParticleAdvectEnd_"+str(step)+" "

    comm_start="CommStart_"+str(step)+" "
    comm_end="CommEnd_"+str(step)+" "

    filter_start="FilterStart_"+str(step)+" "
    filter_end="FilterEnd_"+str(step)+" "

    advec_info="ParticleAdvectInfo"

    filter_start_time=0
    filter_end_time=0
    
    # checking filter start/end time    
    fo=open(file_name, "r")
    for line in fo:
        line_strip=line.strip()
        split_str= line_strip.split(" ")
        if filter_start in line_strip:
            filter_start_time = float(split_str[1])       
        if filter_end in line_strip:
            filter_end_time = float(split_str[1])
    fo.close()

    filter_time = filter_end_time-filter_start_time

    # drawing the gant chart
    barh_list_advec=[]
    barh_list_comm=[]
    round_start_time_list=[]   

    advected_steps_list=[]
    particle_number_list=[]

    fo=open(file_name, "r")
    # read file again to compute bar
    for line in fo:
        line_strip=line.strip()
        split_str= line_strip.split(" ")

        if adevct_start in line_strip:
            #print("advect line strip",line_strip)
            advect_start_time_relative=float(split_str[1])-filter_start_time
            #print("adevct start",int(split_str[1]))
            round_start_time_list.append(int(advect_start_time_relative))

        if adevct_end in line_strip:
            advect_end_time_relative=float(split_str[1])-filter_start_time
            advect_spent_time=advect_end_time_relative-advect_start_time_relative
            width = (advect_spent_time)/filter_time
                
            if width<0:
                print("advec error",advect_end_time_relative, advect_start_time_relative)
            # use start position
            barh_list_advec.append((figsize_x*(advect_start_time_relative/filter_time),width*figsize_x))

        if comm_start in line_strip:
            comm_start_time_relative=float(split_str[1])-filter_start_time
        if comm_end in line_strip:
            comm_end_time_relative=float(split_str[1])-filter_start_time
            #print("comm",comm_end_time_relative-comm_start_time_relative)
            comm_spent_time=comm_end_time_relative-comm_start_time_relative
            width = (comm_spent_time)/filter_time
            #use start position
            if width<0:
                print("comm time error",comm_end_time_relative, comm_start_time_relative)
            barh_list_comm.append((figsize_x*(comm_start_time_relative/filter_time),width*figsize_x))

        if advec_info in line_strip:
            particle_info_details=line_strip.split(" ")[0].split("_")
            particle_number_list.append(int(particle_info_details[1]))
            advected_steps_list.append(int(particle_info_details[2]))

    fo.close()   
    
    plt.xticks([0,figsize_x/4,figsize_x/2,3*figsize_x/4,figsize_x], [0,filter_time/4,filter_time/2, 3*filter_time/4,filter_time])
    plt.yticks([])

    print(len(barh_list_advec))
    print(len(barh_list_comm))

    ax.broken_barh(xranges=barh_list_advec,yrange=(0,bar_height-0.1),facecolors='tab:blue')
    ax.broken_barh(xranges=barh_list_comm,yrange=(0,bar_height-0.1),facecolors='tab:red',alpha=0.2)   

    ax.broken_barh(xranges=[(0,1)],yrange=(1*bar_height,bar_height),facecolors='None',edgecolor='None')


    legend_elems = [Patch(facecolor='tab:blue', edgecolor='black', label='Advec'),
                            Patch(facecolor='tab:red', edgecolor='black', alpha=0.2, label='Comm and Wait'),
                            Patch(facecolor='white', edgecolor='black', label='Other overhead'),]
    legend = plt.legend(handles=legend_elems, loc='upper center', ncol=3, fontsize=12)
    ax.add_artist(legend)

    plt.xlabel('Time(ms)', fontsize="large")
    plt.ylabel('Rank' + str(tracing_rank_id), fontsize="large")
    fig.savefig("gant.png",bbox_inches='tight')
    
    # look for counter information
    counter_file_name = dirPath+"/counter."+str(tracing_rank_id)+".out"
    print(counter_file_name)

    fo=open(counter_file_name, "r")

    
    plt.clf()

    print("round_start_time_list size",len(round_start_time_list))
    print("round_start_time_list",round_start_time_list)

    print("particle_number_list size",len(particle_number_list))
    print("particle_number_list",particle_number_list)
    print("advected_steps_list",advected_steps_list)

    plt.plot(round_start_time_list,particle_number_list)
    plt.xlabel('Time(ms)', fontsize="large")
    plt.ylabel('#Particles', fontsize="large")
    fig.savefig("gant_particle_number_list.png",bbox_inches='tight')

    plt.clf()
    figsize_x = 8
    bar_height=1
    # give some place for legend
    figsize_y = bar_height*2
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))
    plt.xlabel('Time(ms)', fontsize="large")
    plt.ylabel('#Advected steps', fontsize="large")  
    plt.plot(round_start_time_list,advected_steps_list)
    fig.savefig("gant_advected_steps_list.png",bbox_inches='tight')

    # advected_steps_list/particle_number_list
    avg_list = [m/n for m, n in zip(advected_steps_list, particle_number_list)]

    plt.clf()
    figsize_y = bar_height*2
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))
    plt.xlabel('Time(ms)', fontsize="large")
    plt.ylabel('#Advected steps per particle', fontsize="small")  
    plt.plot(round_start_time_list,avg_list)
    fig.savefig("gant_avg_list.png",bbox_inches='tight')