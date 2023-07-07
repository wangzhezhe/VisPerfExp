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

# this script analyse the statistics 
# of all particle associated information

# 0707/astro.A.b64.n2.r64.B_p5000_s2000/ max_alive_id 47712

if __name__ == "__main__":
    
    if len(sys.argv)!=4:
        print("<binary> <procs> <dirpath> <id>")
        exit()

    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    simSycle=0
    dirPath=sys.argv[2]
    particleID=sys.argv[3]

    # extract largest total exeuction time
    filter_start="FilterStart_"+str(simSycle)+" "
    filter_end="FilterEnd_"+str(simSycle)+" "
    initTime=0
    max_filter_time=0
    
    for rank in range(0,procs,1):
        file_name = dirPath+"/timetrace."+str(rank)+".out"
        fo=open(file_name, "r")  
        filter_time=0
        filter_start_time=0
        filter_end_time=0
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(" ")
            if rank==0:
                if "GoStart_0" in line_strip:
                    initTime=float(split_str[1])
            if filter_start in line_strip:
                filter_start_time = float(split_str[1])       
            if filter_end in line_strip:
                filter_end_time = float(split_str[1])
            filter_time = filter_end_time-filter_start_time
            max_filter_time = max(max_filter_time,filter_time)
        fo.close()
    
    print("filter execution time is", max_filter_time)

    # find information for associated id
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        #print(file_name)

        fo=open(file_name, "r")

        cycle_identifier ="s"+str(simSycle)
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")
            #print(split_str)
            #SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks,AccBO,AccEO,AccAdv,AccWait
            if cycle_identifier in line_strip:
                if split_str[1]==particleID:
                    print(split_str) 
                    aliveTime = float(split_str[3])
                    print ("Init",initTime,float(initTime)/aliveTime)
                    print( "bo", split_str[6], float(split_str[6])/aliveTime 
                          ,"eo", split_str[7], float(split_str[7])/aliveTime, 
                           "a",split_str[8], float(split_str[8])/aliveTime, 
                           "wait", split_str[9], float(split_str[9])/aliveTime, 
                           "alive", split_str[3])
                    commTime=aliveTime-float(initTime)-float(split_str[6])-float(split_str[7])-float(split_str[8])-float(split_str[9])
                    print("comm", commTime, commTime/aliveTime)
   