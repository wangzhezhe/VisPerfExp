import numpy
from random import randint
from time import sleep
import time
import matplotlib.pyplot as plt
import shutil
import os
import sys

# current assign plan is a list of list
# [[0],[1,2]] represent there are two occupied rank, rank 0 load block 0, rank 1 load block 1 and 2
def parse_log_get_adv_percentage(current_assign_plan, occupied_rank, dirPath):
# parse log and get advection percentage for each rank
    filter_time=0
    # get filter time, use the rank0's filter time as the total one
    file_name = dirPath+"/timetrace.0.out"
    fo=open(file_name, "r")
    acc_ratio_list=[]
    filter_end="FilterEnd_0"
    for line in fo:
        line_strip=line.strip()
        split_str= line_strip.split(" ")    
        if filter_end in line_strip:
            filter_end_time = float(split_str[1])
            filter_time = filter_end_time
    fo.close()
    print("filter_time",filter_time,flush=True)    # get filter execution time, use rank 0's log
     
    # only 0 to current_assign_plan-1 is occupied
    for rank in range(0,len(current_assign_plan),1):
        # open timetrace file
        file_name = dirPath+"/timetrace."+str(rank)+".out"
        #print(file_name)
        fo=open(file_name, "r")
        work_start="WORKLET_Start_0"
        work_end="WORKLET_End_0"
        work_start_time=0
        acc_work_time=0
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(" ")
            if work_start in line_strip:
                work_start_time=float(split_str[1])
            if work_end in line_strip:
                work_end_time = float(split_str[1])
                acc_work_time = acc_work_time+(work_end_time-work_start_time)
        fo.close()
        #print("acc work time ratio for rank", rank, acc_work_time/filter_time)
        #for each rank, add its work ratio into list
        blockid = current_assign_plan[rank]
        acc_ratio_list.append([blockid,acc_work_time/filter_time])

    return acc_ratio_list, filter_time
# parse the log of previous output and get new execution plan
def parse_log_get_new_plan(curr_plan, occupied_rank, dirPath):
    # compute the adv percentage for each rank
    acc_ratio_list, filter_time = parse_log_get_adv_percentage(curr_plan, occupied_rank,dirPath)
    # use current acc ratio to generate new assignment plan
    acc_ratio_list_sorted=sorted(acc_ratio_list, key=lambda x: x[1], reverse=True)

    print("acc_ratio_list_sorted",acc_ratio_list_sorted)

    # do assignment, long job first, set the upper limitation
    upper_limit = 0.6
    # the program just hangs there if there are too many blocks per rank
    # or the issue is caused by some irregular block assignment plan
    upper_blocks_per_rank=30

    local_blockids=[]
    whole_blockids=[]
    local_acc_value=0
    whole_acc_ratios=[]

    for acc_ratio in acc_ratio_list_sorted:
        #print(acc_ratio, local_acc_value)
        if (local_acc_value+acc_ratio[1]) <=upper_limit and (len(local_blockids)+len(acc_ratio[0]))<=upper_blocks_per_rank:
            # move blocks of this rank to current rank
            local_blockids=local_blockids+acc_ratio[0]
            local_acc_value=local_acc_value+acc_ratio[1]
        else:
            # push previous local_blockids to whole block list
            whole_blockids.append(local_blockids)
            whole_acc_ratios.append(local_acc_value)
            # consider current one
            local_blockids=[]
            # merge two list together
            local_blockids=local_blockids+acc_ratio[0]
            local_acc_value=acc_ratio[1]

        #print("local_blockids",local_blockids)
        #print("local_acc_value",local_acc_value)
        #print("whole_blockids", whole_blockids)

    if len(local_blockids)>0:
        find_place_to_insert=False
        # go through whole_acc_ratios to find a place to fit
        for index, current_acc_ratio in enumerate(whole_acc_ratios):
            #print("current_acc_ratio",current_acc_ratio)
            if current_acc_ratio+local_acc_value <=upper_limit: 
                #print("find one", index)
                whole_blockids[index]=whole_blockids[index]+local_blockids
                whole_acc_ratios[index]=whole_acc_ratios[index]+local_acc_value
                find_place_to_insert = True
                break

        # did not find a one that can fit, exit
        if find_place_to_insert==False:
            whole_blockids.append(local_blockids)

    print("whole_blockids", whole_blockids,flush=True)
    print("whole_acc_ratios",whole_acc_ratios,flush=True)

    # the whole_blockids is new plan
    return whole_blockids, filter_time

def write_assign_options(assignment_plan):
    f = open("assign_options.config",'w')
    for index, blocks in enumerate(assignment_plan):
        #print(index, blocks)
        if len(blocks)==0:
            f.write("\n")
            continue
        
        occupied_process=len(assignment_plan)+1
        for i, bid in enumerate(blocks):
            if i==0:
                f.write(str(bid))
            else:
                f.write(" "+str(bid))
        f.write("\n")

    for v in range(0,num_rank-len(assignment_plan),1):
        # print("append empty")
        f.write("\n")    
    f.close() 

    # adding one that are empty
    print("num_rank",num_rank, "len(assignment_plan)",len(assignment_plan),flush=True)

# if the percentage exceeds specific limiation, than move to a new process
# this will determine how many process will be used, using the greedy strategy here
if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("<binary> <runDirPath> <num_rank>",flush=True)
        exit()
    dirPath=sys.argv[1]
    num_rank=int(sys.argv[2])
    init_plan = []
    for i in range(0,num_rank,1):
        init_plan.append([i])
    curr_plan = init_plan
    # create the assignment plan
    write_assign_options(curr_plan)
    for i in range(0,10,1):
        # execute based on current plan
        # os.system('/bin/bash runtask.sh')
        os.system('/bin/bash runtask-summit.sh')

        updated_plan, filter_time = parse_log_get_new_plan(curr_plan,num_rank,dirPath)
        print("len of curr_plan", len(curr_plan) , "filter_time", filter_time, "fitness value",  len(curr_plan)*filter_time,flush=True)
        
        # using new plan
        write_assign_options(updated_plan)
        curr_plan = updated_plan