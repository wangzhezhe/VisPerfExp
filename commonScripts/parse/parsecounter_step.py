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

    local_comm_time=0
    local_advec_time=0

    local_comm = 0
    file_exists = exists(file_name)
    
    if file_exists==False:
        return
    # open file
    # print("check filename:",file_name,"rank:",rank,"step:",step)
    
    fo=open(file_name, "r")
    step_recv_identify_str="Received_"+str(step)+" "
    step_adev_identify_str="Advected_"+str(step)+" "

    for line in fo:
        line_strip=line.strip()
        #print(line_strip)
        #split between _
        if step_recv_identify_str in line_strip:
            #print(line_strip)
            split_str= line_strip.split(" ")
            comm_count=comm_count+1
            comm_seeds_sum=comm_seeds_sum+int(split_str[1])
            local_comm=local_comm+1
            accumulated_comm_time = accumulated_comm_time+float(split_str[2])
            local_comm_time = local_comm_time + float(split_str[2])
        if step_adev_identify_str in line_strip:
            split_str= line_strip.split(" ")
            accumulated_advec_time = accumulated_advec_time+float(split_str[2])
            local_advec_time = local_advec_time +float(split_str[2])
    
    fo.close()
    if local_comm>max_num_comm:
        max_num_comm=local_comm

    print("rank:", rank, "local_comm:",local_comm_time,"local_advec:", local_advec_time)
    


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
    
    print("number of comm", comm_count)
    print("comm total seeds", comm_seeds_sum)
    print("max_num_comm", max_num_comm)
    #print("comm seeds each time in avg", comm_seeds_sum/comm_count)
    print("accumulated_comm_time", accumulated_comm_time)
    print("accumulated_advec_time", accumulated_advec_time)