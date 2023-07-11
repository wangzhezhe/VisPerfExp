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

    # extract largest total exeuction time
    filter_start="FilterStart_"+str(simSycle)+" "
    filter_end="FilterEnd_"+str(simSycle)+" "
    
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
            if filter_start in line_strip:
                filter_start_time = float(split_str[1])       
            if filter_end in line_strip:
                filter_end_time = float(split_str[1])
            filter_time = filter_end_time-filter_start_time
            max_filter_time = max(max_filter_time,filter_time)
        fo.close()
    
    print("filter execution time is", max_filter_time)
    
    max_num_traversed_blocks=0
    max_num_traversed_blocks_id=0
    max_num_traversed_ratio=0

    max_alive=0
    max_alive_id=0

    traversed_blocks_range=[145,180]
    execution_ratio_range=[0.8,1.0]
    
    searched_particle_list=[]
    
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        #print(file_name)

        fo=open(file_name, "r")

        cycle_identifier ="s"+str(simSycle)
        
        #SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks
        for line in fo:
            line_strip=line.strip()
            if cycle_identifier in line_strip:
                split_str= line_strip.split(",")
                ratio = float(split_str[3])/max_filter_time
                terminat_reason = split_str[2]
                num_traversed_blocks = int(split_str[5])
                
                if ratio>max_alive:
                    max_alive=ratio
                    max_alive_id=split_str[1]
                    max_alive_id_termreason=terminat_reason
                    max_alive_id_traversed_blocks=num_traversed_blocks

                #if max_num_traversed_blocks<int(split_str[5]):
                #    max_num_traversed_blocks = max(max_num_traversed_blocks,num_traversed_blocks)
                #    max_num_traversed_blocks_id=split_str[1]
                #    max_num_traversed_ratio=ratio

                #if terminat_reason=='w' or terminat_reason=='b': 
                #    if (ratio>=execution_ratio_range[0] and ratio<=execution_ratio_range[1] and 
                #        num_traversed_blocks>=traversed_blocks_range[0] and num_traversed_blocks<=traversed_blocks_range[1]):
                #        searched_particle_list.append(split_str[1])

    print("traversed_blocks_range",traversed_blocks_range)
    print("execution_ratio_range",execution_ratio_range)
    #print("searched_particle_list",searched_particle_list)                    

    print("max_num_traversed_blocks_id",max_num_traversed_blocks_id, "max_num_traversed_blocks",max_num_traversed_blocks,"max_num_traversed_ratio",max_num_traversed_ratio, "max alive ratio", max_alive)
    print("max_alive_id",max_alive_id,"max_alive_id_traversed_blocks",max_alive_id_traversed_blocks)