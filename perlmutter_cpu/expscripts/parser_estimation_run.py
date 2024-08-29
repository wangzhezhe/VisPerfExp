import numpy as np
from random import randint
from time import sleep
import time
import shutil
import os
import sys
import math

import matplotlib.pyplot as plt
import json



# stages time should be [0,t1,t2...filterend time]
def parse_log_get_acc_advect_steps_stages(log_dir_path,num_rank,stages_key_time_point):
    
    acc_adv_step_list=[]
    acc_adv_step_list_with_rankid=[]
    for rank in range(0,num_rank):
        sum_adv_steps_per_rank=0
        adv_steps_satges=[]
        number_stages=len(stages_key_time_point)-1
        for i in range(number_stages):
            adv_steps_satges.append(0)

        file_name = log_dir_path+"/timetrace."+str(rank)+".out"
        fo=open(file_name, "r")
        for line in fo:
            line_strip=line.strip()
            if "ParticleAdvectInfo" not in line_strip:
                continue
            adv_steps = int(line_strip.split(" ")[0].split("_")[2])
            adv_end_time_str=line_strip.split(" ")[1]
            #print("debug",adv_steps)
            # for 1e5, we need to convert it to float firstly, then to int
            adv_end_time = int(float(adv_end_time_str))
            # put adv steps into coresponding stages bin
            for i in range(0,number_stages,1):
                #print("debug",adv_end_time,stages_key_time_point[i],stages_key_time_point[i+1])
                if(adv_end_time>=stages_key_time_point[i] and adv_end_time<stages_key_time_point[i+1]):
                    adv_steps_satges[i]=adv_steps_satges[i]+adv_steps

        acc_adv_step_list.append(adv_steps_satges)
        acc_adv_step_list_with_rankid.append([rank,adv_steps_satges])
        fo.close()
    return acc_adv_step_list,acc_adv_step_list_with_rankid


# if one block one rank, the block id is the rank id
def parse_log_get_acc_advect_steps(log_dir_path,num_rank):
    acc_adv_step_list=[]
    acc_adv_step_list_with_rankid=[]
    for rank in range(0,num_rank):
        total_adv_steps=0        
        file_name = log_dir_path+"/timetrace."+str(0)+".out"
        fo=open(file_name, "r")
        for line in fo:
            line_strip=line.strip()
            if "ParticleAdvectInfo" not in line_strip:
                continue
            adv_steps= int(line_strip.split(" ")[0].split("_")[2])

            total_adv_steps=total_adv_steps+adv_steps
        acc_adv_step_list.append(total_adv_steps)
        acc_adv_step_list_with_rankid.append([rank,total_adv_steps])
        fo.close()
    return acc_adv_step_list,acc_adv_step_list_with_rankid

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

def get_actual_in_out_number(actual_log_dir_path, num_rank):
    # get the end time
    file_name = actual_log_dir_path+"/timetrace."+str(0)+".out"
    fo=open(file_name, "r")
    filter_start_time=0.0
    filter_time=0
    filter_end="FilterEnd_"+str(0)+" "
    for line in fo:
        line_strip=line.strip()
        split_str= line_strip.split(" ")    
        if filter_end in line_strip:
            filter_end_time = float(split_str[1])
            filter_time = filter_end_time
    fo.close()

    print("filter_time",filter_time)

    # calculate in(sum of column value) and out(sum of the row value) for each rank
    adjacent_matrix_num_comm = np.zeros((num_rank, num_rank))
    adjacent_matrix_num_particles = np.zeros((num_rank, num_rank))
            
    # go through each rank to extract the dest list values

    for src_rank in range(0,num_rank,1):
        dest_rank_list_time,dest_rank_list_pnum=get_dst_rank_list(actual_log_dir_path, src_rank, 0, filter_time)    
        for index, dest in enumerate(dest_rank_list_time):
            dest_rank=int(dest)
            adjacent_matrix_num_comm[src_rank][dest_rank]=adjacent_matrix_num_comm[src_rank][dest_rank]+1
            adjacent_matrix_num_particles[src_rank][dest_rank]=adjacent_matrix_num_particles[src_rank][dest_rank]+dest_rank_list_pnum[index]
    
    # particles in
    adjacent_matrix_num_particles_colum_sum=adjacent_matrix_num_particles.sum(axis=0)
    # particles out
    adjacent_matrix_num_particles_row_sum=adjacent_matrix_num_particles.sum(axis=1)

    return list(adjacent_matrix_num_particles_colum_sum),list(adjacent_matrix_num_particles_row_sum)



if __name__ == "__main__":
    if len(sys.argv)!=4:
        print("<binary> <estimation log> <num_rank> <num_stages>",flush=True)
        exit(0)
        
    estimation_log=sys.argv[1]
    num_rank=int(sys.argv[2])
    num_stages=int(sys.argv[3])
    
    if num_stages!=1 and num_stages!=3:
        print("only support num stages 1 or 3")
        exit(0)

    if num_stages==1:
        file_name = estimation_log
        fo=open(file_name, "r")
        for line in fo:
            line_strip=line.strip()
            if "NormBlockPopularity:" not in line_strip:
                continue
            adv_step_list_str=line_strip.split(":")[1]
            adv_step_list_str=adv_step_list_str.replace(' ','')
            adv_step_list=eval(adv_step_list_str)
            with open("adv_step_stages_list.json", "w") as f:
                f.write("[")
                for index,work in enumerate(adv_step_list): 
                    if index>0:
                        f.write(",")
                    f.write("["+str(work)+"]")
                f.write("]")
                
                    
            
    
    if num_stages==3:
        file_name = estimation_log
        fo=open(file_name, "r")
        for line in fo:
            line_strip=line.strip()
            if "MultiStagesBlockPopularity" not in line_strip:
                continue
            adv_step_stages_list= line_strip.split(":")[1]
        
        #find dedicated log
        adv_step_stages_list=adv_step_stages_list.replace('"','')
        print(adv_step_stages_list)

        # compute the popularity

        with open("adv_step_stages_list.json", "w") as f:
            f.write(adv_step_stages_list)


