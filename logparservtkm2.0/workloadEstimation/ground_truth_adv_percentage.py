import numpy
from random import randint
from time import sleep
import time
import shutil
import os
import sys


def parse_log_get_adv_percentage(num_rank, dirPath):
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
    for rank in range(0,num_rank,1):
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
        acc_ratio_list.append(acc_work_time/filter_time)

    return acc_ratio_list, filter_time

def parse_log_get_acc_advect_steps(dataset_name, num_rank, dirPath):
    acc_adv_step_list=[]
    acc_adv_step_list_with_rankid=[]
    for rank in range(0,num_rank):
        total_adv_steps=0        
        file_name = dirPath+"/actual_"+dataset_name+"_"+str(num_rank)+"/timetrace."+str(rank)+".out"
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

def parse_log_estimator_popularity(dataset_name,num_rank, dirPath, num_test_points):
    file_name = dirPath+"/estimate_"+dataset_name+"_r"+str(num_rank)+ "_tp" + str(num_test_points) + ".log"
    fo=open(file_name, "r")
    estimator_value_list=[]
    for line in fo:
        line_strip=line.strip()
        #print(line_strip)
        if "NormBlockPopularity" in line_strip:
            start =line_strip.find("[")
            end=line_strip.find("]")
            extract_num = line_strip[start+1:end-1]
            split_line = extract_num.split(",")
            print(split_line)
            estimator_value_list = [float(v) for v in split_line]
    fo.close()
    estimator_value_list_with_rankid=[]
    i=0
    if len(estimator_value_list)==0:
        print("No NormBlockPopularity log")
        exit(0)
    for v in estimator_value_list:
        estimator_value_list_with_rankid.append([i,v])
        i+=1
    return estimator_value_list,estimator_value_list_with_rankid



if __name__ == "__main__":
    if len(sys.argv)!=5:
        print("<binary> <dataset name> <runDirPath> <num_rank> <num_test_points>",flush=True)
        exit()
    dataset_name=sys.argv[1]
    dirPath=sys.argv[2]
    num_rank=int(sys.argv[3])
    num_test_points=int(sys.argv[4])
    # acc_ratio_list, filter_time = parse_log_get_adv_percentage(num_rank, dirPath)
    # r=0
    # for v in acc_ratio_list: 
    #     print("rank",r,"ratio",v)
    #     r+=1

    acc_adv_step_list, acc_adv_step_list_with_rankid = parse_log_get_acc_advect_steps(dataset_name, num_rank, dirPath)
    #print("acc_adv_step_list",acc_adv_step_list)
    adv_all_steps = sum(acc_adv_step_list)
    acc_adv_step_list_norm = [float(i)/adv_all_steps for i in acc_adv_step_list]
    
    for v in acc_adv_step_list_with_rankid:
        v[1]=v[1]/adv_all_steps

    estimate_ratio,estimator_value_list_with_rankid=parse_log_estimator_popularity(dataset_name, num_rank, dirPath, num_test_points)


    r=0
    for v in acc_adv_step_list_norm: 
        print("rank",r,"ground_truth",format(v, '.6f'), "estimation", \
              format(estimate_ratio[r], '.6f'), "diff", \
              format(abs(estimate_ratio[r]-v), '.6f'), \
              "ratio", format(v/abs(estimate_ratio[r]), '.6f'))
        r+=1

    # sorting block id accoring to estimate_ratio
        
    print(acc_adv_step_list_with_rankid)
    print(estimator_value_list_with_rankid)


    sorted_acc_adv_step_list_with_rankid=sorted(acc_adv_step_list_with_rankid, key=lambda x: x[1], reverse=True)
    sorted_estimator_value_list_with_rankid=sorted(estimator_value_list_with_rankid, key=lambda x: x[1], reverse=True)

    print("sorted_acc_adv_step_list_with_rankid")
    print([v[0] for v in sorted_acc_adv_step_list_with_rankid])
    print([format(v[1], '.6f') for v in sorted_acc_adv_step_list_with_rankid])

    print("sorted_estimator_value_list_with_rankid")
    print([v[0] for v in sorted_estimator_value_list_with_rankid])
    print([format(v[1], '.6f') for v in sorted_estimator_value_list_with_rankid])

    sorted_diff=0
    i = 0 
    for v in sorted_acc_adv_step_list_with_rankid:
        if( v[0]!= sorted_estimator_value_list_with_rankid[i][0]):
            sorted_diff+=1
        i+=1
    print("sorted_diff",sorted_diff)
    
    
    # sorting block id accoring to acc_adv_step_list_norm