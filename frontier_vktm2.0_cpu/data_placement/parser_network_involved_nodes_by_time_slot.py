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


if __name__ == "__main__":

    if len(sys.argv)!=4:
        print("<binary> <log dir> <proc num> <num of slots>",flush=True)
        exit()
    

    log_dir_path=sys.argv[1]
    num_rank=int(sys.argv[2])
    num_slots=int(sys.argv[3])


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
    
        involved_ranks.append(len(involved_block_ids))

        # store associated adjacent_matrix_num_particles
        adjacent_matrix_num_particles_array.append(adjacent_matrix_num_particles)

    print(involved_ranks)
    fig, ax = plt.subplots(figsize=(8,4))
    ax.set_ylabel('Involved number of processes', fontsize='large')
    ax.set_xlabel('Index of the time slot', fontsize='large')
    ax.plot( involved_ranks, '-', color='blue', marker='o')
    plt.savefig("number_involved_processes.png", bbox_inches='tight')

    # the x axis is the index of the slot
    # finding turning point? 
    # Simple way, the involved points becomes the 1/n of the origianl one
    turnning_point=0
    for i in range (1,len(involved_ranks),1):
        if involved_ranks[i] < 0.2 * involved_ranks[i-1]:
            print("turning point is", i, "start time is", slot_dist*i)
            turnning_point=i


    # compute the workload according to the coresponding adjacent map
    # assignt plans based on that, the other ranks are empty
    # assuming there is one turning point
    np.set_printoptions(threshold=np.inf)
    print(adjacent_matrix_num_particles_array[turnning_point])




