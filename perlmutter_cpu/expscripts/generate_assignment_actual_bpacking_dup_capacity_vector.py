import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import json 
import random

# divide things into multiple stages
# try to identify these stages
# make sure block id list for each stage and associated ranks
# generate assignment plans
# combine assigment plans

if __name__ == "__main__":
    
    # TODO, adding maximum number of blocks for each rank
    # this value need to be less than 15
    # how to add this constraints?
    MaxNumBlocks=15
    if len(sys.argv)!=4:
        print("<binary> <block num> <intransit_proc_num> <adv stages list log>",flush=True)
        exit()
    
    # this info is not used in this script now
    block_num=int(sys.argv[1])
    # the number of procs we want to put the bin into
    original_proc_num=block_num # block num should equal to original proc num
    intransit_proc_num=int(sys.argv[2])
    adv_stages_list=sys.argv[3]
    
    print("block_num",block_num,"origianl proc num",original_proc_num, "intransit_proc_num proc num", intransit_proc_num, "adv_stages_list",adv_stages_list)
    
    # load the adv stages list
    with open("adv_step_stages_list.json", "r") as f:
         loaded_list = json.load(f)
            
    #print("loaded_list",loaded_list)
    
    num_stages=len(loaded_list[0])
    num_stages_total=[]
    
    #print("num_stages",num_stages)

    for i in range(0,num_stages,1):
        stage_total_popularity=0
        for j in range(0,block_num,1):
            stage_total_popularity=stage_total_popularity+float(loaded_list[j][i])
        num_stages_total.append(stage_total_popularity)
    
    # how much popularity for each dim
    print(num_stages_total)
    
    # total popularity for each stage
    bin_factor=1.2
    avg_capacity=(np.array(num_stages_total)/intransit_proc_num)*bin_factor

    # init avalible capacity
    print(avg_capacity)

    # init remaining_capacity_list
    # the length is the number of blocks
    # each value contains an avg value
    # Be careful, each bin should contains 1/intransit_proc_num workload in avg
    # instead of the number of blocks/in situ ranks
    remaining_capacity_list=[]
    for i in range(0,intransit_proc_num,1):
        remaining_capacity_list.append([i,list(avg_capacity)])
    

    #print("remaining_capacity_list\n",remaining_capacity_list)
    # give block id to loaded_list
    # this is actually a stack, we use the list to simulate it
    popularity_list_with_id=[]

    for i in range(0,block_num,1):
        popularity_list_with_id.append([i,loaded_list[i]])
    
    # sorting popularity_list_with_id according their total popularity
    # otherwise, there is issue for putting large bin
    # if there is tiny space, and there comes large bin, we need to divide it small workloads
    # too many times
    sorted_adv_popularity=sorted(popularity_list_with_id, key=lambda x: sum(x[1]), reverse=True)

    #print(sorted_adv_popularity)

    # try to assign blocks
    block_list_for_proc=[]
    
    for i in range(0,intransit_proc_num,1):
        block_list_for_proc.append([])

   
    index=0
    list_start_pos=0

    many_repeated_id=set()
    while(len(sorted_adv_popularity)>0):
        # get one
        #print("\nlen(sorted_adv_popularity)",len(sorted_adv_popularity))
        #print("sorted_adv_popularity\n",sorted_adv_popularity)
        #print("remaining_capacity_list\n",remaining_capacity_list)

        block_id=sorted_adv_popularity[0][0]
        block_popularity=sorted_adv_popularity[0][1]

        # print("debug block_id",block_id, "block_popularity",block_popularity)
        # pop out first element
        sorted_adv_popularity.pop(0)
        find_bin=False
        # shuffle remaining_capacity_list?
        # random.shuffle(remaining_capacity_list)
        # for item in (station_list[start:] + station_list[:start]) 
        for capacity_info in (remaining_capacity_list[list_start_pos:]+remaining_capacity_list[:list_start_pos]):
            # avoid some edge case, the smaller one might be duplicated multiple times since
            # the remaining space becomes so small
            # for each component
            bin_index = capacity_info[0]
            bin_remaining_vector = capacity_info[1]
            # check if there are enough blocks
            if len(block_list_for_proc[bin_index])>=MaxNumBlocks:
                continue

            for i in range(0,num_stages,1):
                if (bin_remaining_vector[i]>block_popularity[i]) or (block_popularity[i]<0.00001) :
                    find_bin=True
                    continue
                else:
                    # once there is one disqualified, the result is false
                    find_bin=False
                    break
            
            if(find_bin==False):
                # current bin is not suitable
                # jump to next one
                continue
            else:
                # find one block, put it into the block list
                # update the remaning vector 
                # if the block have been assigned to one block, skip the current block_list_for_proc
                if block_id in block_list_for_proc[bin_index]:
                    #we have loaded this block in this rank
                    continue

                for i in range(0,num_stages,1):
                    bin_remaining_vector[i]-=block_popularity[i]

                block_list_for_proc[bin_index].append(block_id)
                # find one slot, do not need to search
                break
        
        # not find for current block after iterating all remaning bins
        # do the splitting
        if find_bin==False:
            # after going through all spaces, there are still no avalible spaces
            # duplicate current workload
            
            # if laste splitted block did not find a proper position
            # there are three splitted blocks with same id
            # do not split further, just use the sum of workloads
            
            
            if(len(sorted_adv_popularity)>=3):
                if(block_id==sorted_adv_popularity[0][0]==sorted_adv_popularity[1][0]==sorted_adv_popularity[2][0]):
                    many_repeated_id.add(block_id)
            
            if block_id in many_repeated_id:
                for capacity_info in (remaining_capacity_list[list_start_pos:]+remaining_capacity_list[:list_start_pos]):
                    bin_index = capacity_info[0]
                    bin_remaining_vector = capacity_info[1]
                    # check if there are enough blocks
                    if len(block_list_for_proc[bin_index])>=MaxNumBlocks:
                        continue
                    
                    if sum(bin_remaining_vector) > sum(block_popularity) or sum(block_popularity)<0.00001:
                        # find block
                        if block_id in block_list_for_proc[bin_index]:
                            continue
                        for i in range(0,num_stages,1):
                            bin_remaining_vector[i]-=block_popularity[i]
                        block_list_for_proc[bin_index].append(block_id)
                        break
            else:            
                #print("splitting block",block_id)
                block_popularity_splitting=[]
                for i in range(0,num_stages,1):
                    block_popularity_splitting.append(block_popularity[i]/2.0)

                sorted_adv_popularity.insert(0,[block_id,block_popularity_splitting])
                sorted_adv_popularity.insert(0,[block_id,block_popularity_splitting])

        index=index+1

        
        list_start_pos=(list_start_pos+1)%len(remaining_capacity_list)    

        
        #if(index==300):
        #    break

    print("block_list_for_proc\n",block_list_for_proc)
    # write out assignment plan
    outputfile = "assign_options.config"
    with open(outputfile, 'w') as f:
        for block_list in block_list_for_proc:
            # for each block
            index = 0
            for block in block_list:
                if index>0:
                    f.write(" "+str(block))
                else:
                    f.write(str(block))
                index+=1
            f.write('\n')