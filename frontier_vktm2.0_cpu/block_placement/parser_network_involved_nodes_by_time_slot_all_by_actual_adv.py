import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

# compute the networking connectivity between all ranks
# parser algorithmRecorder.<rank>.out
def get_dst_rank_list(log_dir_path, rank, start_time, end_time):
    file_name = log_dir_path+"/algorithmRecorder."+str(rank)+".out"
    #print("est file name",file_name)
    fo=open(file_name, "r")
    dest_rank_list=[]
    dest_rank_list_pnum=[]

    for line in fo:
        line_strip=line.strip()
        #print(line_strip)
        if "SEND_PARTICLES_rank_np" in line_strip:
            # sample input [9:82,6:3,]
            split_info = line_strip.split(",")
            #print(split_info)
            #print(float(split_info[2]))
            send_time = float(split_info[0])
            # not at the start end time slot
            if(send_time<start_time or send_time>end_time):
                continue
            num_dest = int((len(split_info) - 2)/2)
            #print("num_dest",num_dest)
            for i in range(0,num_dest,1):
                dest_rank_list.append(int(split_info[2+i*2]))
                dest_rank_list_pnum.append(int(split_info[2+i*2+1]))

    return dest_rank_list,dest_rank_list_pnum

def get_num_advec_proc_in_this_period(slot_start,slot_end,log_dir_path,num_rank):
    num_involved=0
    # go through each rank
    # if there advection operation during this period of time
    # add it to num_involved
    for rankid in range(0,num_rank):
        # check this rank
        file_name = log_dir_path+"/timetrace."+str(rankid)+".out"
        print(file_name)
        fo=open(file_name, "r")
        for line in fo:
            line_strip=line.strip()
            worklet_start_time=-1
            worklet_end_time=-1
            if "WORKLET_Start" in line_strip:
                split_info = line_strip.split(" ")
                worklet_start_time = float(split_info[1])
                #print("worklet_start_time",worklet_start_time)
                if worklet_start_time>slot_end:
                    break

            if "WORKLET_End" in line_strip:
                split_info = line_strip.split(" ")
                worklet_end_time = float(split_info[1])
                #print("worklet_end_time",worklet_end_time)
                if worklet_end_time<slot_start:
                    #print("break",worklet_end_time,slot_start)
                    continue                    
                
                # we got start and end and there is overlapping
                num_involved=num_involved+1
                #print("num_involved",num_involved)
                break

        fo.close()
    return num_involved

def get_involved_ranks(log_dir_path,num_slots,num_rank):
    print("---process log_dir_path",log_dir_path)

    # get the end time
    file_name = log_dir_path+"/timetrace."+str(0)+".out"
    fo=open(file_name, "r")
    filter_start_time=0.0
    filter_end="FilterEnd_"+str(0)+" "
    for line in fo:
        line_strip=line.strip()
        split_str= line_strip.split(" ")    
        if filter_end in line_strip:
            filter_end_time = float(split_str[1])
            filter_time = filter_end_time
    fo.close()

    print("filter_time",filter_time)

    slot_dist=filter_time/num_slots

    involved_ranks=[]

    adjacent_matrix_num_particles_array=[]

    # go through each slot
    for i in range (0,num_slots,1):
        slot_start=i*slot_dist
        slot_end=i*slot_dist+slot_dist

        print(slot_start,slot_end)
        
        # get number of ranks that has work during this period of time
        num_involved_proc = get_num_advec_proc_in_this_period(slot_start,slot_end,log_dir_path,num_rank)
    
        involved_ranks.append(num_involved_proc)

    print(involved_ranks)
    return involved_ranks




if __name__ == "__main__":

    if len(sys.argv)!=1:
        print("<binary>",flush=True)
        exit()
    

    num_rank=32
    num_slots=10
    result_dir = "/Users/zhewang/Documents/Research/PaperSubmission/BlockAssignments/VisPerfStudy/Results/"
    dir_list=[result_dir+"VisPerfExpSl2_Astro244_Rank32_Nxyz1_0731/one_data_per_rank",
             result_dir+"VisPerfExpSl2_Clover244_Rank32_Nxyz1_0731/one_data_per_rank",
             result_dir+"VisPerfExpSl2_Isabel244_Rank32_Nxyz1_0731/one_data_per_rank",
             result_dir+"VisPerfExpSl2_Redsea442_Rank32_Nxyz1_0731/one_data_per_rank"]
    


    num_involved_rank_all=[]

    for log_dir in (dir_list):
        num_involved_rank=get_involved_ranks(log_dir,num_slots,num_rank)
        #print(num_involved_rank)
        num_involved_rank_all.append(num_involved_rank)

    print(num_involved_rank_all)

    fig, ax = plt.subplots(figsize=(8,4))
    labelsize = 18
    ticksize = 16
    ax.set_ylabel('Involved number of processes', fontsize=labelsize)
    ax.set_xlabel('Index of the time segment', fontsize=labelsize)
    # set tick size

    p1=ax.plot(num_involved_rank_all[0], '-', color='blue', marker='.', label="Supernova")
    p2=ax.plot(num_involved_rank_all[1], '-', color='red', marker='.', label="CloverLeaf")
    p3=ax.plot(num_involved_rank_all[2], '-', color='purple', marker='.',label="Isabel")
    p4=ax.plot(num_involved_rank_all[3], '-', color='green', marker='.',label="RedSea")
    
    # Set tick size for the x-axis only
    plt.tick_params(axis='x', labelsize=ticksize)
    # Set tick size for the y-axis only
    plt.tick_params(axis='y', labelsize=ticksize)

    plt.ylim(0,38)

    plt.legend(ncol=4, fontsize='large', loc="upper center")
    plt.savefig("number_involved_processes_all_adv.png", bbox_inches='tight')





