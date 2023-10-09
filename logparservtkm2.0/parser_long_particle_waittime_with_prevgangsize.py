from os import system
from os.path import exists
import sys
import math
import scipy.stats
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

scatterSize=60

def draw_comm_wait_time_with_prev_gang(ax,procs,dirPath,data_name,figid):
    all_particles=[]
    i=0

    for rank in range(0,procs,1):
        recvok=0
        gang_comm_start=0
        prev_gang=0
        desirilize_time=0
        curr_gang_size=0
        file_name = dirPath+"/particle_tracing_details."+str(rank)+".out"
        fo=open(file_name, "r")

        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")

            if split_str[0]=="RECVOK":
                recvok=float(split_str[4])

            if split_str[0]=="ADVECTSTART":
                curr_gang_size=float(split_str[6])

            #if split_str[0]=="GANG_COMM_END":
            if split_str[0]=="ParticleSendEnd":
                gang_send_out=float(split_str[4])
                all_particles.append([recvok,gang_send_out,rank,curr_gang_size ])

    all_particles_sorted=sorted(all_particles, key=lambda x: x[0])
    
    #ax.set_ylim([0,100000])
    
    #print(all_particles_sorted)

    if data_name=="Tokamak":
        ax.set_ylabel('Comm & wait time (us)', fontsize=labelSize)
    
    ax.tick_params(axis='y', labelsize=tickSize)
    #else:
    #    ax.set_yticks([])

    ax.title.set_text(figid+data_name)
    ax.title.set_fontsize(labelSize)

    #compute prev group
    wait_time =[]
    prev_group=[]
    all_time_pos =[]
    curr_gang_size_list=[]
    for index, p in enumerate(all_particles_sorted):
        if index>0:
            debug_time=101826000
            # the x axis is the time when particle is recieved
            send_time_from_src=all_particles_sorted[index-1][1]
            recv_time_of_dst=all_particles_sorted[index][0]
            dst_rank=all_particles_sorted[index][2]
            temp_curr_group=all_particles_sorted[index-1][3]
            
            wait_time.append(recv_time_of_dst-send_time_from_src)
            if int(recv_time_of_dst)==debug_time:
                print("debug start",send_time_from_src,recv_time_of_dst)

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
                        #print("debug overlapping part", recv_time_of_dst-adv_end_time)
                    
                    # only count fully overlapping case
                    if int(adv_start_time)>=int(send_time_from_src) and int(adv_end_time)<=int(recv_time_of_dst):
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

            prev_group.append(prev_group_element)
            all_time_pos.append(all_particles_sorted[index][0])
            curr_gang_size_list.append(temp_curr_group)

    
    #print(all_wait_time)
    #print(len(all_particles_sorted))
    #print(len(prev_group))
    #print(len(wait_time))
    #print("debug prev_group", prev_group)
    # color by all time pos
    scatter_plot = ax.scatter(prev_group, wait_time, s=scatterSize, c=all_time_pos, cmap='viridis_r')
    # color by current gang size
    #scatter_plot = ax.scatter(prev_group, wait_time, s=scatterSize, c=curr_gang_size_list, cmap='viridis_r')



    #plt.colorbar(scatter_plot,cax=ax,orientation='horizontal')
    fig.colorbar(scatter_plot, ax=ax)

    # draw the fitted poly line
    b, a = np.polyfit(prev_group, wait_time, deg=1)

    # Create sequence of 100 numbers from 0 to 100 
    xseq = np.linspace(0, max(prev_group), num=100)

    # Plot regression line
    ax.plot(xseq, a + b * xseq, color="k", lw=1.0)

    corr = scipy.stats.pearsonr(prev_group, wait_time)
    print(corr)


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
   
    nr=1
    fig, axs = plt.subplots(nrows=nr, ncols=5, figsize=(figsize_x*5,figsize_y*nr)) 

    for index, data in enumerate(dataname):
        dirname_complete = dirPath+"/"+data
        print("dirname",dirname_complete,"index",index)
        figid = ""
        draw_comm_wait_time_with_prev_gang(axs[index],procs,dirname_complete, official_name[index], figid)

    fig.text(0.5, 0.01, 'Total sizes of advected groups in dest rank during comm&wait time (partially overlapped group is also counted)', ha='center',fontsize=labelSize)

    fig.savefig("parser_long_particle_waittime_with_prevgangsize.png",bbox_inches='tight',dpi=400)
    fig.savefig("parser_long_particle_waittime_with_prevgangsize.pdf",bbox_inches='tight')