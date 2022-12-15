from os import system
import subprocess
import re
from os.path import exists
import sys

# for each rank, for specific iteration(step)
# collect ParticlesAdvected_0(actual work), ParticlesSend_0(actual comm), ParticleActive_0(what does it represent?), 

# for whole ranks
# collect ParticlesSend_0

total_send_particles=0

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

    
    print("rank",rank, "ParticlesAdvected", sum(particle_advected_list))
    print("rank",rank, "ParticlesSend", local_send_particles)

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
