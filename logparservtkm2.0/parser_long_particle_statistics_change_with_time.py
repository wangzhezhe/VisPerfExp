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

figsize_x = 8
figsize_y = 5

scatterSize=4

def draw_adjust_prev_group_num(ax,procs,dirPath,data_name,figid):
    all_particles=[]
    i=0

    for rank in range(0,procs,1):
        recvok=0
        gang_comm_start=0
        prev_gang=0
        desirilize_time=0
        file_name = dirPath+"/particle_tracing_details."+str(rank)+".out"
        fo=open(file_name, "r")

        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")

            if split_str[0]=="RECVOK":
                recvok=float(split_str[4])

            #if split_str[0]=="GANG_COMM_END":
            if split_str[0]=="ParticleSendBegin":
                gang_comm_start=float(split_str[4])
                all_particles.append([recvok,gang_comm_start,rank])

    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    i=0
    #if data_name=="Supernova":
        #for p in all_particles_sorted:
        #    print(i,p)
        #    i=i+1

    ax.set_ylim([0,20])
    
    #print(all_particles_sorted)

    #for index, p in enumerate(all_particles_sorted):
        #if index>0 and data_name=="CloverLeaf3D":
            #print("debug sorted", p, "wait",all_particles_sorted[index][0]-all_particles_sorted[index-1][1])
    
    print("debug data set",data_name)

    if data_name=="Tokamak":
        ax.set_ylabel('# groups during comm&wait', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])

    ax.title.set_text(figid+data_name)
    ax.title.set_fontsize(labelSize)

    #compute prev group
    all_time_pos =[]
    prev_group=[]
    prev_group_num=[]
    for index, p in enumerate(all_particles_sorted):
        if index>0:
            debug_time=101826000
            # the x axis is the time when particle is recieved
            send_time_from_src=all_particles_sorted[index-1][1]
            recv_time_of_dst=all_particles_sorted[index][0]
            dst_rank=all_particles_sorted[index][2]
            if int(recv_time_of_dst)==debug_time:
                print("debug start",send_time_from_src,recv_time_of_dst)

            if send_time_from_src>recv_time_of_dst:
                print ("debug wrong wait gap",send_time_from_src,recv_time_of_dst)

            # open dst rank, check how many group in specific range
            # print("file_name",file_name,send_time_from_src,recv_time_of_dst)
            file_name = dirPath+"/timetrace."+str(dst_rank)+".out"
            fo=open(file_name, "r")
            
            adv_start_time=0
            adv_end_time=0
            # one value per file search
            temp_group=0
            prev_group_element=0
            temp_group_num=0
            debug_split_str=""
            contain_particle_advect_info=False

            for line in fo:
                line_strip=line.strip()
                split_str= line_strip.split(" ")
                # iteration in dst ranks
                if split_str[0]=="AdvectStart_0":
                    adv_start_time=float(split_str[1])
                    # reset temp group to 0 when new iteration start
                    temp_group=0
                    # the start position of a new iteration
                    contain_particle_advect_info=False
                if "ParticleAdvectInfo" in split_str[0]:
                    split_str_advct=split_str[0].split("_")
                    temp_group=float(split_str_advct[1])
                    debug_split_str=split_str
                    find_complete_adv_period=True
                    #if int(recv_time_of_dst)==debug_time:
                    #    print(split_str_advct,temp_group)
                    #if data_name=="Supernova" and dst_rank==76:
                    #    print(temp_group)
                    contain_particle_advect_info=True
                if split_str[0]=="AdvectEnd_0":
                    adv_end_time=float(split_str[1])

                    if int(recv_time_of_dst)==debug_time:
                        print("debug adv start",adv_start_time, "comm end", adv_end_time, "temp_group", temp_group)
                    
                    # when finding an avalible advec start and end
                    # do not have actual advection particles
                    if contain_particle_advect_info==False:
                        continue

                    # find complete adv period
                    if int(adv_start_time)<int(send_time_from_src) and int(send_time_from_src)<=int(adv_end_time) and int(adv_end_time)<int(recv_time_of_dst):
                        # Attention, there are some issues in this way, when there is partial overlapping, if count it???
                        prev_group_element=prev_group_element+temp_group
                        temp_group_num=temp_group_num+1
                        #prev_group_element+=temp_group*(recv_time_of_dst-adv_end_time)/(adv_end_time-adv_start_time)
                    
                    # only count fully overlapping case
                    if adv_start_time>=send_time_from_src and adv_end_time<=recv_time_of_dst:
                        #prev_group.append(temp_group)
                        prev_group_element=prev_group_element+temp_group
                        temp_group_num=temp_group_num+1

                    #if adv_start_time>send_time_from_src and adv_start_time<recv_time_of_dst and adv_end_time>recv_time_of_dst:
                        #prev_group.append(temp_group)
                    #    prev_group_element+=temp_group

                    #   Try to check if the start time and adv time is valid

                if adv_start_time>recv_time_of_dst:
                    break

            fo.close()
            #print(dst_rank)
            #print(len(prev_group))
            if int(recv_time_of_dst)==debug_time:
                print("append prev_group_element",prev_group_element)
            prev_group.append(prev_group_element)
            prev_group_num.append(temp_group_num)
            all_time_pos.append(all_particles_sorted[index][0])
    ax.scatter(all_time_pos,prev_group_num, s=scatterSize)


def draw_adjust_prev_gang_time(ax,procs,dirPath,data_name,figid):
    all_particles=[]
    i=0

    for rank in range(0,procs,1):
        recvok=0
        gang_comm_start=0
        prev_gang=0
        desirilize_time=0
        file_name = dirPath+"/particle_tracing_details."+str(rank)+".out"
        fo=open(file_name, "r")

        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")

            if split_str[0]=="RECVOK":
                recvok=float(split_str[4])

            #if split_str[0]=="GANG_COMM_END":
            if split_str[0]=="ParticleSendBegin":
                gang_comm_start=float(split_str[4])
                all_particles.append([recvok,gang_comm_start,rank])

    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    i=0
    #if data_name=="Supernova":
        #for p in all_particles_sorted:
        #    print(i,p)
        #    i=i+1

    ax.set_ylim([0,100000])
    
    #print(all_particles_sorted)

    # for index, p in enumerate(all_particles_sorted):
    #     if index>0 and data_name=="CloverLeaf3D":
    #         print("debug sorted", p, "wait",all_particles_sorted[index][0]-all_particles_sorted[index-1][1])
    
    print("debug data set",data_name)

    if data_name=="Tokamak":
        ax.set_ylabel('Adjusted prev gang', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])

    ax.title.set_text(figid+data_name)
    ax.title.set_fontsize(labelSize)

    #compute prev group
    all_time_pos =[]
    prev_group=[]
    prev_group_num=[]
    for index, p in enumerate(all_particles_sorted):
        if index>0:
            debug_time=101826000
            # the x axis is the time when particle is recieved
            send_time_from_src=all_particles_sorted[index-1][1]
            recv_time_of_dst=all_particles_sorted[index][0]
            src_rank=all_particles_sorted[index-1][2]
            dst_rank=all_particles_sorted[index][2]
            if int(recv_time_of_dst)==debug_time:
                print("debug start",send_time_from_src,recv_time_of_dst)

            if send_time_from_src>recv_time_of_dst:
                print ("debug wrong wait gap",send_time_from_src,recv_time_of_dst)

            # open dst rank, check how many group in specific range
            # print("file_name",file_name,send_time_from_src,recv_time_of_dst)
            file_name = dirPath+"/timetrace."+str(dst_rank)+".out"
            print(file_name)
            fo=open(file_name, "r")
            
            adv_start_time=0
            adv_end_time=0
            # one value per file search
            temp_group=0
            prev_group_element=0
            temp_group_num=0
            debug_split_str=""
            contain_particle_advect_info=False

            for line in fo:
                line_strip=line.strip()
                split_str= line_strip.split(" ")
                # iteration in dst ranks
                if split_str[0]=="AdvectStart_0":
                    adv_start_time=float(split_str[1])
                    # reset temp group to 0 when new iteration start
                    temp_group=0
                    # the start position of a new iteration
                    contain_particle_advect_info=False
                if "ParticleAdvectInfo" in split_str[0]:
                    split_str_advct=split_str[0].split("_")
                    temp_group=float(split_str_advct[1])
                    debug_split_str=split_str
                    find_complete_adv_period=True
                    #if int(recv_time_of_dst)==debug_time:
                    #    print(split_str_advct,temp_group)
                    #if data_name=="Supernova" and dst_rank==76:
                    #    print(temp_group)
                    contain_particle_advect_info=True
                if split_str[0]=="AdvectEnd_0":
                    adv_end_time=float(split_str[1])

                    if int(recv_time_of_dst)==debug_time:
                        print("debug adv start",adv_start_time, "comm end", adv_end_time, "temp_group", temp_group)
                    
                    # when finding an avalible advec start and end
                    # do not have actual advection particles
                    if contain_particle_advect_info==False:
                        continue

                    # find complete adv period
                    if int(adv_start_time)<int(send_time_from_src) and int(send_time_from_src)<=int(adv_end_time) and int(adv_end_time)<int(recv_time_of_dst):
                        # Attention, there are some issues in this way, when there is partial overlapping, if count it???
                        prev_group_element=prev_group_element+temp_group
                        temp_group_num=temp_group_num+1
                        #prev_group_element+=temp_group*(recv_time_of_dst-adv_end_time)/(adv_end_time-adv_start_time)
                        #print("debug overlapping part", recv_time_of_dst-adv_end_time)
                        #if send_time_from_src==int(3752710) and  recv_time_of_dst==int(3796620):
                        #   print("debug large temp group", temp_group_num, prev_group_element, "dst_rank",dst_rank,"wait gap",send_time_from_src, recv_time_of_dst,"wait time",recv_time_of_dst-send_time_from_src, "adv gap",adv_start_time,adv_end_time,"prev_group_element",prev_group_element,"debug_split_str",debug_split_str)

                    
                    # only count fully overlapping case
                    if int(adv_start_time)>=int(send_time_from_src) and int(adv_end_time)<=int(recv_time_of_dst):
                        #prev_group.append(temp_group)
                        prev_group_element=prev_group_element+temp_group
                        temp_group_num=temp_group_num+1
                        #if send_time_from_src==int(3752710) and  recv_time_of_dst==int(3796620):
                        #    print("debug large temp group", temp_group_num, prev_group_element, "dst_rank",dst_rank,"wait gap",send_time_from_src, recv_time_of_dst,"wait time",recv_time_of_dst-send_time_from_src, "adv gap",adv_start_time,adv_end_time,"prev_group_element",prev_group_element,"debug_split_str",debug_split_str)


                    #if adv_start_time>send_time_from_src and adv_start_time<recv_time_of_dst and adv_end_time>recv_time_of_dst:
                        #prev_group.append(temp_group)
                    #    prev_group_element+=temp_group

                    #   Try to check if the start time and adv time is valid


                    if adv_start_time>adv_end_time:
                        print ("debug wrong adv time",adv_start_time,adv_end_time)

                    if temp_group_num==0 and prev_group_element!=0:
                        print(temp_group_num,prev_group_element,"dst_rank",dst_rank,"wait gap",send_time_from_src, recv_time_of_dst, "wait time",recv_time_of_dst-send_time_from_src, "adv gap",adv_start_time,adv_end_time,"prev_group_element",prev_group_element,"debug_split_str",debug_split_str)
                
                    if temp_group_num>0 and prev_group_element==0:
                        print(temp_group_num,prev_group_element,"dst_rank",dst_rank,"wait gap",send_time_from_src, recv_time_of_dst,"wait time",recv_time_of_dst-send_time_from_src, "adv gap",adv_start_time,adv_end_time,"prev_group_element",prev_group_element,"debug_split_str",debug_split_str)

                    if temp_group_num>1:
                        print("debug large temp group", temp_group_num, prev_group_element, "dst_rank",dst_rank,"wait gap",send_time_from_src, recv_time_of_dst,"wait time",recv_time_of_dst-send_time_from_src, "adv gap",adv_start_time,adv_end_time,"prev_group_element",prev_group_element,"debug_split_str",debug_split_str)
                    


                if adv_start_time>recv_time_of_dst:
                    break

            fo.close()
            #print(dst_rank)
            #print(len(prev_group))
            if int(recv_time_of_dst)==debug_time:
                print("append prev_group_element",prev_group_element)
            prev_group.append(prev_group_element)
            prev_group_num.append(temp_group_num)
            all_time_pos.append(all_particles_sorted[index][0])

    if data_name=="CloverLeaf3D":
        print("debug clover prev_group",prev_group)
    ax.scatter(all_time_pos,prev_group, s=scatterSize)

def draw_deserilize_time(ax,procs,dirPath,data_name,figid):
    all_particles=[]
    i=0

    for rank in range(0,procs,1):
        recvok=0
        gang_comm_start=0
        prev_gang=0
        desirilize_time=0
        file_name = dirPath+"/particle_tracing_details."+str(rank)+".out"
        fo=open(file_name, "r")

        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")

            if split_str[0]=="DESERIALIZE_PARTICLES":
                desirilize_time=float(split_str[4])

            if split_str[0]=="RECVOK":
                recvok=float(split_str[4])

            if split_str[0]=="ADVECTEND":
                prev_gang=float(split_str[7])

            if split_str[0]=="GANG_COMM_START":
                gang_comm_start=float(split_str[4])
                all_particles.append([recvok,gang_comm_start,rank,prev_gang,desirilize_time])

    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    i=0
    # if data_name=="Supernova":
    #     for p in all_particles_sorted:
    #         print(i,p)
    #         i=i+1

    ax.set_ylim([0,100000])
    
    #print(all_particles_sorted)
    if data_name=="Tokamak":
        ax.set_ylabel('Deserialization time (us)', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])

    ax.title.set_text(figid+data_name)
    ax.title.set_fontsize(labelSize)

    #compute wait time
    all_draw_time=[]
    all_time_pos =[]
    for index, p in enumerate(all_particles_sorted):
        if index>0:
            # the x axis is the time when particle is recieved
            des_time = p[4]
            all_draw_time.append(des_time)
            #using comm end as the x position
            all_time_pos.append(all_particles_sorted[index][0])
    
    #print(all_wait_time)
    #print(all_time_pos)
    #print(all_draw_time)
    ax.scatter(all_time_pos,all_draw_time, s=scatterSize)

def draw_comm_wait_time(ax,procs,dirPath,data_name,figid):
    all_particles=[]
    i=0
    for rank in range(0,procs,1):
        recvok=0
        gang_comm_start=0
        prev_gang=0
        file_name = dirPath+"/particle_tracing_details."+str(rank)+".out"
        fo=open(file_name, "r")

        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")

            if split_str[0]=="RECVOK":
                recvok=float(split_str[4])

            if split_str[0]=="ADVECTEND":
                prev_gang=float(split_str[7])

            if split_str[0]=="GANG_COMM_START":
                gang_comm_start=float(split_str[4])
                all_particles.append([recvok,gang_comm_start,rank,prev_gang])

    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    i=0
    if data_name=="Supernova":
        for p in all_particles_sorted:
            #print(i,p)
            i=i+1

    ax.set_ylim([0,3*1e6])
    #if data_name=="CloverLeaf3D":
    #    print("debug wait time, CloverLeaf3D all_particles_sorted",all_particles_sorted)
    
    if data_name=="Tokamak":
        ax.set_ylabel('Comm & wait time(us)', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])

    ax.title.set_text(figid+data_name)
    ax.title.set_fontsize(labelSize)

    #compute wait time
    all_wait_time=[]
    all_time_pos =[]
    for index, p in enumerate(all_particles_sorted):
        if index>0:
            wait_time = all_particles_sorted[index][0]-all_particles_sorted[index-1][1]
            all_wait_time.append(wait_time)
            #if data_name=="CloverLeaf3D":
            #    print("debug wait time", index,wait_time,"src", all_particles_sorted[index-1][2], "dst", all_particles_sorted[index][2], "sent",all_particles_sorted[index-1][1],"recv",all_particles_sorted[index][0])
            #using comm end as the x position
            all_time_pos.append(all_particles_sorted[index][0])
    
    if data_name=="CloverLeaf3D":
        print("debug clover wait time", all_wait_time)
    ax.scatter(all_time_pos,all_wait_time, s=scatterSize)


def draw_curr_gang_size(ax,procs,dirPath,data_name,figid):
    all_particles=[]
    i=0

    for rank in range(0,procs,1):
        gang_comm_start=0
        file_name = dirPath+"/particle_tracing_details."+str(rank)+".out"
        fo=open(file_name, "r")
        curr_gang=0
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")

            if split_str[0]=="ADVECTEND":
                curr_gang=float(split_str[6])
            if split_str[0]=="GANG_COMM_START":
                gang_comm_start=float(split_str[4])
                all_particles.append([gang_comm_start,curr_gang])

    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])

    ax.set_ylim([0,100000])
    
    #print(all_particles_sorted)
    if data_name=="Tokamak":
        ax.set_ylabel('Curr gang size', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])

    ax.title.set_text(figid+data_name)
    ax.title.set_fontsize(labelSize)

    #compute wait time
    all_gang_size=[]
    all_time_pos =[]
    for index, p in enumerate(all_particles_sorted):
        if index>0:
            all_gang_size.append(p[1])
            #using comm end as the x position
            all_time_pos.append(p[0])
    
    ax.scatter(all_time_pos,all_gang_size, s=scatterSize)

def draw_prev_gang_size(ax,procs,dirPath,data_name,figid):
    all_particles=[]
    i=0

    for rank in range(0,procs,1):
        gang_comm_start=0
        file_name = dirPath+"/particle_tracing_details."+str(rank)+".out"
        fo=open(file_name, "r")
        prev_gang=0
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")

            if split_str[0]=="ADVECTEND":
                prev_gang=float(split_str[7])
            if split_str[0]=="GANG_COMM_START":
                gang_comm_start=float(split_str[4])
                all_particles.append([gang_comm_start,prev_gang])

    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    


    ax.set_ylim([0,100000])
    
    #print(all_particles_sorted)
    if data_name=="Tokamak":
        ax.set_ylabel('Naive prev gang size', fontsize=labelSize)
        ax.tick_params(axis='y', labelsize=tickSize)
    else:
        ax.set_yticks([])

    ax.title.set_text(figid+data_name)
    ax.title.set_fontsize(labelSize)

    #compute wait time
    all_gang_size=[]
    all_time_pos =[]
    for index, p in enumerate(all_particles_sorted):
        if index>0:
            all_gang_size.append(p[1])
            #using comm end as the x position
            all_time_pos.append(p[0])
    
    ax.scatter(all_time_pos,all_gang_size, s=scatterSize)


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

    # dataname=["fusion.A.b128.n4.r128.SINGLE_p5000_s2000_id0",
    #           "astro.A.b128.n4.r128.SINGLE_p5000_s2000_id0",
    #           "fishtank.A.b128.n4.r128.SINGLE_p5000_s2000_id0",
    #           "clover.A.b128.n4.r128.SINGLE_p5000_s2000_id0",
    #           "syn.A.b128.n4.r128.SINGLE_p5000_s2000_id0"]

    #dataname=["astro.A.b128.n4.r128.B_p5000_s2000_id418463"]

    official_name = ["Tokamak","Supernova","Hydraulics","CloverLeaf3D","Synthetic"]
   
    nr=5
    fig, axs = plt.subplots(nrows=nr, ncols=5, figsize=(figsize_x*5,figsize_y*nr)) 

    for index, data in enumerate(dataname):
        dirname_complete = dirPath+"/"+data
        print("dirname",dirname_complete,"index",index)
        figid = "(a."+str(index+1)+")"
        draw_comm_wait_time(axs[0][index],procs,dirname_complete, official_name[index], figid)


    for index, data in enumerate(dataname):
        dirname_complete = dirPath+"/"+data
        print("dirname",dirname_complete,"index",index)
        figid = "(b."+str(index+1)+")"
        draw_curr_gang_size(axs[1][index],procs,dirname_complete, official_name[index], figid)


    # for index, data in enumerate(dataname):
    #     dirname_complete = dirPath+"/"+data
    #     print("dirname",dirname_complete,"index",index)
    #     figid = "(c."+str(index+1)+")"
    #     draw_prev_gang_size(axs[2][index],procs,dirname_complete, official_name[index], figid)

    for index, data in enumerate(dataname):
        dirname_complete = dirPath+"/"+data
        print("dirname",dirname_complete,"index",index)
        figid = "(c."+str(index+1)+")"
        draw_deserilize_time(axs[2][index],procs,dirname_complete, official_name[index], figid)
    
    for index, data in enumerate(dataname):
        dirname_complete = dirPath+"/"+data
        print("dirname",dirname_complete,"index",index)
        figid = "(d."+str(index+1)+")"
        #if official_name[index]=="CloverLeaf3D":
        draw_adjust_prev_gang_time(axs[3][index],procs,dirname_complete, official_name[index], figid)
    
    #draw prev_group_num_list for sanity check
    for index, data in enumerate(dataname):
        dirname_complete = dirPath+"/"+data
        print("dirname",dirname_complete,"index",index)
        figid = "(d."+str(index+1)+")"
        #if official_name[index]=="CloverLeaf3D":
        draw_adjust_prev_group_num(axs[4][index],procs,dirname_complete, official_name[index], figid)   

    fig.text(0.5, 0.08, 'Time (us)', ha='center',fontsize=labelSize)

    fig.savefig("parser_long_particle_statistics_change_with_time.png",bbox_inches='tight',dpi=600)
    fig.savefig("parser_long_particle_statistics_change_with_time.pdf",bbox_inches='tight')