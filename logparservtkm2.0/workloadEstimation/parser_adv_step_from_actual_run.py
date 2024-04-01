import numpy as np
from random import randint
from time import sleep
import time
import shutil
import os
import sys



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


if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("<binary> <logFileDirPath> <num_rank>",flush=True)
        exit()
    log_dir_path=sys.argv[1]
    num_rank=int(sys.argv[2])
    
    # go through the data dir to find the actual advection steps
    acc_adv_step_list, acc_adv_step_list_with_rankid = parse_log_get_acc_advect_steps(log_dir_path,num_rank)
    sum_adv_steps = sum(acc_adv_step_list)
    # start from 0 to the largest one
    print(acc_adv_step_list_with_rankid)
