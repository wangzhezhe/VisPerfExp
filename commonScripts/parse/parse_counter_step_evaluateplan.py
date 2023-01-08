from os import system
import subprocess
import re
from os.path import exists
import sys
import statistics
import os
import shutil

# for the givin assignment plan (or the dir)
# evaluate its key properties based on the counter log

# for each rank, for specific iteration(step)
# collect ParticlesAdvected_0(actual work), ParticlesSend_0(actual comm), ParticleActive_0(what does it represent?), 

# for whole ranks
# collect ParticlesSend_0

total_send_particles=0

dic_advected_particles={}
dic_send_particles={}

intransit_proc_num=4

def parse_step(file_name, rank, step):
    global total_send_particles

    # local time represents the time info for each rank

    local_active_particles=0
    local_advected_particles=0
    local_send_particles=0
    
    file_exists = exists(file_name)
    
    if file_exists==False:
        return
    # open file
    # print("check filename:",file_name,"rank:",rank,"step:",step)
    
    fo=open(file_name, "r")
    particle_advected_str="ParticlesAdvected_"+str(step)+" "
    particle_advected_list=[]

    particle_todest_str="ToDest_"+str(step)+" "

    for line in fo:
        line_strip=line.strip()
        #print(line_strip)
        #split between _
        split_str= line_strip.split(" ")
        if particle_advected_str in line_strip:
            temp_advected_particles=int(split_str[1])
            particle_advected_list.append(temp_advected_particles)

        if particle_todest_str in line_strip:
            # the first one is the dest id, the second one is the # particles to dest
            local_send_particles=local_send_particles+int(split_str[2])
            total_send_particles=total_send_particles+int(split_str[2])

    sum_particle_advected=sum(particle_advected_list)
    print("rank",rank, "ParticlesAdvected", sum_particle_advected)
    #print("rank",rank, "ParticlesSend", local_send_particles)
    dic_advected_particles[rank]=sum_particle_advected
    dic_send_particles[rank]=local_send_particles

def compute_largest_workload(assignment_option, dic_advected_particles):
    if len(assignment_option)!=intransit_proc_num:
        print("assignment_option len should be "+str(intransit_proc_num))
        exit(-1)
    
    # for each group
    max_particle_number=0
    for group in assignment_option:
        curr_particles=0
        
        # go through blocks in each groups
        for blockid in group:
            curr_particles=curr_particles+dic_advected_particles[blockid]
        
        # for each group, update the largetst one
        max_particle_number=max(max_particle_number,curr_particles)

    return max_particle_number

def compute_workload_stdev(assignment_option, dic_advected_particles):
    
    if len(assignment_option)!=intransit_proc_num:
        print("assignment_option len should be "+str(intransit_proc_num))
        exit(-1)
    group_workload=[]
    for option in assignment_option:
        temp_particles=0
        for blockid in option:
            temp_particles=temp_particles+dic_advected_particles[blockid]
        group_workload.append(temp_particles)
    
    #print(group_workload)
    return statistics.stdev(group_workload)

if __name__ == "__main__":

    if len(sys.argv)!=5:
        print("<binary> <procs> <step> <logDirPath, no /> <assignmentDir>")
        exit()
    
    procs = int(sys.argv[1])
    step = int(sys.argv[2])
    logDirPath = sys.argv[3]
    assignment_dir = sys.argv[4]

    for i in range (0,procs,1):
        log_file_name = logDirPath+"/counter."+str(i)+".out"
        parse_step(log_file_name,i,step)  
    
    # this number can show the level of communicated particles
    print("Total number of send particles", total_send_particles)
    print(dic_advected_particles)
    print(dic_send_particles)
    
    # the above code extracts key information from log file
    # the subsequent code evaluate provided plans in the provided folder

    # go through all cases can find one there is balanced workload
    # get all combinations
    options_workload_balanced=[]
    min_workload_stdev=sys.maxsize
    min_workload_largest=sys.maxsize
    index=0
    workload_balanced_index_tuple=[]
    workload_largest_index_tuple=[]

    for filename in os.listdir(assignment_dir):
        plan_file_path=assignment_dir+"/"+filename
        # load the assignment plan from file path
        curr_assignment_plan = []

        plan_index = filename.split("_")[2]

        #print(plan_file_path, plan_index)

        fo=open(plan_file_path, "r")
        for line in fo:
            # go through each line
            line_strip=line.strip()
            curr_assignment_plan.append(list(map(int, line_strip.split())))
        fo.close()

        # compute workload_stdev, maybe adding more evaluated metrics here
        workload_stdev = compute_workload_stdev(curr_assignment_plan,dic_advected_particles)
        
        temp_tuple_stdev=(plan_index,workload_stdev)
        workload_balanced_index_tuple.append(temp_tuple_stdev)

        if workload_stdev<min_workload_stdev:
            min_workload_stdev=workload_stdev
            assign_option_workload_balanced=curr_assignment_plan   

        # compute the largest workload
        workload_largest = compute_largest_workload(curr_assignment_plan,dic_advected_particles)
        # find the minimal of max workload
        if workload_largest<min_workload_largest:
            min_workload_largest=workload_largest
            assign_option_workload_largest=curr_assignment_plan
        
        temp_tuple_largest_workload=(plan_index,workload_largest)
        workload_largest_index_tuple.append(temp_tuple_largest_workload)          

    
    print("assign_option_workload_balanced", assign_option_workload_balanced)
    print("min_workload_stdev",min_workload_stdev)

    print("assign_option_workload_largest", assign_option_workload_largest)
    print("min_workload_largest",min_workload_largest)

    # ouput the balanced options into a file
    f = open("assign_options_optimal_workload_stdev.config",'w')
    for option in assign_option_workload_balanced:
        option_str=""
        for index, blockid in enumerate(option):
            if index==0:
                option_str=str(blockid)
            else:
                option_str=option_str+" "+str(blockid)
        f.write(option_str+"\n")
    f.close()    
    
    # sort the tuple list
    # which have k best solutions for workload stdev
    dir_name_workload_stdev_kmin="./assignment_stdev_kmin"
    dir_name_all=assignment_dir

    workload_balanced_index_tuple.sort(key = lambda x: x[1])

    # output the minimal kth
    # create dir if it is not exist
    if not os.path.isdir(dir_name_workload_stdev_kmin):
        os.mkdir(dir_name_workload_stdev_kmin)

    for i in range (0,20,1):
        print(workload_balanced_index_tuple[i])
        plan_index=workload_balanced_index_tuple[i][0]
        # put these restuls into a separate dir
        src=dir_name_all+"/assign_options.config_"+str(plan_index)
        dst=dir_name_workload_stdev_kmin+"/assign_options.config_"+str(plan_index)
        shutil.copyfile(src, dst)

    # sort tuple list, output the result with the largest workload
    dir_name_workload_largest_kmin="./assignment_largest_kmin"
    dir_name_all=assignment_dir

    workload_largest_index_tuple.sort(key = lambda x: x[1])

    # output the minimal kth
    # create dir if it is not exist
    if not os.path.isdir(dir_name_workload_largest_kmin):
        os.mkdir(dir_name_workload_largest_kmin)
    
    print("---workload largest results---")

    for i in range (0,100,1):
        print(workload_largest_index_tuple[i])
        plan_index=workload_largest_index_tuple[i][0]
        # put these restuls into a separate dir
        src=dir_name_all+"/assign_options.config_"+str(plan_index)
        dst=dir_name_workload_largest_kmin+"/assign_options.config_"+str(plan_index)
        shutil.copyfile(src, dst)
    