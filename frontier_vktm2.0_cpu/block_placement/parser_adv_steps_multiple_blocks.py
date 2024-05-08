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

# one rank may contains multiple blocks
def parse_log_get_acc_advect_steps(log_dir_path,num_rank):
    acc_adv_step_list=[]
    acc_adv_step_list_with_blockid=[]

    for rank in range(0,num_rank):
        total_adv_steps=0        
        file_name = log_dir_path+"/timetrace."+str(rank)+".out"
        # for each rank, use map store the blockid:acc_adv_steps
        adv_step_dict = dict()
        fo=open(file_name, "r")
        for line in fo:
            line_strip=line.strip()
            if "ParticleAdvectInfo" not in line_strip:
                continue

            par_adv_str_list = line_strip.split(" ")[0].split("_")
            
            if len(par_adv_str_list)!=7:
                print("Checking log format, the blockid should be printed out")
                fo.close()
                exit(0)

            blockid= int(par_adv_str_list[5])
            adv_steps= int(par_adv_str_list[2])
            if blockid in adv_step_dict.keys():
                adv_step_dict[blockid]+=adv_steps
            else:
                # the first time we get this blockid
                adv_step_dict[blockid]=adv_steps
        fo.close()

        # go through dict
        # key is block id, value is associated adv steps for this block
        for key, value in adv_step_dict.items():
            acc_adv_step_list.append(value)
            acc_adv_step_list_with_blockid.append([key,value])
        
    return acc_adv_step_list,acc_adv_step_list_with_blockid


if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("<binary> <dir for run> <num_rank>",flush=True)
        exit()
    actual_log_dir_path=sys.argv[1]
    num_rank=int(sys.argv[2])
    
    # go through the data dir to find the actual advection steps
    acc_adv_step_list, acc_adv_step_list_with_blockid = parse_log_get_acc_advect_steps(actual_log_dir_path,num_rank)
    sum_adv_steps = sum(acc_adv_step_list)

    # sort the values in the blockid from small value to large value
    acc_adv_step_list_with_blockid_sorted=sorted(acc_adv_step_list_with_blockid, key=lambda x: x[0], reverse=False)
    print("acc_adv_step_list_with_blockid_sorted",acc_adv_step_list_with_blockid_sorted)

    acc_adv_step_list_sorted=[]
    acc_adv_step_list_sorted_nodup=[]
    temp_step=0
    nodup_index=-1
    for index,adv_info in enumerate(acc_adv_step_list_with_blockid_sorted):
        # merge the block with the same id
        if index>0 and acc_adv_step_list_with_blockid_sorted[index][0]==acc_adv_step_list_with_blockid_sorted[index-1][0]:
            # merge this into previous one
            # when index>0 the nodup_index is >=0
            acc_adv_step_list_sorted_nodup[nodup_index][1]=acc_adv_step_list_sorted_nodup[nodup_index][1]+adv_info[1]
        else:
            acc_adv_step_list_sorted_nodup.append(adv_info)
            nodup_index+=1


    #acc_adv_step_list_sorted.append(adv_info[1]/sum_adv_steps)
    acc_adv_step_list_sorted_nodup_popularity=[]
    for i in range(len(acc_adv_step_list_sorted_nodup)):
        acc_adv_step_list_sorted_nodup_popularity.append(float(acc_adv_step_list_sorted_nodup[i][1])/sum_adv_steps)

    print("acc_adv_step_list_sorted_nodup_popularity", end=":")
    print(list(acc_adv_step_list_sorted_nodup_popularity))
    
    # print("acc_adv_step_list_sorted", end=":")
    # print(list(acc_adv_step_list_sorted))

