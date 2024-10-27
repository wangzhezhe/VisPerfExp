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


def get_involved_ranks(log_dir_path,num_slots):
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

        # init an adjacent table, the size is rank*rank
        adjacent_matrix_num_comm = np.zeros((num_rank, num_rank))
        adjacent_matrix_num_particles = np.zeros((num_rank, num_rank))
            
        # go through each rank to extract the dest list values

        for src_rank in range(0,num_rank,1):
            dest_rank_list_time,dest_rank_list_pnum=get_dst_rank_list(log_dir_path, src_rank, slot_start, slot_end)    
            for index, dest in enumerate(dest_rank_list_time):
                dest_rank=int(dest)
                adjacent_matrix_num_comm[src_rank][dest_rank]=adjacent_matrix_num_comm[src_rank][dest_rank]+1
                adjacent_matrix_num_particles[src_rank][dest_rank]=adjacent_matrix_num_particles[src_rank][dest_rank]+dest_rank_list_pnum[index]

        # calculate involved data values according to adjacent tables
        involved_block_ids=set()
        for i in range(0,num_rank,1):
            for j in range(0,num_rank,1):
                if(adjacent_matrix_num_comm[i][j]>0):
                    involved_block_ids.add(i)
                    involved_block_ids.add(j)
        num_involved_proc=len(involved_block_ids)
        if num_involved_proc==0:
            # no sending operation during this period of time
            num_involved_proc=1
        involved_ranks.append(num_involved_proc)

        # store associated adjacent_matrix_num_particles
        adjacent_matrix_num_particles_array.append(adjacent_matrix_num_particles)

    #print(involved_ranks)
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
        num_involved_rank=get_involved_ranks(log_dir,num_slots)
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
    plt.savefig("number_involved_processes_all.png", bbox_inches='tight')





