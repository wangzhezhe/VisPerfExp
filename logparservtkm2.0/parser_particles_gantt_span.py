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

# draw gantt chart from the perspective of tracing particles.
if __name__ == "__main__":
    
    if len(sys.argv)!=7:
        print("<binary> <procs> <step/cycle> <dirpath> <tracing_particle_id> <startTime> <endTime>")
        exit()

    procs=int(sys.argv[1])
    step=int(sys.argv[2])
    dirPath=sys.argv[3]
    tracing_particle_id=int(sys.argv[4])
    start_time = float(sys.argv[5])
    end_time = float(sys.argv[6])
    
    dirname = dirPath.split("/")[-2]

    # go through all files and sorting the particle according to advected steps
    particle_list=[]

    advect_whole=0
    advect_steps_whole=0
    comm_start_time=0
    comm_start_list=[]
    comm_end_time=0
    comm_time_list=[]
    actual_comm_list=[]
    recv_time_list=[]
    send_end_list=[]
    for proc in range(0,procs,1):
        file_name = dirPath+"/particle_tracing_details."+str(proc)+".out"
        fo=open(file_name, "r")
        
        advect_start_time=0
        advect_step_before=0

        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")
                   
            # for in-transit case, the rankid may not eauqls to proc number
            # Event,SimCycle,BlockID(RankId),ParticleID,CurrTime,AdvectedSteps
            if str(step)==split_str[1] :
                #print(split_str)
                if split_str[0]=="WORKLET_Start":
                    advect_start_time=float(split_str[4])
                    advect_step_before=float(split_str[5])
                if split_str[0]=="WORKLET_End":
                    advect_end_time=float(split_str[4])
                    advect_step_after=float(split_str[5])
                    blockid = int(split_str[2])
                    pnum = int(split_str[6])
                    # start time, end time, advec steps, blockid
                    advect_steps_whole=advect_steps_whole+advect_step_after-advect_step_before
                    particle_list.append([advect_start_time,advect_end_time,advect_step_after-advect_step_before,blockid,pnum])

                if split_str[0]=="GANG_COMM_START":
                    comm_start_time=float(split_str[4])
                    #print("comm_start_time",comm_start_time)
                    comm_start_list.append(comm_start_time)
                if split_str[0]=="GANG_COMM_END":
                    comm_end_time=float(split_str[4])
                    comm_time_list.append((comm_start_time,comm_end_time-comm_start_time))
                    actual_comm_list.append(comm_end_time-comm_start_time)
                    send_end_list.append(comm_end_time)
                if split_str[0]=="RECVOK":
                    recv_time_list.append(float(split_str[4]))


    #sorting all particle list
    particle_list_sorted=sorted(particle_list, key=lambda x: x[0])
    #print(particle_list_sorted)
    particle_live_time = particle_list_sorted[-1][1]
    print("particle_live_time", particle_live_time)


    #computing key information in specific range
    currEndTime=start_time
    
    for p in particle_list_sorted:
        if p[0]<currEndTime:
            continue
        print("wait ", p[0]-currEndTime) 
        print("advct ",p[1]-p[0])
        currEndTime=p[1]





