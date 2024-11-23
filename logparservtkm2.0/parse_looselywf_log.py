from os import system
from os.path import exists
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# read the loosly coupled wf log 
# and draw the gant chart

ticksize=18
labelSize=16

#small scale case
#python3 parse_looselywf_log.py /Users/zhewang/Documents/Research/PaperSubmission/BlockAssignments/VisPerfStudy/Results/VisPerfExp_local_ubuntu_log/looselyclient_rrb.log /Users/zhewang/Documents/Research/PaperSubmission/BlockAssignments/VisPerfStudy/Results/VisPerfExp_local_ubuntu_log/looselyclient_trace.log /Users/zhewang/Documents/Research/PaperSubmission/BlockAssignments/VisPerfStudy/Results/VisPerfExp_local_ubuntu_log/looselyclient_est.log 

#large scale case
#python3 parse_looselywf_log.py /Users/zhewang/Documents/Research/PaperSubmission/BlockAssignments/VisPerfStudy/Results/VisPerfExp_wf_loose_rrb_clover_1023_5000/tightly_rrb.log /Users/zhewang/Documents/Research/PaperSubmission/BlockAssignments/VisPerfStudy/Results/VisPerfExp_wf_loose_webylog_clover_1023_5000/tightlyinsitu_webylog.log /Users/zhewang/Documents/Research/PaperSubmission/BlockAssignments/VisPerfStudy/Results/VisPerfExp_wf_loose_webyest_clover_1023_5000/tightlyinsitu_webyest.log  

def get_bars_for_rrb_log(logfile,wf_time,figsize_x):
    # the bar length is from 0 to wf_time, containing these bars
    # stage bars
    # load and sim bars
    # wait bars

    wf_time_for_figure = wf_time
    stage_bars=[]
    load_sim_bars=[]
    wait_bars=[]

    # xranges is sequence of tuples (xmin, xwidth)
    init_ok_str="Time init ok is"
    load_sim_str="load and sim ok"
    stage_str="stage ok is"
    runfilter_str="runfilter ok is"
    # update last tick gradually
    last_tick=0

    fo=open(logfile, "r")
    for line in fo:
        line_strip=line.strip()
        # extract from the "Time ... " log may start with rank id on HPC
        time_index = line_strip.find("Time")
        line_strip=line_strip[time_index:]
        split_str= line_strip.split(" ")
        
        if init_ok_str in line_strip:
            print(line_strip)
            init_tick=float(line_strip.split(" ")[4])
            last_tick=init_tick
            continue
        
        if stage_str in line_strip:
            stage_ok_tick=float(line_strip.split(" ")[4])
            print("stage_ok_tick",stage_ok_tick,"last_tick",last_tick)
            temp_stage_time=stage_ok_tick-last_tick
            print("temp_stage_time",temp_stage_time)
            # start position should be the last tick for all bars
            stage_bars.append((figsize_x*(last_tick/wf_time_for_figure), figsize_x*(temp_stage_time/wf_time_for_figure)))               
            last_tick=stage_ok_tick
            continue        
        
        if load_sim_str in line_strip:
            load_sim_tick=float(line_strip.split(" ")[9])
            print("load_sim_tick",load_sim_tick,"last_tick",last_tick)
            temp_load_sim_time=load_sim_tick-last_tick
            print("temp_load_sim_time",temp_load_sim_time)
            load_sim_bars.append((figsize_x*(last_tick/wf_time_for_figure), figsize_x*(temp_load_sim_time/wf_time_for_figure)))
            # update tick
            last_tick=load_sim_tick
            continue        

        if runfilter_str in line_strip:
            wait_filter_tick=float(line_strip.split(" ")[4])
            print("wait_filter_tick",wait_filter_tick,"last_tick",last_tick)
            temp_wait_filter_time=wait_filter_tick-last_tick
            print("temp_load_sim_time",temp_wait_filter_time)
            wait_bars.append((figsize_x*(last_tick/wf_time_for_figure), figsize_x*(temp_wait_filter_time/wf_time_for_figure)))
            # update tick
            last_tick=wait_filter_tick            
            continue        
    fo.close()

    return load_sim_bars,stage_bars,wait_bars


def get_bars_for_we_log(logfile,wf_time,figsize_x):

    wf_time_for_figure = wf_time
    stage_bars=[]
    load_sim_bars=[]
    wait_bars=[]
    process_bars=[]

    init_ok_str="Time init ok is"
    load_sim_str="load and sim ok"
    process_ok_str="processing log ok"
    stage_str="stage ok is"
    runfilter_str="runfilter ok is"
    last_tick=0

    fo=open(logfile, "r")
    for line in fo:
        line_strip=line.strip()
        # extract from the "Time ... " log may start with rank id on HPC
        time_index = line_strip.find("Time")
        line_strip=line_strip[time_index:]
        split_str= line_strip.split(" ")
        
        if init_ok_str in line_strip:
            init_tick=float(line_strip.split(" ")[4])
            last_tick=init_tick
            continue

        if load_sim_str in line_strip:
            load_sim_tick=float(line_strip.split(" ")[9])
            print("load_sim_tick",load_sim_tick,"last_tick",last_tick)
            temp_load_sim_time=load_sim_tick-last_tick
            print("temp_load_sim_time",temp_load_sim_time)
            load_sim_bars.append((figsize_x*(last_tick/wf_time_for_figure), figsize_x*(temp_load_sim_time/wf_time_for_figure)))
            # update tick
            last_tick=load_sim_tick
            continue    

        if process_ok_str in line_strip:
            process_ok_tick=float(line_strip.split(" ")[5])
            print("process_ok_tick",process_ok_tick,"last_tick",last_tick)
            temp_process_time=process_ok_tick-last_tick
            print("temp_process_time",temp_process_time)
            process_bars.append((figsize_x*(last_tick/wf_time_for_figure), figsize_x*(temp_process_time/wf_time_for_figure)))
            # update tick
            last_tick=process_ok_tick
            continue    


        if stage_str in line_strip:
            stage_ok_tick=float(line_strip.split(" ")[4])
            print("stage_ok_tick",stage_ok_tick,"last_tick",last_tick)
            temp_stage_time=stage_ok_tick-last_tick
            print("temp_stage_time",temp_stage_time)
            # start position should be the last tick for all bars
            stage_bars.append((figsize_x*(last_tick/wf_time_for_figure), figsize_x*(temp_stage_time/wf_time_for_figure)))               
            last_tick=stage_ok_tick
            continue        
        
    
        if runfilter_str in line_strip:
            wait_filter_tick=float(line_strip.split(" ")[4])
            print("wait_filter_tick",wait_filter_tick,"last_tick",last_tick)
            temp_wait_filter_time=wait_filter_tick-last_tick
            print("temp_load_sim_time",temp_wait_filter_time)
            wait_bars.append((figsize_x*(last_tick/wf_time_for_figure), figsize_x*(temp_wait_filter_time/wf_time_for_figure)))
            # update tick
            last_tick=wait_filter_tick            
            continue        
    fo.close()

    return load_sim_bars,process_bars,stage_bars,wait_bars


if __name__ == "__main__":
    if len(sys.argv)!=4:
        print("<binary> <logfile_rrb> <logfile_we_trace> <logfile_we_est>")
        exit()

    logfile_rrb=sys.argv[1]
    logfile_we_trace=sys.argv[2]
    logfile_we_est=sys.argv[3]

    fo=open(logfile_rrb, "r")
    wf_start_time=0.0
    # using this as input of time manually
    wf_time_for_figure=230.0
    #wf_time_for_figure=185.0
    
    figsize_x=15
    figsize_y=2
    bar_height=0.01

    load_sim_bars,stage_bars,wait_bars = get_bars_for_rrb_log(logfile_rrb, wf_time_for_figure, figsize_x)

    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))  
    ax.set_xlim(0,figsize_x)

    ax.broken_barh(xranges=load_sim_bars,yrange=(0,bar_height),facecolors='tab:blue', edgecolor="none")
    ax.broken_barh(xranges=stage_bars,yrange=(0,bar_height),facecolors='tab:green',alpha=0.35,edgecolor="none")
    ax.broken_barh(xranges=wait_bars,yrange=(0,bar_height),facecolors='tab:red',alpha=0.35,edgecolor='None')          
    

    we_load_sim_bars, we_process_bars, we_stage_bars,we_wait_bars = get_bars_for_we_log(logfile_we_trace, wf_time_for_figure, figsize_x)

    ax.broken_barh(xranges=we_load_sim_bars,yrange=(1.5*bar_height,bar_height),facecolors='tab:blue', edgecolor="none")
    ax.broken_barh(xranges=we_process_bars,yrange=(1.5*bar_height,bar_height),facecolors='tab:purple', edgecolor="none")
    ax.broken_barh(xranges=we_stage_bars,yrange=(1.5*bar_height,bar_height),facecolors='tab:green',alpha=0.35,edgecolor="none")
    ax.broken_barh(xranges=we_wait_bars,yrange=(1.5*bar_height,bar_height),facecolors='tab:red',alpha=0.35,edgecolor='None')          


    print("---third case debug")
    est_load_sim_bars, est_process_bars, est_stage_bars, est_wait_bars = get_bars_for_we_log(logfile_we_est, wf_time_for_figure, figsize_x)

    ax.broken_barh(xranges=est_load_sim_bars,yrange=(3*bar_height,bar_height),facecolors='tab:blue', edgecolor="none")
    ax.broken_barh(xranges=est_process_bars,yrange=(3*bar_height,bar_height),facecolors='tab:purple', edgecolor="none")
    ax.broken_barh(xranges=est_stage_bars,yrange=(3*bar_height,bar_height),facecolors='tab:green',alpha=0.35,edgecolor="none")
    ax.broken_barh(xranges=est_wait_bars,yrange=(3*bar_height,bar_height),facecolors='tab:red',alpha=0.35,edgecolor='None')          

    #ax.set_yticks([])
    plt.xticks([0,figsize_x/4,figsize_x/2,3*figsize_x/4,figsize_x], [0,int(wf_time_for_figure/4),int(wf_time_for_figure/2), int(3*wf_time_for_figure/4),int(wf_time_for_figure)],fontsize=20)
    plt.yticks([0.5*bar_height,2*bar_height,3.5*bar_height], ["RRB","Trace","Estimation"],fontsize=18)
    
    #adding legend

    legend_elems = [Patch(facecolor='tab:blue', edgecolor='None', label='Sim&Load'),
                            Patch(facecolor='tab:purple', edgecolor='None', label='Assignment'),
                            Patch(facecolor='tab:green', alpha=0.35, edgecolor='None', label='Stage'),
                            Patch(facecolor='tab:red', alpha=0.35, edgecolor='None', label='Wait')]

    legend = plt.legend(handles=legend_elems,bbox_to_anchor=(0.8, 1.35),ncol=4, fontsize=labelSize)


    plt.xlabel('Time (seconds)', fontsize=ticksize)
    plt.ylabel('Assignment plans', fontsize=ticksize)    

    fig.savefig("parse_looselywf_gantt.png",bbox_inches='tight',dpi=800)
