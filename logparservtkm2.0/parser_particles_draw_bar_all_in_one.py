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
from matplotlib.lines import Line2D

labelSize = 23
tickSize = 22
legendsize=21
figsize_x = 6.0
figsize_y = 5.5
lwidth=2.5

def draw_one_bar_fig(ax, dirPath, procs, data_official_name):
    # extract largest total exeuction time
    filter_start="FilterStart_"+str(simSycle)+" "
    filter_end="FilterEnd_"+str(simSycle)+" "
    
    for rank in range(0,procs,1):
        file_name = dirPath+"/timetrace."+str(rank)+".out"
        fo=open(file_name, "r")
        max_filter_time=0
        filter_time=0
        filter_start_time=0
        filter_end_time=0
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(" ")
            if filter_start in line_strip:
                filter_start_time = float(split_str[1])       
            if filter_end in line_strip:
                filter_end_time = float(split_str[1])
            filter_time = filter_end_time-filter_start_time
            max_filter_time = max(max_filter_time,filter_time)
        fo.close()
    
    print("filter execution time is", max_filter_time)

    # go through each particle files
    # each particle, store id, life time, traversed blocks number, die reason
    
    ## This is for another figure that use the number of particles as y axis
    number_bin = 50
    bin_length = 1.0/(1.0*number_bin)
    bin_list_oob = [0]*number_bin
    bin_list_zero = [0]*number_bin
    bin_list_maxstep = [0]*number_bin
    
    total_particles = 0
    long_exec = 0 
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        #print(file_name)
        fo=open(file_name, "r")
        cycle_identifier ="s"+str(simSycle)
        
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")
            #print(split_str)
            
            if cycle_identifier in line_strip:
                total_particles=total_particles+1
                # id, lifetime/total execution time, traversed number of blocks, die reason
                ratio = float(split_str[3])/filter_time
                num_adv_steps=int(split_str[12])
                #compute the bin_index
                bin_index= int(ratio/bin_length)
                #sequence is outof bounud, zero velocity and max step
                if(split_str[2]=='b'):
                    bin_list_oob[bin_index]+=1
                    if num_adv_steps>1800:
                        long_exec=long_exec+1
                elif(split_str[2]=='z'):
                    bin_list_zero[bin_index]+=1
                    if num_adv_steps>1800:
                        long_exec=long_exec+1
                else:
                    bin_list_maxstep[bin_index]+=1
                    long_exec+=1
        
        fo.close()

    # another plot
    # print(bin_list)
    # fig, ax = plt.subplots()
    width = 0.25 

    # dule ax
    print("total_particles",total_particles)
    ax2=ax.twinx()
    ax2.set_ylim(0,total_particles)

    # generate list for existing particles
    active_particles=[]
    curr_active_particles=total_particles
    for i in range(number_bin):
        active_particles.append(curr_active_particles)
        curr_active_particles=curr_active_particles-bin_list_oob[i]-bin_list_zero[i]-bin_list_maxstep[i]

    
    ind = np.arange(number_bin)
    #plt.xticks(ind, ['(0,0.1]', '(0.1,0.2]' , '(0.2,0.3]', '(0.3,0.4]', '(0.4,0.5]','(0.5,0.6]','(0.6,0.7]','(0.7,0.8]','(0.8,0.9]','(0.9,1.0]'], fontsize=7.5)
    #ax.set_xlabel('Index of bin between 0% to 100%', fontsize=labelSize)
    
    ax.title.set_text(data_official_name)
    ax.title.set_fontsize(labelSize)
    
    if data_official_name=="Tokamak":
        ax.set_ylabel('Number of terminated particles', fontsize=labelSize)
        ax2.set_yticks([])
    elif data_official_name=="Synthetic":
        ax.set_yticks([])
        ax2.set_ylabel('Number of active particles', fontsize=labelSize)
    else:
        ax.set_yticks([])
        ax2.set_yticks([])

    ax.tick_params(axis='y', labelsize=tickSize)
    ax2.tick_params(axis='y', labelsize=tickSize)
    ax2.set_xticks([])

    tempx = figsize_x*8.0
    ax.set_xticks([0,tempx/2.0,tempx],["0%","50%","100%"],fontsize=tickSize)
    #ax2.tick_params(axis='x', labelsize=tickSize)
    
    
    width = 0.8
    bottom = np.zeros(number_bin)
    p1 = ax.bar(ind,bin_list_oob,width, bottom=bottom,color='blue',alpha=0.8)
    bottom+=bin_list_oob
    p2 = ax.bar(ind,bin_list_zero,width,bottom=bottom,color='red',alpha=0.8)
    bottom+=bin_list_zero
    p3 = ax.bar(ind,bin_list_maxstep,width,bottom=bottom,color='green',alpha=0.8)


    ax2.plot(ind,active_particles,linewidth=lwidth, color='orange')

    #ax.legend((p1, p2, p3), ('Out of bounds', 'Zero velocity','Max step'),  ncol=1, fontsize='large')
    #fig.savefig("existing_particles_"+dirName+".png", bbox_inches='tight')
    print("out of bound particles ratio:", "{:.1%}".format(sum(bin_list_oob)/total_particles))
    print("zero velocity particles ratio:", "{:.1%}".format(sum(bin_list_zero)/total_particles))
    print("max step particles ratio:", "{:.1%}".format(sum(bin_list_maxstep)/total_particles))

    #print("long exec particles ratio:", 1.0*long_exec/total_particles)


# parse the timetrace log and draw the gantt chart
if __name__ == "__main__":

    if len(sys.argv)!=3:
        print("<binary> <procs> <dirpath for all data>")
        exit()

    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    simSycle=0
    dirPath=sys.argv[2]

    dataname=["fusion.A.b128.n4.r128.B_p5000_s2000",
              "astro.A.b128.n4.r128.B_p5000_s2000",
              "fishtank.A.b128.n4.r128.B_p5000_s2000_id625027",
              "clover.A.b128.n4.r128.B_p5000_s2000",
              "syn.A.b128.n4.r128.B_p5000_s2000"]

    official_name = ["Tokamak","Supernova","Hydraulics","CloverLeaf3D","Synthetic"]


    fig, axs = plt.subplots(nrows=1, ncols=5, figsize=(figsize_x*5,figsize_y)) 

    for index, data in enumerate(dataname):
        dirname_complete = dirPath+"/"+data
        print("dirname",dirname_complete,"index",index)
        draw_one_bar_fig(axs[index],dirname_complete, procs, official_name[index])
    
    legend_elem_1 = [Patch( label='Out of bounds',
                        facecolor='blue', edgecolor=None),
                     Patch(label='Zero velocity',
                        facecolor='red', edgecolor=None),
                     Patch( label='Max step',
                        facecolor='green', edgecolor=None)]
    
    fig.legend(handles=legend_elem_1, bbox_to_anchor=(0.62,1.08), ncol=3, fontsize=legendsize)


    fig.text(0.5, 0.0, 'Ratio of execution time', ha='center',fontsize=labelSize)
    fig.savefig("particles_bars_all.png",bbox_inches='tight')
    fig.savefig("particles_bars_all.pdf",bbox_inches='tight')
