from os import system
import subprocess
import re
from os.path import exists
import sys


comm_count=0
comm_seeds_sum=0
max_num_comm=0
accumulated_comm_time=0
accumulated_advec_time=0

def parse_step(file_name, rank, step):
    global comm_count
    global comm_seeds_sum
    global max_num_comm
    global accumulated_comm_time
    global accumulated_advec_time

    local_recv_time=0
    local_advec_time=0
    local_comm_count = 0
    local_comm_time = 0
    local_init_time = 0
    local_advect_steps=0
    local_before_while_time=0
    local_update_result_time=0

    file_exists = exists(file_name)
    
    if file_exists==False:
        return
    # open file
    # print("check filename:",file_name,"rank:",rank,"step:",step)
    
    fo=open(file_name, "r")
    step_recv_identify_str="Received_"+str(step)+" "
    step_adev_identify_str="Advected_"+str(step)+" "

    init_str = "Init_"+str(step)+" "
    before_while_str = "BeforeAdve_"+str(step)+" "
    update_result_str = "UpdateResult_"+str(step)+" "
    

    advect_steps_str = "AdvectSteps_"+str(step)+" "
    comm_str = "Comm_"+str(step)+" "
    
    
   

    for line in fo:
        line_strip=line.strip()
        #print(line_strip)
        #split between _
        split_str= line_strip.split(" ")
        if step_recv_identify_str in line_strip:
            #print(line_strip)
            comm_count=comm_count+1
            comm_seeds_sum=comm_seeds_sum+int(split_str[1])
            local_comm_count=local_comm_count+1
            local_recv_time = local_recv_time + float(split_str[2])

        if step_adev_identify_str in line_strip:
            accumulated_advec_time = accumulated_advec_time+float(split_str[2])
            local_advec_time = local_advec_time +float(split_str[2])     

        if comm_str in line_strip:
            local_comm_time = local_comm_time +float(split_str[2])

        if init_str in line_strip:
            local_init_time = local_init_time+float(split_str[2])

        if before_while_str in line_strip:
            local_before_while_time = local_before_while_time+float(split_str[2])

        if update_result_str in line_strip:
            local_update_result_time = local_update_result_time+float(split_str[2])

        if advect_steps_str in line_strip:
            local_advect_steps = local_advect_steps +int(split_str[1])  

    fo.close()
    if local_comm_time>max_num_comm:
        max_num_comm=local_comm_time

    print("rank:", rank, "advec_time:", local_advec_time, "comm_time",local_comm_time, "local_recv_time:",local_recv_time, "local_comm_count",local_comm_count, "comm_seeds_sum", comm_seeds_sum, "local_advect_steps",local_advect_steps)
    print("rank:", rank, "local_init_time",local_init_time,"local_before_while_time",local_before_while_time,"local_update_result_time",local_update_result_time )

    #print("rank:", rank, "local_comm:",local_comm_time,"local_advec:", local_advec_time)
    


if __name__ == "__main__":
    
    if len(sys.argv)!=4:
        print("<binary> <procs> <step> <logDirPath, no />")
        exit()
    
    procs = int(sys.argv[1])
    step = int(sys.argv[2])
    dirPath = sys.argv[3]

    for i in range (0,procs,1):
        file_name = dirPath+"/counter."+str(i)+".out"
        parse_step(file_name,i,step)  
    
    print("total number of comm", comm_count)
    print("comm total seeds", comm_seeds_sum)
    print("max_num_comm", max_num_comm)
    #print("comm seeds each time in avg", comm_seeds_sum/comm_count)
    #print("accumulated_comm_time", accumulated_comm_time)
    #print("accumulated_advec_time", accumulated_advec_time)