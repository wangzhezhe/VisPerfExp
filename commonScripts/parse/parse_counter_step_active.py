# check both the counter and the timetrace log
# to see how the active particle changes

from os import system
from os.path import exists
import sys
import statistics
import os
import matplotlib.pyplot as plt
import math

def check_active_num(file_path, step):
    local_active_particles_list=[]
    fo=open(file_path, "r")
    for line in fo:
        line_strip=line.strip()
        key_str="ParticleActive_"+str(step)
        if key_str in line_strip:
            split_str= line_strip.split(" ")
            active_particles=int(split_str[1])
            local_active_particles_list.append(active_particles)
    fo.close()
    return local_active_particles_list  

def check_active_time(file_path,step):
    local_active_particles_time=[]

    # start time
    go_start_str="GoStart_"+str(step)+" "
    
    # particle active
    particle_active_str="ParticleActiveTrace_"+str(step)+" "

    fo=open(file_path, "r")
    
    go_start_time=0

    for line in fo:
        line_strip=line.strip()
        split_str= line_strip.split(" ")
        
        if go_start_str in line_strip:
            # this should be the first timetrace
            go_start_time = int(split_str[1])

        if particle_active_str in line_strip:
            if go_start_time==0:
                raise Exception("go_start_time is not supposed to 0 here")  
            particle_active_relative_time=int(split_str[1])-go_start_time
            local_active_particles_time.append(particle_active_relative_time)

    fo.close()
    return local_active_particles_time  

def new_time_and_particles(time_list, particle_list, max_time):
    #print(time_list,particle_list)
    new_time = [0] * max_time
    new_particles = [0] * max_time

    for index, v in enumerate(new_time):
        new_time[index]=index
    
    current_active_particles=0
    index_original=0

    #go through each new_time slot
    #if there are specific particles
    #it is new particles
    #otherwise, it is same with old one
    #print("len time_list",len(time_list))
    for index, v in enumerate(new_time):
        #print(v,index_original,time_list[index_original])
        if v<time_list[index_original]:
            new_particles[index]=current_active_particles
        elif v==time_list[index_original]:
            new_particles[index]=particle_list[index_original]
            current_active_particles=particle_list[index_original]
            if index_original<len(time_list)-1:
                index_original=index_original+1
                while index_original<len(time_list)-1 and time_list[index_original]==time_list[index_original-1] :
                    # if there are redoundant time trace
                    # continue move
                    index_original=index_original+1
        else:
            # till the end of the time array
            new_particles[index]=0
            

    return new_time, new_particles



if __name__ == "__main__":
    
    if len(sys.argv)!=4:
        print("<binary> <procs> <step> <dirpath>")
        exit()
   
    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    step=sys.argv[2]
    dir_path=sys.argv[3]
    
    all_ranks_active_particles=[]
    all_ranks_active_timetrace=[]
    # go through each rank
    for rank in range(0,procs,1):
        counter_file_path = dir_path+"/counter."+str(rank)+".out"
        time_file_path = dir_path+"/timetrace."+str(rank)+".out"
        
        temp_particles_counter_list=check_active_num(counter_file_path,step)
        all_ranks_active_particles.append(temp_particles_counter_list)

        temp_particles_time_list=check_active_time(time_file_path,step)
        all_ranks_active_timetrace.append(temp_particles_time_list)

    #print(all_ranks_active_particles)
    if len(all_ranks_active_particles)!=procs:
        raise Exception("len(all_ranks_active_particles)!=procs")

    #print(all_ranks_active_timetrace)
    if len(all_ranks_active_timetrace)!=procs:
        raise Exception("len(all_ranks_active_timetrace)!=procs")

    
    fig, axs = plt.subplots(procs)

    max_x=0

    # compute the max x
    for rank in range(0,procs,1):
        max_x=max(max_x,max(all_ranks_active_timetrace[rank]))


    # plot the figure and using the timetrace as the x axis
    # make sure the sequence is same with the gant chart
    # the bottom one is rank zero
    # axs[0] is at the bottom
    new_x_list=[]
    new_y_list=[]
    for rank in range(0,procs,1):
        x=all_ranks_active_timetrace[procs-rank-1]
        y=all_ranks_active_particles[procs-rank-1]

        if len(x)!=len(y):
            raise Exception("#timetrace is supposed to equal #active_particles")
        
        # test
        new_x,new_y=new_time_and_particles(x,y,max_x)
        new_x_list.append(new_x)
        new_y_list.append(new_y)
        
        if rank==0:
            print(x,y)
            print(new_x,new_y)
        
        #print(procs-rank-1)
        #print("time",x)
        #print("active particles",y)
        #print("rank",procs-rank-1)
        #print("time\n", x[0:range])
        #print("active particles\n",y[0:range])
        axsindex=rank
        #the 0 axsindex is at the top of the figure
        #make the width as a large number
        #otherwise, the bar might be to thin and we can not see it
        axs[axsindex].set_xlim(-20, max_x)
        #axs[axsindex].bar(x, y, width=8)
        #axs[axsindex].plot(x, y)
        axs[axsindex].bar(new_x, new_y, width=1)

        axs[axsindex].set_ylabel("R"+str(procs-rank-1))
        
        axs[axsindex].tick_params(labelleft=False)
        axs[axsindex].set_yticklabels([])
        #remove that small tick line
        axs[axsindex].yaxis.set_ticks_position('none')

        # the bottom one
        if axsindex==procs-1:
            axs[axsindex].set_xlabel('Time(ms)', fontsize="large")
        else:
            # do not set x labels for non zero case
            axs[axsindex].tick_params(labelbottom=False)

    fig.savefig('active_distribution_all.png')


    # sum figure
    #sum_y_list = [0] * max_x
 

    # create the bar graph, this means 100ms
    histogram_bin_size = 1
    number_bin = math.ceil(max_x/histogram_bin_size)

    print("histogram_bin_size",histogram_bin_size,"number_bin",number_bin)
    
    
    histogram_bin_value = [0] * number_bin
    histogram_bin_positions= [0] * number_bin
    for index, v in enumerate(histogram_bin_positions):
        histogram_bin_positions[index]=index

    # go though data in each ranks
    # put data in specific bin
    for rank in range(0,procs,1):
        #x=all_ranks_active_timetrace[rank]
        x=new_x_list[rank]
        for index, time in enumerate(x):
            bin_index=int(time/histogram_bin_size)
            histogram_bin_value[bin_index]+=new_y_list[rank][index]
            #print(time, bin_index)

    #print(histogram_bin_value)

    fig, ax = plt.subplots()
    ax.bar(histogram_bin_positions,histogram_bin_value)
    ax.set_xlabel('Index of the bin', fontsize="large")
    ax.set_ylabel('Number of active particles', fontsize="large")

    fig.savefig('active_histogram.png',bbox_inches='tight')
