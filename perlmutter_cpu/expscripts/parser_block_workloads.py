import numpy as np
from random import randint
from time import sleep
import time
import shutil
import os
import sys
import math
import json

def parse_block_workloads(trace_log_dir,num_ranks,num_blocks,stages_key_time_point):
    
    block_workloads_list=[]
    num_stages=len(stages_key_time_point)-1
    
    for i in range(0,num_blocks,1):
        block_workloads_list.append([])
        for s in range (0,num_stages,1):
            block_workloads_list[i].append(0)
    
        
    # go through each rank file
    # adding workloads into the corresponding block id
    adv_steps_sum=0
    for rankid in range(0,num_ranks,1):
        trace_file=trace_log_dir+"/timetrace."+str(rankid)+".out"
        fo=open(trace_file, "r")
        
        for line in fo:
            line_strip=line.strip()
            #ParticleAdvectInfo_3_983_34_1000_2_0 1.5751e+07
            #ParticleAdvectInfo_[gang size]_[total adv step]_[small step]_[prev gang size]_[block id]_[cycle] 1.5751e+07
            if "ParticleAdvectInfo" not in line_strip:
                continue
            
            adv_steps= int(line_strip.split(" ")[0].split("_")[2])
            block_id=int(line_strip.split(" ")[0].split("_")[5])
            adv_happen_time=(float(line_strip.split(" ")[1]))
            #print("adv_happen_time is ",adv_happen_time)
            adv_steps_sum=adv_steps_sum+adv_steps
            if block_id>=num_blocks:
                print("block_id is", block_id, "it should be less than num_ranks: ",num_blocks)
                exit(-1)
            
            # using adv_happen_time to decide where to put the bin
            for index in range(0,num_stages,1):
                if adv_happen_time>=stages_key_time_point[index] and adv_happen_time<stages_key_time_point[index+1]:
                    block_workloads_list[block_id][index]+=adv_steps
                    break
        
        fo.close()
        
    return block_workloads_list,adv_steps_sum



if __name__ == "__main__":

    if len(sys.argv)!=5:
        print("<binary> <dir for log> <num_ranks> <num_blocks> <num_stages>",flush=True)
        exit()

    actual_log_dir=sys.argv[1]
    num_ranks=int(sys.argv[2])
    num_blocks=int(sys.argv[3])
    num_stages=int(sys.argv[4])

    # compute key breaking points for dividing stages
    # get filter end time
    # get filter time, use the rank0's filter time as the total one
    file_name = actual_log_dir+"/timetrace."+str(0)+".out"
    fo=open(file_name, "r")
    filter_start_time=0.0
    filter_time=0
    filter_end="FilterEnd_"
    for line in fo:
        line_strip=line.strip()
        split_str= line_strip.split(" ")    
        if filter_end in line_strip:
            filter_end_time = float(split_str[1])
            print("filter_end_time",filter_end_time)
            filter_time = filter_end_time
    fo.close()

    print("filter_time",filter_time)

    time_length=math.ceil(filter_time/num_stages)

    stages_key_time_point=[0]
    for i in range(0,num_stages,1):
        stages_key_time_point.append((i+1)*time_length)    

    print("stages_key_time_point",stages_key_time_point)

    # get the list of block workloads
    block_workloads_list,adv_steps_sum=parse_block_workloads(actual_log_dir,num_ranks,num_blocks,stages_key_time_point)
    
    for i in range(0,num_blocks,1):
        for j in range(0,num_stages,1):
            block_workloads_list[i][j]=block_workloads_list[i][j]/adv_steps_sum
    
    # temp_sum=0
    # for i in range(0,num_blocks,1):
    #     for j in range(0,num_stages,1):
    #         temp_sum=temp_sum+block_workloads_list[i][j]

    # get normalized results and write out to json file
    
    # print("temp_sum",temp_sum)
    print ("block_workloads_list",block_workloads_list)

    with open("adv_step_stages_list.json", "w") as f:
        json.dump(block_workloads_list, f)