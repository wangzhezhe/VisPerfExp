import numpy as np
from random import randint
from time import sleep
import time
import shutil
import os
import sys

import matplotlib.pyplot as plt

gblue = '#4486F4'
gred = '#DA483B'
gyellow = '#FFC718'
ggreen = '#1CA45C'

# if one block one rank, the block id is the rank id
def parse_log_get_acc_advect_steps(log_dir_path,num_rank):
    acc_adv_step_list=[]
    acc_adv_step_list_with_rankid=[]
    for rank in range(0,num_rank):
        total_adv_steps=0        
        file_name = log_dir_path+"/timetrace."+str(rank)+".out"
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
    if len(sys.argv)!=3:
        print("<binary> <dir for actual run> <num_rank>",flush=True)
        exit()
    actual_log_dir_path=sys.argv[1]
    num_rank=int(sys.argv[2])
    
    # go through the data dir to find the actual advection steps
    acc_adv_step_list, acc_adv_step_list_with_rankid = parse_log_get_acc_advect_steps(actual_log_dir_path,num_rank)
    sum_adv_steps = sum(acc_adv_step_list)
    # start from 0 to the largest one
    actual_acc_advect_steps_popularity = np.array(acc_adv_step_list)/sum_adv_steps
    print(acc_adv_step_list_with_rankid)
    
    print("actual_acc_advect_steps_popularity", end=":")
    print(list(actual_acc_advect_steps_popularity))
    # looking at the estimation results
    
    # get the actual in and out particles according to the raw log
    actual_in_particles, actual_out_particles = get_actual_in_out_number(actual_log_dir_path,num_rank)
    norm_actual_in_particles = (actual_in_particles/sum(actual_in_particles)).tolist()
    norm_actual_out_particles = (actual_out_particles/sum(actual_out_particles)).tolist()
    print("normalized actual_in_particles",norm_actual_in_particles)
    print("normalized actual_out_particles",norm_actual_out_particles)
