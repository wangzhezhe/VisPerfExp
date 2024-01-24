import numpy
from random import randint
from time import sleep
import time
import matplotlib.pyplot as plt
import shutil
import os
import sys
# the source code come from
# 

#function_inputs = range(0,num_rank,1) # Function inputs. from 0 to n-1
# we do not need function input here, this is just a synthetic value
function_inputs = 0
desired_output = 0 # Function output.
global num_rank
# https://stackoverflow.com/questions/8713620/appending-to-one-list-in-a-list-of-lists-appends-to-all-other-lists-too
# be carefule of this, modify one, modify all
# generate assignment config from solution plan, and then execute the function, and get associated execution times
def get_exec_time(solution_plan):
    # print("function_inputs:", function_inputs)
    # run the particle advection to get exec time
    # psudu code, sleep random time
    start = time.time()
    # sleep(randint(1,3)/1000)
    # generate a assign_options.config according to input
    assignment_list=[[] for _ in range(len(solution_plan))]
    for index, v in enumerate(solution_plan):
        #print(index, v)
        #the value generated by generic algorithm might not be integer
        if (int(v)>(num_rank-1)):
            assignment_list[num_rank-1].append(index)
        else:
            assignment_list[int(v)].append(index)
    print("assignment_list is", assignment_list)

    # write out plan
    occupied_process=0
    f = open("assign_options.config",'w')
    for index, blocks in enumerate(assignment_list):
        #print(index, blocks)
        if len(blocks)==0:
            f.write("\n")
            continue
        
        occupied_process=occupied_process+1
        for i, bid in enumerate(blocks):
            if i==0:
                f.write(str(bid))
            else:
                f.write(" "+str(bid))
        f.write("\n")
    # call the particle advection based on plan
    os.system('/bin/bash runtask.sh')
    
    end = time.time()
    exec_time = end-start
    return exec_time,occupied_process

def fitness_func(ga_instance, solution, solution_idx):
    print("solution",solution)
    #exec_time, occupied_process = get_exec_time(solution)

    #synthetic option
    exec_time = 1+randint(1,3)
    occupied_process=2+randint(1,3)/1000
    sleep(randint(1,3)/1000)
    # count occupied process
    core_time=exec_time*occupied_process
    print("exec_time",exec_time,"occupied_process",occupied_process)
    fitness = 1.0 / numpy.abs(core_time - desired_output + 0.001)
    return fitness

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
    print("filter_time",filter_time)    # get filter execution time, use rank 0's log
    
    for rank in range(0,occupied_rank,1):
        # open timetrace file
        file_name = dirPath+"/timetrace."+str(rank)+".out"
        #print(file_name)
        fo=open(file_name, "r")
        work_start="WORKLET_Start_0"
        work_end="WORKLET_End_0"
        work_start_time=0
        acc_work_time=0
        fo=open(file_name, "r")
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
    acc_ratio_list, filter_time = parse_log_get_adv_percentage(init_plan, occupied_rank,dirPath)
    # use current acc ratio to generate new assignment plan
    acc_ratio_list_sorted=sorted(acc_ratio_list, key=lambda x: x[1], reverse=True)

    print(acc_ratio_list_sorted)

    # do assignment, long job first, set the upper limitation
    upper_limit = 0.8

    local_blockids=[]
    whole_blockids=[]
    local_acc_value=0
    whole_acc_ratios=[]

    for acc_ratio in acc_ratio_list_sorted:
        #print(acc_ratio, local_acc_value)
        if (local_acc_value+acc_ratio[1]) <=upper_limit:
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

    print("whole_blockids", whole_blockids)
    print("whole_acc_ratios",whole_acc_ratios)

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

    # adding one that are empty
    print("num_rank",num_rank, "len(assignment_plan)",len(assignment_plan))
    for v in range(0,num_rank-len(assignment_plan),1):
        # print("append empty")
        f.write("\n")
    f.close() 
    
    f.close() 

# if the percentage exceeds specific limiation, than move to a new process
# this will determine how many process will be used, using the greedy strategy here
if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("<binary> <runDirPath> <num_rank>")
        exit()
    dirPath=sys.argv[1]
    num_rank=int(sys.argv[2])
    init_plan = [[0],[1],[2],[3],[4],[5],[6],[7]]
    curr_plan = init_plan
    # create the assignment plan
    write_assign_options(curr_plan)
    for i in range(0,5,1):
        # execute based on current plan
        os.system('/bin/bash runtask.sh')
        updated_plan, filter_time = parse_log_get_new_plan(curr_plan,num_rank,dirPath)
        # create assignment plan    
        print("len updated_plan", updated_plan , "filter_time", filter_time, "fitness value",  len(updated_plan)*filter_time)
        write_assign_options(updated_plan)

        curr_plan = updated_plan