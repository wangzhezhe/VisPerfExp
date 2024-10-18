from os import system
from os.path import exists
import sys
import matplotlib.pyplot as plt

# read the loosly coupled wf log 
# and draw the gant chart

ticksize=10

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
        split_str= line_strip.split(" ")    
        
        if init_ok_str in line_strip:
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
            last_tick=load_sim_tick
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
    if len(sys.argv)!=3:
        print("<binary> <logfile_rrb> <logfile_we_trace>")
        exit()

    logfile_rrb=sys.argv[1]
    logfile_we_trace=sys.argv[2]

    fo=open(logfile_rrb, "r")
    wf_start_time=0.0
    # using this as input of time manually
    wf_time_for_figure=250.0
    figsize_x=15
    figsize_y=2
    ticksize=8
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

    #ax.set_yticks([])
    plt.xticks([0,figsize_x/4,figsize_x/2,3*figsize_x/4,figsize_x], [0,int(wf_time_for_figure/4),int(wf_time_for_figure/2), int(3*wf_time_for_figure/4),int(wf_time_for_figure)],fontsize=ticksize)
    plt.yticks([0.5*bar_height,2*bar_height], ["RRB","Trace"],fontsize=ticksize)



    plt.xlabel('Time (seconds)', fontsize=ticksize)
    plt.ylabel('Assignment plans', fontsize=ticksize)    

    fig.savefig("parse_looselywf_gantt.png",bbox_inches='tight',dpi=800)
