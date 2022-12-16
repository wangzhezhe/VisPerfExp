from os import system
import subprocess
import re
from os.path import exists
import sys
import statistics

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


def partition(collection):
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset 
        yield [ [ first ] ] + smaller

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


def outputAssignment(index, assignPlan):

    f = open("./assignment/assign_options.config_"+str(index),'w')
    for option in assignPlan:
        option_str=""
        for index, blockid in enumerate(option):
            if index==0:
                option_str=str(blockid)
            else:
                option_str=option_str+" "+str(blockid)
        f.write(option_str+"\n")
    f.close()     


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
    
    # this number can show the level of communicated particles
    print("Total number of send particles", total_send_particles)
    print(dic_advected_particles)
    print(dic_send_particles)
    

    # go through all cases can find one there is balanced workload
    # get all combinations
    assign_option_workload_balanced=[]
    proclist = list(range(0,procs))
    min_workload_stdev=sys.maxsize
    index=0
    for n, p in enumerate(partition(proclist), 1):
        #print(n, sorted(p), len(p))
        # assume dedicated procs are intransit_proc_num
        sorted_p_list=sorted(p)
        if len(sorted_p_list)==intransit_proc_num:
            outputAssignment(index,sorted_p_list)
            index=index+1

            #workload_stdev = compute_workload_stdev(sorted_p_list,dic_advected_particles)
            #if workload_stdev<min_workload_stdev:
            #    min_workload_stdev=workload_stdev
            #    assign_option_workload_balanced=sorted_p_list

    # go through options, return the stdev
    #print("assign_option_workload_balanced", assign_option_workload_balanced)
    #print("min_workload_stdev",min_workload_stdev)

    # ouput the balanced options into a file
    #f = open("assign_options.config",'w')
    #for option in assign_option_workload_balanced:
    #    option_str=""
    #    for index, blockid in enumerate(option):
    #        if index==0:
    #            option_str=str(blockid)
    #        else:
    #            option_str=option_str+" "+str(blockid)
    #    f.write(option_str+"\n")
    #f.close()    
    
    # Build the graph of the particle send/recv path
    # TODO, find one there is balanced workload