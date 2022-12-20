from os import system
from os.path import exists
import sys
import statistics
import os

def check_comm(file_path):
    # create the group list
    block_group_list=[]
    blockid_to_groupid={}
    print("check",file_path)
    fo=open(file_path, "r")
    groupid=0
    for line in fo:
        # go through each line
        line_strip=line.strip()
        block_list=line_strip.split(" ")
        block_group_list.append(block_list)

        # insert blockid into map
        for blockid in block_list:
            blockid_to_groupid[blockid]=groupid

        groupid=groupid+1

    fo.close()

    print("block_group_list",block_group_list)
    print("blockid_to_groupid",blockid_to_groupid)
    
    total_transfered_particles=0
    # go through the log file and check the keyword
    for src_rank in range (0,procs,1):
        local_transfered_particles=0
        counter_log_file_name=logdir_path+"/counter."+str(src_rank)+".out"
        # open file and read the data line by line
        fo=open(counter_log_file_name, "r")
        for line in fo:
            line_strip=line.strip()
            key_str="ToDest_"+str(step)
            if key_str in line_strip:
                split_str= line_strip.split(" ")
                # get the dst id and the #particles sent to dst
                dst_rank=split_str[1]
                sent_number_particles=int(split_str[2])
                #print(dest_id,sent_particles)
                #decide if src_id and dest_id is in same group
                #the value in block list is str
                src_group_id=blockid_to_groupid[str(src_rank)]
                dst_group_id=blockid_to_groupid[dst_rank]
                if src_group_id==dst_group_id:
                    #same group
                    continue
                else:
                    local_transfered_particles=local_transfered_particles+sent_number_particles
        fo.close() 
        total_transfered_particles=total_transfered_particles+local_transfered_particles
        #print("rank", src_rank, "local_transfered_particles",local_transfered_particles)

    print("total_transfered_particles",total_transfered_particles)

# based on the generated assign plan
# output its comm number of particles
# TODO, assign plan can be a dir
if __name__ == "__main__":
    
    if len(sys.argv)!=5:
        print("<binary> <procs> <step> <logDirPath, no /> <dir of assign_plans>")
        exit()
    
    procs = int(sys.argv[1])
    step = int(sys.argv[2])
    logdir_path = sys.argv[3]
    assign_plans_dir = sys.argv[4]

    for filename in os.listdir(assign_plans_dir):
        file_path=assign_plans_dir+"/"+filename
        check_comm(file_path)
