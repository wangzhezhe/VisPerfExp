import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

def get_actual_run_info(file_name):
    print("actual data parse file name",file_name)
    fo=open(file_name, "r")
    actual_acc_advect_steps_popularity=[]

    for line in fo:
        line_strip=line.strip()
        #print(line_strip)
        if "actual_acc_advect_steps_popularity" in line_strip:
            start =line_strip.find("[")
            end=line_strip.find("]")
            extract_num = line_strip[start+1:end-1]
            split_line = extract_num.split(",")
            #print(split_line)
            actual_acc_advect_steps_popularity = [float(v) for v in split_line]


    fo.close()

    return actual_acc_advect_steps_popularity

def get_estimated_info(file_name):
    print("est file name",file_name)
    fo=open(file_name, "r")
    estimator_steps_popularity_list=[]
    estimator_particle_in_list=[]
    estimator_particle_out_list=[]

    for line in fo:
        line_strip=line.strip()
        #print(line_strip)
        if "NormBlockPopularity" in line_strip:
            start =line_strip.find("[")
            end=line_strip.find("]")
            extract_num = line_strip[start+1:end-1]
            split_line = extract_num.split(",")
            #print(split_line)
            estimator_steps_popularity_list = [float(v) for v in split_line]

        if "ParticlesIn" in line_strip:
            start =line_strip.find("[")
            end=line_strip.find("]")
            extract_num = line_strip[start+1:end-1]
            split_line = extract_num.split(",")
            #print(split_line)
            estimator_particle_in_list = [float(v) for v in split_line]

        if "ParticlesOut" in line_strip:
            start =line_strip.find("[")
            end=line_strip.find("]")
            extract_num = line_strip[start+1:end-1]
            split_line = extract_num.split(",")
            #print(split_line)
            estimator_particle_out_list = [float(v) for v in split_line]

    fo.close()

    if len(estimator_steps_popularity_list)==0:
        print("No NormBlockPopularity log")
        exit(0)

    return estimator_steps_popularity_list,estimator_particle_in_list,estimator_particle_out_list

def put_workload_into_bin_2(estimated_block_popularity,remaining_space_list,block_list_for_proc):
    index=0
    while (len(estimated_block_popularity)>0):
        # there are blocks
        # get one
        block_id=estimated_block_popularity[0][0]
        bin_popularity=estimated_block_popularity[0][1]

        # pop out first element
        estimated_block_popularity.pop(0)

        print("block_id",block_id)
        print("bin_popularity",bin_popularity)

        # bin_remaining_space_list, check if find the avalible space
        find_bin=False
        max_remaining_space=0
        for bin_index, bin_remaining in enumerate(remaining_space_list):
            # avoid some edge case, the smaller one might be duplicated multiple times since
            # the remaining space becomes so small
            if (bin_remaining>=bin_popularity):

                find_bin=True
                remaining_space_list[bin_index]-=bin_popularity
                block_list_for_proc[bin_index].append(block_id)
                break
        
        if find_bin==False:
            # after going through all spaces, there are still no avalible spaces
            # duplicate current workload
            estimated_block_popularity.insert(0,[block_id,bin_popularity/2.0])
            estimated_block_popularity.insert(0,[block_id,bin_popularity/2.0])

        print("estimated_block_popularity end",estimated_block_popularity)
        print("block_list_for_proc",block_list_for_proc)
        print("remaining_space_list",remaining_space_list)
        index+=1
        #if index == 100:
        #    break    
    return

def put_workload_into_bin(estimated_adv_popularity,remaining_space_list,avg_bin_size):
    unfitted_block=[]
    for bin_info in estimated_adv_popularity:
        bin_popularity = bin_info[1]
        block_id = bin_info[0]
        #find a bin for current block_id
        #go through all bin_remaining_space_list, find one that can hold current bin
        find_bin=False
        for bin_index, bin_remaining in enumerate(remaining_space_list):
            # when we looks at the new bin, the package size 
            # is larger than bin size
            if (bin_remaining<bin_popularity):
                if (abs(bin_remaining-avg_bin_size)<0.0000001):
                    block_list_for_proc[bin_index].append(block_id)
                    # update space
                    remaining_space_list[bin_index]-=bin_popularity
                    find_bin=True
                    break    
            
            # if there is enough space
            if bin_remaining>=bin_popularity:
                # put block into associated bins
                block_list_for_proc[bin_index].append(block_id)
                # update space
                remaining_space_list[bin_index]-=bin_popularity
                find_bin=True
                break
        if find_bin==False:
            print("Warning! failed to find bin for bin_popularity",bin_popularity,"curr bin_remaining",bin_remaining, "bin_remaining_space_list",bin_remaining_space_list)
            # duplicate the work according to the lagest bin size
            # store these blocks separately
            unfitted_block.append(bin_info)

    return unfitted_block


# compute the networking connectivity between all ranks
# parser algorithmRecorder.<rank>.out
def get_dst_rank_list(log_dir_path, rank, start_time, end_time):
    file_name = log_dir_path+"/one_data_per_rank/algorithmRecorder."+str(rank)+".out"
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

# identify start and end time
# divide into several time slots
# compute the involved ranks
# compute the drop point
# return the drop point, there might be multiple ones
# the number of rank sould equals numer of blocks here
def identify_blocks_after_turning_point(num_bins, num_rank, log_dir_path):

    file_name = log_dir_path+"/one_data_per_rank/timetrace."+str(0)+".out"
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

    print("filter_end_time",filter_end_time)

    slot_dist=filter_end_time/num_bins

    involved_ranks=[]

    adjacent_matrix_num_particles_array=[]

    # go through each slot
    # the list store global matrix results
    adjacent_matrix_num_comm_list=[]
    adjacent_matrix_num_particles_list=[]

    for i in range (0,num_bins,1):
        slot_start=i*slot_dist
        slot_end=i*slot_dist+slot_dist

        #print(slot_start,slot_end)

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
        
        adjacent_matrix_num_comm_list.append(adjacent_matrix_num_comm)
        adjacent_matrix_num_particles_list.append(adjacent_matrix_num_particles)

        involved_ranks.append(len(involved_block_ids))   
    
    print("involved_ranks",involved_ranks)
    turnning_point_index=0
    for i in range (1,len(involved_ranks),1):
        if involved_ranks[i] < 0.2 * involved_ranks[i-1]:
            print("turning point is", i, "start time is", slot_dist*i)
            turnning_point_index=i

    adjacent_matrix_num_particles_s2=np.zeros((num_rank, num_rank))
    for i in range(turnning_point_index,num_bins,1):
        adjacent_matrix_num_particles_s2=np.add(adjacent_matrix_num_particles_s2,adjacent_matrix_num_particles_list[i])
    
    # extracting [bid, workload] list from adjacent_matrix_num_particles_s2
    adjacent_matrix_num_particles_s2_sum=adjacent_matrix_num_particles_s2.sum(axis=0)
    #print("adjacent_matrix_num_particles_s2_sum",adjacent_matrix_num_particles_s2_sum)
    adjacent_matrix_num_particles_s2_sum_norm=adjacent_matrix_num_particles_s2_sum/sum(adjacent_matrix_num_particles_s2_sum)

    list_stage2=[]
    for blockid in range(0,num_rank,1):
        if adjacent_matrix_num_particles_s2_sum[blockid]>0:
            list_stage2.append(blockid)

    return list_stage2


# the workload list contains a series of [blockid, workload value]
# the workload value is normalized value
def get_assignment_plan_from_workload_list(workload_list, avalible_procs):
    block_list_for_proc=[]
    bin_remaining_space_list=[]
    factor=1.01
    avg_bin_size = factor*1.0/(1.0*avalible_procs)
    
    # init the bin_remaining_space_list
    for i in range(0,avalible_procs,1):
        bin_remaining_space_list.append(avg_bin_size)
        block_list_for_proc.append([])

    index=0
    while (len(workload_list)>0):
        # there are blocks
        # get one
        block_id=workload_list[0][0]
        bin_popularity=workload_list[0][1]

        # pop out first element
        workload_list.pop(0)

        # print("block_id",block_id)
        # print("bin_popularity",bin_popularity)

        # bin_remaining_space_list, check if find the avalible space
        find_bin=False
        max_remaining_space=0
        for bin_index, bin_remaining in enumerate(bin_remaining_space_list):
            # avoid some edge case, the smaller one might be duplicated multiple times since
            # the remaining space becomes so small
            if (bin_remaining>=bin_popularity):

                find_bin=True
                bin_remaining_space_list[bin_index]-=bin_popularity
                block_list_for_proc[bin_index].append(block_id)
                break
        
        if find_bin==False:
            # after going through all spaces, there are still no avalible spaces
            # duplicate current workload
            workload_list.insert(0,[block_id,bin_popularity/2.0])
            workload_list.insert(0,[block_id,bin_popularity/2.0])

        # print("estimated_block_popularity end",workload_list)
        # print("block_list_for_proc",block_list_for_proc)
        # print("remaining_space_list",bin_remaining_space_list)
        index+=1
        #if index == 100:
        #    break    

    print("block_list_for_proc",block_list_for_proc)
    return block_list_for_proc


def merge_block_list(block_list_for_proc1,block_list_for_proc2):
    merged_block_list=[]
    if len(block_list_for_proc1)!=len(block_list_for_proc2):
        print("two block list should be equal")
        return merged_block_list
    for i in range(0,len(block_list_for_proc1),1):
        set1=set(block_list_for_proc1[i])
        set2=set(block_list_for_proc2[i])
        merged_set=set1.union(set2)
        merged_block_list.append(list(merged_set))

    return merged_block_list


# divide things into multiple stages
# try to identify these stages
# make sure block id list for each stage and associated ranks
# generate assignment plans
# combine assigment plans

if __name__ == "__main__":

    if len(sys.argv)!=7:
        print("<binary> <workload estimation log> <block num> <original proc num> <estmate proc num> <num bins> <actual_parse_log>",flush=True)
        exit()

    workload_estimation_log = sys.argv[1]
    block_num=int(sys.argv[2])
    # the number of procs we want to put the bin into
    original_proc_num=int(sys.argv[3])
    intransit_proc_num=int(sys.argv[4])
    num_bins = int(sys.argv[5])
    actual_parse_log=sys.argv[6]
    
    print("workload_estimation_log",workload_estimation_log,"block_num",block_num,"origianl proc num",original_proc_num, "intransit_proc_num proc num", intransit_proc_num, "num bins",num_bins)

    # original dup based assignment
    actual_adv_popularity=get_actual_run_info(actual_parse_log)
    print("actual_adv_popularity")
    print(actual_adv_popularity)

    bin_remaining_space_list=[]
    block_list_for_proc=[]
    
    #make bin size a little bit larger than avg
    #other wise, the last one might be duplicated for many times
    factor=1.01
    avg_bin_size = factor*1.0/(1.0*original_proc_num)
    
    # init the bin_remaining_space_list
    for i in range(0,original_proc_num,1):
        bin_remaining_space_list.append(avg_bin_size)
        block_list_for_proc.append([])
    
    print ("init status bin_remaining_space_list", bin_remaining_space_list, "block_list_for_proc", block_list_for_proc)

    # sorting the list, using the first-fit decreasing
    # if the largest popularity is larger than the average bin size
    # just mark assign a separate bin for that block
    # sort the estimated_adv_popularity with the block id

    adv_popularity_for_sorting = [] 
    
    for index, popularity in enumerate(actual_adv_popularity):
        adv_popularity_for_sorting.append([index,popularity])

    #print(estimated_adv_popularity_for_sorting)

    # sorting list according to the second popularity
    sorted_adv_popularity=sorted(adv_popularity_for_sorting, key=lambda x: x[1], reverse=True)

    print("sorted_adv_popularity:", sorted_adv_popularity)
    
    original_block_list_for_proc=get_assignment_plan_from_workload_list(sorted_adv_popularity,intransit_proc_num)

    # identify the block that located in ping pong region

    # redistribute these few blocks to others

    # num_bins, filter_end_time, log_dir_path
    long_running_blocks=identify_blocks_after_turning_point(num_bins,block_num,workload_estimation_log)
    

    print("original_block_list_for_proc",original_block_list_for_proc)

    print("long_running_blocks",long_running_blocks)
    
    index=0
    for i in range (0,len(original_block_list_for_proc),1):
        temp_list=original_block_list_for_proc[i]
        # if elements in long_running_blocks is in templist
        # continue
        contain_bid=False
        for bid in long_running_blocks:
            if bid in temp_list:
                contain_bid=True
                break
        if contain_bid==False:
            index=index%len(long_running_blocks)
            original_block_list_for_proc[i].append(long_running_blocks[index])
            index=(index+1)

    print("updated original_block_list_for_proc",original_block_list_for_proc)
    # TODO, merge long_running_blocks into original_block_list_for_proc

    outputfile = "assign_options.config"
    with open(outputfile, 'w') as f:
        for block_list in original_block_list_for_proc:
            # for each block
            index = 0
            for block in block_list:
                if index>0:
                    f.write(" "+str(block))
                else:
                    f.write(str(block))
                index+=1
            f.write('\n')