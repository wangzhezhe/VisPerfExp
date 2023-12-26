from os import system
from os.path import exists
import sys
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import ticker
import statistics
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

labelSize = 16
tickSize = 16
legendsize=21
simSycle=0

figsize_x = 5.5
figsize_y = 3

sample_rate=1000

# asix, number of procs, dirpath and dataname
def draw_alive_time(ax,procs,dirPath,data_name, figid):
    all_particles=[]
    i=0
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        fo=open(file_name, "r")
        cycle_identifier ="s"+str(simSycle)
        
        for line in fo:
            line_strip=line.strip()

            #not the valide particle log
            if cycle_identifier not in line_strip:
                continue
            
            i=i+1
            split_str= line_strip.split(",")
            
            if(i%sample_rate!=0):
                continue
            #print(split_str)
            
            # id, lifetime/total execution time, traversed number of blocks, die reason
            # SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks,AccBO,AccEO,AccAdv,AccAllAdv,AccWait,AccWB,NumSteps,NumSmallSteps,AccGangSize,AccPrevGangSize
            alivetime = float(split_str[3])
            acc_group_size = float(split_str[14])
            traveled_blocks = float(split_str[5])
            particle=[acc_group_size,alivetime]
            all_particles.append(particle)
        fo.close()

    print("collected particle number:", len(all_particles))
    
    # sort particles from small to large
    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    time_list=[]
    for p in all_particles_sorted:
        time_list.append(p[1])
    

    ax.set_ylim([0,0.25*1e9])
    xpos = range(0, len(time_list),1)
    print(len(xpos),len(time_list))

    ax.bar(xpos,time_list)
    #ax.set_xticks([0,len(xpos)/2,len(xpos)])
    #ax.set_xticklabels(['0','320000','640000'])
    ax.set_xticks([])

    if data_name=="Tokamak":
        ax.set_ylabel(r'$Σ T_P$ (us)', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])
    
    ax.title.set_text(figid+data_name)
    ax.title.set_fontsize(labelSize)

def draw_acc_group_size(ax,procs,dirPath,data_name,figid):
    
    all_particles=[]
    i=0
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        fo=open(file_name, "r")
        cycle_identifier ="s"+str(simSycle)
        
        for line in fo:
            line_strip=line.strip()

            #not the valide particle log
            if cycle_identifier not in line_strip:
                continue
            
            i=i+1
            split_str= line_strip.split(",")
            
            if(i%sample_rate!=0):
                continue
            #print(split_str)
            
            # id, lifetime/total execution time, traversed number of blocks, die reason
            # SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks,AccBO,AccEO,AccAdv,AccAllAdv,AccWait,AccWB,NumSteps,NumSmallSteps,AccGangSize,AccPrevGangSize
            alivetime = float(split_str[3])
            acc_group_size = float(split_str[14])
            traveled_blocks = float(split_str[5])
            particle=[acc_group_size,acc_group_size]
            all_particles.append(particle)
        fo.close()

    print("collected particle number:", len(all_particles))
    
    # sort particles from small to large
    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    time_list=[]
    for p in all_particles_sorted:
        time_list.append(p[1])
    

    #ax.set_ylim([0,np.log(3.5*1e6)])
    ax.set_ylim([0,9*1e6])
    
    xpos = range(0, len(time_list),1)
    print(len(xpos),len(time_list))

    #ax.bar(xpos,list(np.log(time_list)))
    ax.bar(xpos,time_list)
    
    #ax.set_xticks([0,len(xpos)/2,len(xpos)])
    #ax.set_xticklabels(['0','320000','640000'])
    ax.set_xticks([])
    if data_name=="Tokamak":
        ax.set_ylabel('Acc group sizes', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])
    ax.title.set_text(figid)
    ax.title.set_fontsize(labelSize)

def draw_acc_and_prv_group_size(ax,procs,dirPath,data_name,figid):
    
    all_particles=[]
    i=0
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        fo=open(file_name, "r")
        cycle_identifier ="s"+str(simSycle)
        
        for line in fo:
            line_strip=line.strip()

            #not the valide particle log
            if cycle_identifier not in line_strip:
                continue
            
            i=i+1
            split_str= line_strip.split(",")
            
            if(i%sample_rate!=0):
                continue
            #print(split_str)
            
            # id, lifetime/total execution time, traversed number of blocks, die reason
            # SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks,AccBO,AccEO,AccAdv,AccAllAdv,AccWait,AccWB,NumSteps,NumSmallSteps,AccGangSize,AccPrevGangSize
            alivetime = float(split_str[3])
            acc_group_size = float(split_str[14])
            acc_prev_group_size = float(split_str[15])

            traveled_blocks = float(split_str[5])
            particle=[alivetime,0.2*acc_group_size+0.8*acc_prev_group_size]
            all_particles.append(particle)
        fo.close()

    print("collected particle number:", len(all_particles))
    
    # sort particles from small to large
    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    time_list=[]
    for p in all_particles_sorted:
        time_list.append(p[1])
    

    #ax.set_ylim([0,np.log(3.5*1e6)])
    ax.set_ylim([0,4.8*1e6])
    
    xpos = range(0, len(time_list),1)
    print(len(xpos),len(time_list))

    #ax.bar(xpos,list(np.log(time_list)))
    ax.bar(xpos,time_list)
    
    #ax.set_xticks([0,len(xpos)/2,len(xpos)])
    #ax.set_xticklabels(['0','320000','640000'])
    ax.set_xticks([])
    if data_name=="Tokamak":
        ax.set_ylabel('Total group size', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])
    ax.title.set_text(figid)
    ax.title.set_fontsize(labelSize)

def draw_acc_prev_group_size(ax,procs,dirPath,data_name,figid):
    
    all_particles=[]
    i=0
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        fo=open(file_name, "r")
        cycle_identifier ="s"+str(simSycle)
        
        for line in fo:
            line_strip=line.strip()

            #not the valide particle log
            if cycle_identifier not in line_strip:
                continue
            
            i=i+1
            split_str= line_strip.split(",")
            
            if(i%sample_rate!=0):
                continue
            #print(split_str)
            
            # id, lifetime/total execution time, traversed number of blocks, die reason
            # SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks,AccBO,AccEO,AccAdv,AccAllAdv,AccWait,AccWB,NumSteps,NumSmallSteps,AccGangSize,AccPrevGangSize
            alivetime = float(split_str[3])
            acc_group_size = float(split_str[14])
            acc_prev_group_size = float(split_str[15])
            traveled_blocks = float(split_str[5])
            particle=[acc_group_size,acc_prev_group_size]
            all_particles.append(particle)
        fo.close()

    print("collected particle number:", len(all_particles))
    
    # sort particles from small to large
    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    time_list=[]
    for p in all_particles_sorted:
        time_list.append(p[1])
    

    ax.set_ylim([0,3.5*1e6])
    #ax.set_ylim([0,2.8*1e6])
    
    xpos = range(0, len(time_list),1)
    print(len(xpos),len(time_list))

    #ax.bar(xpos,list(np.log(time_list)))
    ax.bar(xpos,time_list)
    
    #ax.set_xticks([0,len(xpos)/2,len(xpos)])
    #ax.set_xticklabels(['0','320000','640000'])
    ax.set_xticks([])
    if data_name=="Tokamak":
        ax.set_ylabel('Prev group size', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])
    ax.title.set_text(figid)
    ax.title.set_fontsize(labelSize)

def draw_comm_times(ax,procs,dirPath,data_name,figid):
    
    all_particles=[]
    i=0
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        fo=open(file_name, "r")
        cycle_identifier ="s"+str(simSycle)
        
        for line in fo:
            line_strip=line.strip()

            #not the valide particle log
            if cycle_identifier not in line_strip:
                continue
            
            i=i+1
            split_str= line_strip.split(",")
            
            if(i%sample_rate!=0):
                continue
            #print(split_str)
            
            # id, lifetime/total execution time, traversed number of blocks, die reason
            # SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks,AccBO,AccEO,AccAdv,AccAllAdv,AccWait,AccWB,NumSteps,NumSmallSteps,AccGangSize,AccPrevGangSize
            alivetime = float(split_str[3])
            acc_group_size = float(split_str[14])
            traveled_blocks = float(split_str[5])
            particle=[acc_group_size,traveled_blocks]
            all_particles.append(particle)
        fo.close()

    print("collected particle number:", len(all_particles))
    
    # sort particles from small to large
    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    time_list=[]
    for p in all_particles_sorted:
        time_list.append(p[1])
    

    ax.set_ylim([0,400])
    xpos = range(0, len(time_list),1)
    print(len(xpos),len(time_list))

    ax.bar(xpos,time_list)
    #ax.set_xticks([0,len(xpos)/2,len(xpos)])
    #ax.set_xticklabels(['0','320000','640000'])
    ax.set_xticks([])
    if data_name=="Tokamak":
        ax.set_ylabel('# visited blocks', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])
    ax.title.set_text(figid)
    ax.title.set_fontsize(labelSize)

def draw_acc_wait(ax,procs,dirPath,data_name,figid):
    
    all_particles=[]
    i=0
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        fo=open(file_name, "r")
        cycle_identifier ="s"+str(simSycle)
        
        for line in fo:
            line_strip=line.strip()

            #not the valide particle log
            if cycle_identifier not in line_strip:
                continue
            
            i=i+1
            split_str= line_strip.split(",")
            
            if(i%sample_rate!=0):
                continue
            #print(split_str)
            
            # id, lifetime/total execution time, traversed number of blocks, die reason
            # SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks,AccBO,AccEO,AccAdv,AccAllAdv,AccWait,AccWB,NumSteps,NumSmallSteps,AccGangSize,AccPrevGangSize
            alivetime = float(split_str[3])
            acc_group_size = float(split_str[14])
            traveled_blocks = float(split_str[5])
            acc_wait=float(split_str[10])
            particle=[acc_group_size,acc_wait]
            all_particles.append(particle)
        fo.close()

    print("collected particle number:", len(all_particles))
    
    # sort particles from small to large
    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    time_list=[]
    for p in all_particles_sorted:
        time_list.append(p[1])
    
    ax.set_ylim([0,0.1*1e9])
    xpos = range(0, len(time_list),1)
    print(len(xpos),len(time_list))

    ax.bar(xpos,time_list)
    ax.set_xticks([])
    #ax.set_xticks([0,len(xpos)/2,len(xpos)])
    #ax.set_xticklabels(['0','320000','640000'])
    if data_name=="Tokamak":
        ax.set_ylabel(r'$Σ T_{CW}$ (us)', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])
    ax.title.set_text(figid)
    ax.title.set_fontsize(labelSize)

def draw_acc_adv(ax,procs,dirPath,data_name,figid):
    
    all_particles=[]
    i=0
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        fo=open(file_name, "r")
        cycle_identifier ="s"+str(simSycle)
        
        for line in fo:
            line_strip=line.strip()

            #not the valide particle log
            if cycle_identifier not in line_strip:
                continue
            
            i=i+1
            split_str= line_strip.split(",")
            
            if(i%sample_rate!=0):
                continue
            #print(split_str)
            
            # id, lifetime/total execution time, traversed number of blocks, die reason
            # SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks,AccBO,AccEO,AccAdv,AccAllAdv,AccWait,AccWB,NumSteps,NumSmallSteps,AccGangSize,AccPrevGangSize
            alivetime = float(split_str[3])
            acc_group_size = float(split_str[14])
            traveled_blocks = float(split_str[5])
            acc_adv=float(split_str[8])
            particle=[acc_group_size,acc_adv]
            all_particles.append(particle)
        fo.close()

    print("collected particle number:", len(all_particles))
    
    # sort particles from small to large
    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    time_list=[]
    for p in all_particles_sorted:
        time_list.append(p[1])
    
    ax.set_ylim([0,2*1e8])
    xpos = range(0, len(time_list),1)
    print(len(xpos),len(time_list))

    ax.bar(xpos,time_list)
    #ax.set_xticks([0,len(xpos)/2,len(xpos)])
    #ax.set_xticklabels(['0','320000','640000'])
    ax.set_xticks([])
    if data_name=="Tokamak":
        ax.set_ylabel(r'Σ $T_A$ (us)', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])
    ax.title.set_text(figid)
    ax.title.set_fontsize(labelSize)


def draw_acc_bo_eo(ax,procs,dirPath,data_name,figid):
    
    all_particles=[]
    i=0
    for rank in range(0,procs,1):
        file_name = dirPath+"/particle."+str(rank)+".out"
        fo=open(file_name, "r")
        cycle_identifier ="s"+str(simSycle)
        
        for line in fo:
            line_strip=line.strip()

            #not the valide particle log
            if cycle_identifier not in line_strip:
                continue
            
            i=i+1
            split_str= line_strip.split(",")
            
            if(i%sample_rate!=0):
                continue
            #print(split_str)
            
            # id, lifetime/total execution time, traversed number of blocks, die reason
            # SimCycle,ParticleID,RemovedReason,ActiveTime,NumComm,TraversedNumofBlocks,AccBO,AccEO,AccAdv,AccAllAdv,AccWait,AccWB,NumSteps,NumSmallSteps,AccGangSize,AccPrevGangSize
            alivetime = float(split_str[3])
            acc_group_size = float(split_str[14])
            traveled_blocks = float(split_str[5])
            acc_bo=float(split_str[6])
            acc_eo=float(split_str[7])

            particle=[acc_group_size,acc_bo+acc_eo]
            all_particles.append(particle)
        fo.close()

    print("collected particle number:", len(all_particles))
    
    # sort particles from small to large
    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    time_list=[]
    for p in all_particles_sorted:
        time_list.append(p[1])
    
    ax.set_ylim([0,0.8*1e8])
    xpos = range(0, len(time_list),1)
    print(len(xpos),len(time_list))

    ax.bar(xpos,time_list)
    #ax.set_xticks([0,len(xpos)/2,len(xpos)])
    #ax.set_xticklabels(['0','320000','640000'])
    ax.set_xticks([])
    if data_name=="Tokamak":
        ax.set_ylabel(r'$Σ T_{BO}+Σ T_{EO}$ (us)', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])
    ax.title.set_text(figid)
    ax.title.set_fontsize(labelSize)

# parse the timetrace log and draw the gantt chart
if __name__ == "__main__":
    
    if len(sys.argv)!=3:
        print("<binary> <procs> <dirpath for all data>")
        exit()

    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    simSycle=0
    dirPath=sys.argv[2]


    # dataname=["fusion.A.b128.n4.r128.B_p5000_s2000",
    #          "astro.A.b128.n4.r128.B_p5000_s2000",
    #          "fishtank.A.b128.n4.r128.B_p5000_s2000_id625027",
    #          "clover.A.b128.n4.r128.B_p5000_s2000",
    #          "syn.A.b128.n4.r128.B_p5000_s2000"]


    dataname=["fusion.A.b128.n4.r128.B_p5000_s2000_id582493",
              "astro.A.b128.n4.r128.B_p5000_s2000_id418463",
              "fishtank.A.b128.n4.r128.B_p5000_s2000_id625027",
              "clover.A.b128.n4.r128.B_p5000_s2000_id275499",
              "syn.A.b128.n4.r128.B_p5000_s2000_id365728"]

    # dataname=["fusion.A.b128.n4.r128.B_p5000_s2000_id582493_PPP6000",
    #           "astro.A.b128.n4.r128.B_p5000_s2000_id255124_PPP6000",
    #           "fishtank.A.b128.n4.r128.B_p5000_s2000_id625027_PPP6000",
    #           "clover.A.b128.n4.r128.B_p5000_s2000_id275499_PPP6000",
    #           "syn.A.b128.n4.r128.B_p5000_s2000_id365728_PPP6000"]

    official_name = ["Tokamak","Supernova","Hydraulics","CloverLeaf3D","Synthetic"]
   
    nr=5
    fig, axs = plt.subplots(nrows=nr, ncols=5, figsize=(figsize_x*5,figsize_y*nr)) 
    plt.subplots_adjust(wspace=0, hspace=0.2)
    for index, data in enumerate(dataname):
        dirname_complete = dirPath+"/"+data
        print("dirname",dirname_complete,"index",index)
        figid = "(a."+str(index+1)+")"
        draw_alive_time(axs[0][index],procs,dirname_complete, official_name[index], figid)


    for index, data in enumerate(dataname):
        dirname_complete = dirPath+"/"+data
        print("dirname",dirname_complete,"index",index)
        figid = "(b."+str(index+1)+")"
        draw_acc_wait(axs[1][index],procs,dirname_complete, official_name[index],figid)

    for index, data in enumerate(dataname):
         dirname_complete = dirPath+"/"+data
         print("dirname",dirname_complete,"index",index)
         figid = "(c."+str(index+1)+")"
         draw_acc_adv(axs[2][index],procs,dirname_complete, official_name[index],figid)

    for index, data in enumerate(dataname):
         dirname_complete = dirPath+"/"+data
         print("dirname",dirname_complete,"index",index)
         figid = "(d."+str(index+1)+")"
         draw_acc_bo_eo(axs[3][index],procs,dirname_complete, official_name[index],figid)


    for index, data in enumerate(dataname):
        dirname_complete = dirPath+"/"+data
        print("dirname",dirname_complete,"index",index)
        figid = "(e."+str(index+1)+")"
        draw_acc_group_size(axs[4][index],procs,dirname_complete, official_name[index],figid)

    # for index, data in enumerate(dataname):
    #     dirname_complete = dirPath+"/"+data
    #     print("dirname",dirname_complete,"index",index)
    #     figid = "(f."+str(index+1)+")"
    #     draw_acc_prev_group_size(axs[5][index],procs,dirname_complete, official_name[index],figid)

    # for index, data in enumerate(dataname):
    #     dirname_complete = dirPath+"/"+data
    #     print("dirname",dirname_complete,"index",index)
    #     figid = "(d."+str(index+1)+")"
    #     draw_acc_and_prv_group_size(axs[3][index],procs,dirname_complete, official_name[index],figid)

    #for index, data in enumerate(dataname):
    #    dirname_complete = dirPath+"/"+data
    #    print("dirname",dirname_complete,"index",index)
    #    figid = "(f."+str(index+1)+")"
    #    draw_comm_times(axs[5][index],procs,dirname_complete, official_name[index],figid)

    fig.text(0.5, 0.08, 'Particles sorted by accumulated group size', ha='center',fontsize=labelSize)

    fig.savefig("particles_all_dots_statistics.png",bbox_inches='tight',dpi=800)
    fig.savefig("particles_all_dots_statistics.pdf",bbox_inches='tight')



