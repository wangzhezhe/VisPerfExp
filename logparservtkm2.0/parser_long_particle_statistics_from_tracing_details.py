from os import system
from os.path import exists
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import ticker
import statistics
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# go through particle file which records all necessary information when a particle terminates
# finding one that satisfies specific constraints
# max execution time
# or ids statyin in specific executionime-#traversing block region
if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("<binary> <procs> <dirpath>")
        exit()

    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    simSycle=0
    dirPath=sys.argv[2]

    dirname = dirPath.split("/")[-2]
    print("dirname:",dirname)

    particle_comm_stard_recvok_list=[]

    particle_send_acc=0
    particle_worklet_acc=0
    end_overhead_acc=0
    begin_overhead_acc=0
    go_start_time=0

    for rank in range(0,procs,1):
        
        particle_send_begin=0
        particle_worklet_begin=0
        end_overhead_begin=0
        begin_overhead_begin=0
        recv_ok_time=0

        particle_send_end=0
        particle_worklet_end=0
        end_overhead_end=0
        begin_overhead_end=0

        file_name = dirPath+"/particle_tracing_details."+str(rank)+".out"
        #print(file_name)
        fo=open(file_name, "r")

        particle_send_out_time=0
        
        #SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")

            if split_str[0]=="RECVOK":   
                recv_ok_time=float(split_str[4])
                begin_overhead_begin=recv_ok_time

            if split_str[0]=="WORKLET_Start":   
                particle_worklet_begin=float(split_str[4])
                begin_overhead_end=particle_worklet_begin
                if begin_overhead_end<begin_overhead_begin:
                    print("wrong log parser",file_name,begin_overhead_begin, begin_overhead_end)
                begin_overhead_acc=begin_overhead_acc+(begin_overhead_end-begin_overhead_begin)


            if split_str[0]=="WORKLET_End":
                particle_worklet_end=float(split_str[4])
                particle_worklet_acc=particle_worklet_acc+(particle_worklet_end-particle_worklet_begin)
                end_overhead_begin=particle_worklet_end

            if split_str[0]=="GANG_COMM_START":
                end_overhead_end=float(split_str[4])
                end_overhead_acc=end_overhead_acc+(end_overhead_end-end_overhead_begin)
            

            if split_str[0]=="GANG_COMM_END":
                comm_end=float(split_str[4])
                # store two key point: adv and comm start
                particle_comm_stard_recvok_list.append([recv_ok_time,end_overhead_end,comm_end,rank])

            if split_str[0]=="ParticleSendBegin":
                particle_send_begin=float(split_str[4])

            if split_str[0]=="ParticleSendEnd":
                particle_send_end=float(split_str[4])
                particle_send_acc=particle_send_acc+(particle_send_end-particle_send_begin)
                #print(particle_send_end,particle_send_begin)
    
    particle_comm_wait_acc=0
    # checking the comm and wait time
    all_particles_sorted=sorted(particle_comm_stard_recvok_list, key=lambda x: x[0])
    for index, p in enumerate(all_particles_sorted):
        if index>0:
            particle_comm_wait_acc=particle_comm_wait_acc+(all_particles_sorted[index][0]-all_particles_sorted[index-1][1])
    
    # adding the last one, only have comm time, not wait time
    particle_comm_wait_acc=particle_comm_wait_acc+(all_particles_sorted[-1][2]-all_particles_sorted[-1][1])
    
    # use last comm end time as the filter exec time
    filter_time = all_particles_sorted[-1][2]
    print("filter_time", (filter_time/1000000))

    print("all_particles_sorted[0]",all_particles_sorted[0])

    print("all_particles_sorted[-1]",all_particles_sorted[-1])
    
    percent_bo_acc=begin_overhead_acc/filter_time
    print("particle_begin_overhead_acc",begin_overhead_acc,"{:.0%}".format(percent_bo_acc))  
    percent_eo_acc=end_overhead_acc/filter_time
    print("particle_end_overhead_acc",end_overhead_acc,"{:.0%}".format(percent_eo_acc)) 
    percent_work_acc=particle_worklet_acc/filter_time
    print("particle_worklet_acc",particle_worklet_acc, "{:.0%}".format(percent_work_acc))    
    
    percent_comm_wait_acc=particle_comm_wait_acc/filter_time
    print("particle_comm_wait_acc",particle_comm_wait_acc,"{:.0%}".format(percent_comm_wait_acc)) 

    percent_send_acc=particle_send_acc/particle_comm_wait_acc
    print("percent of particle_send_acc in particle_comm_wait_acc",particle_send_acc,"{:.0%}".format(percent_send_acc)) 

    print("unmersured percent", 1.0-(percent_bo_acc+percent_eo_acc+percent_work_acc+percent_comm_wait_acc))