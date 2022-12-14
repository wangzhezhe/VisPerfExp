
from os import system
from os.path import exists
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import statistics

def advect_distribution(list_advec_all, go_time, figsize_x):
    # draw the distribution of the advect time
    # x is teh start time
    # y is the legth/height of the bar
    
    procs = len(list_advec_all)
    #print(list_advec_all)
    #print("advect_distribution procs",procs)

    # there are issues to use axs[0] if there are one procs
    fig, axs = plt.subplots(procs)
    
    #figsize_y=2
    #plt.ylim([0, figsize_y])
 
    max_y=0
    for i in range (0,procs,1):
        for t in list_advec_all[i]:
            max_y=max(max_y,t[1]) 

    # make the figure the same sequence with the gant table
    # the axs 0 is at the top here, it should store the rank[proc-1] case
    for i in range (0,procs,1):
        x=[]
        y=[]
        for t in list_advec_all[procs-i-1]:
            x.append(t[0])
            y.append(t[1])
        #print(x,y)
        #print("debug",i,x,y)
        axs[i].bar(x, y, width=0.05)
        if i==procs-1:
            axs[i].set_xticks((0,figsize_x/2,figsize_x))
            axs[i].set_xticklabels((0,go_time/2, go_time))
            axs[i].set_xlabel('Time(ms)', fontsize="large")

        else:
            axs[i].tick_params(labelbottom=False)
        
        axs[i].set_ylim(0, max_y+0.1) 
        axs[i].set_ylabel("R"+str(procs-i-1))
        
        axs[i].tick_params(labelleft=False)
        axs[i].set_yticklabels([])
        #remove that small tick line
        axs[i].yaxis.set_ticks_position('none')

        axs[i].set_xlim([0, figsize_x])

    #plt.xticks([0,8,16], [0,go_time/2, go_time])
    fig.savefig('advect_distribution_all.png')
    

def comm_distribution(list_comm_all, go_time, figsize_x):
    # draw the distribution of the advect time
    # x is teh start time
    # y is the legth/height of the bar
    
    procs = len(list_comm_all)
    #print(list_comm_all)
    #print("advect_distribution procs",procs)
    fig, axs = plt.subplots(procs)
    #figsize_y=2
    #plt.ylim([0, figsize_y])

    
    max_y=0
    for i in range (0,procs,1):
        for t in list_comm_all[i]:
            max_y=max(max_y,t[1]) 

    # make the figure the same sequence with the gant table
    # the axs 0 is at the top here, it should store the rank[proc-1] case
    for i in range (0,procs,1):
        x=[]
        y=[]
        for t in list_comm_all[procs-i-1]:
            x.append(t[0])
            y.append(t[1])
        #print(x,y)
        axs[i].bar(x, y, width=0.05, color='tab:red',alpha=0.8)
        if i==procs-1:
            axs[i].set_xticks((0,figsize_x/2,figsize_x))
            axs[i].set_xticklabels((0,go_time/2, go_time))
            axs[i].set_xlabel('Time(ms)', fontsize="large")

        else:
            axs[i].tick_params(labelbottom=False)
        
        #remove that small tick line
        ax.yaxis.set_ticks_position('none')

        axs[i].set_ylim(0, max_y+0.1) 
        axs[i].set_ylabel("R"+str(procs-i-1))
        
        axs[i].tick_params(labelleft=False)

        axs[i].set_yticklabels([])
        #remove that small tick line
        axs[i].yaxis.set_ticks_position('none')

        axs[i].set_xlim([0, figsize_x])



    #plt.xticks([0,8,16], [0,go_time/2, go_time])
    fig.savefig('comm_distribution_all.png')



# parse the timetrace log and draw the gant chart
if __name__ == "__main__":
    
    if len(sys.argv)!=4:
        print("<binary> <procs> <step> <dirpath>")
        exit()
   
    procs=int(sys.argv[1])
    # for each procs, the operations are executed multiple steps
    step=sys.argv[2]
    dirPath=sys.argv[3]

    rank0_start_time=0
    figsize_x = 16
    bar_height=0.5
    # give some place for legend
    figsize_y = procs*bar_height+1
    fig, ax = plt.subplots(1, figsize=(figsize_x,figsize_y))    

    list_advec_all=[]
    list_comm_all=[]

    list_getp_accumulated=[]
    list_adv_accumulated=[]
    list_classify_accumulated=[]
    list_sr_accumulated=[]
    list_wait_accumulated=[]   
    list_meta_accumulated=[]
    list_while_accumulated=[]   

    
    for rank in range(0,procs,1):
        file_name = dirPath+"/timetrace."+str(rank)+".out"
        print(file_name)

        fo=open(file_name, "r")
    
        adevct_start="AdvectStart_"+str(step)+" "
        adevct_end="AdvectEnd_"+str(step)+" "

        comm_start="CommStart_"+str(step)+" "
        comm_end="CommEnd_"+str(step)+" "

        go_start = "GoStart_"+str(step)+" "    
        go_end = "GoEnd_"+str(step)+" "

        while_start = "WhileStart_" +str(step)+" "
        while_end = "WhileEnd_" +str(step)+" "

        send_start="SendStart_" +str(step)+" "
        send_end="SendEnd_" +str(step)+" "

        recv_start="RecvStart_" +str(step)+" "
        recv_end="RecvEnd_" +str(step)+" "

        update_result="UpdateResultOK_"+str(step)+" "
        get_particle_ok="getParticleOK_"+str(step)+" "

        init = "Init_"+str(step)+" "
        # compute the total time and use this to compute the bar length
        # there is variance for multiprocess case
        # different ranks starts at different time   

        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(" ")
            if go_start in line_strip:
                go_start_time = int(split_str[1])       
            if go_end in line_strip:
                go_end_time = int(split_str[1])

        fo.close() 

        if rank==0:
            rank0_start_time=go_start_time
        
        if rank==0:
            offset=0
        else:
            offset= go_start_time - rank0_start_time
    
        go_time = (go_end_time - go_start_time)
        print("rank",rank,"total time ",go_time)
        offset = figsize_x*(offset/go_time)
        print("rank",rank,"offset",offset)

        advect_start_time_relative=0
        advect_end_time_relative=0
        comm_start_time_relative=0
        comm_end_time_relative=0
        while_start_time_relative=0
        while_end_time_relative=0

        send_end_time_relative=0
        send_end_time_relative=0
        recv_start_time_relative=0
        recv_end_time_relative=0
        
        getp_accumulated_perproc=0
        adv_accumulated_perproc=0
        classify_accumulated_perproc=0
        sr_accumulated_perproc=0
        comm_accumulated_perproc=0   
        meta_accumulated_perproc=0
        while_accumulate_perproc=0
    
        # all the width should be proportional to this figsize_x
        # when we use the micro second, some iteration happens quickly and 
        # the start time is the same with the end time
        # the granularity is 1ms, if the two timer is less than 1ms, we could not draw it

        plt.xticks([0,figsize_x/4,figsize_x/2,3*figsize_x/4,figsize_x], [0,go_time/4,go_time/2, 3*go_time/4,go_time])
        #plt.xticks([0,figsize_x/4,figsize_x/2,3*figsize_x/4,figsize_x], [0,figsize_x/4,figsize_x/2,3*figsize_x/4,figsize_x])

        proc_id=list(range(0, procs))
        # tick position in figure and tick text value
        plt.yticks(bar_height*np.array(proc_id)+0.5*bar_height-0.05,proc_id)

        barh_list_advec=[]
        barh_list_comm=[]
        barh_list_while=[]
        barh_list_actual_send=[]
        barh_list_actual_recv=[]
        
        barh_list_get_active_particles=[]
        barh_list_advec_raw=[]
        barh_list_update_result=[]
        barh_list_update_terminated=[]
        barh_list_init=[]
        
        # read file again
        fo=open(file_name, "r")
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(" ")


            if init in line_strip:
                init_time_relative=int(split_str[1])-go_start_time
                print("init_time_relative",init_time_relative)
                width = (init_time_relative)/go_time
                barh_list_init.append((0,width*figsize_x))

            if while_start in line_strip:
                while_start_time_relative = int(split_str[1])-go_start_time

            if adevct_start in line_strip:
                #print("advect line strip",line_strip)
                advect_start_time_relative=int(split_str[1])-go_start_time
                #print("adevct start",int(split_str[1]))


            if get_particle_ok in line_strip:
                get_particle_ok_time_relative=int(split_str[1])-go_start_time
                getp_spent_time=get_particle_ok_time_relative-while_start_time_relative
                getp_accumulated_perproc=getp_accumulated_perproc+getp_spent_time
                width = (getp_spent_time)/go_time
                if width<0:
                    print("get particles error",get_particle_ok_time_relative, while_start_time_relative)
                # use start position
                barh_list_get_active_particles.append((offset+figsize_x*(while_start_time_relative/go_time),width*figsize_x))

                
            if adevct_end in line_strip:
                advect_end_time_relative=int(split_str[1])-go_start_time
                #print(advect_end_time_relative)
                #update plot
                #print("advec end",int(split_str[1]),advect_end_time_relative-advect_start_time_relative)
                #the second parameter is the width of the plot
                advect_spent_time=advect_end_time_relative-advect_start_time_relative
                width = (advect_spent_time)/go_time
                adv_accumulated_perproc=adv_accumulated_perproc+advect_spent_time
                
                if width<0:
                    print("advec error",advect_end_time_relative, advect_start_time_relative)
                # use start position
                barh_list_advec.append((offset+figsize_x*(advect_start_time_relative/go_time),width*figsize_x))
                barh_list_advec_raw.append((advect_start_time_relative+go_start_time,advect_start_time_relative,advect_end_time_relative))
            
            if update_result in line_strip:
                update_result_relative=int(split_str[1])-go_start_time
                update_spent_time=update_result_relative-advect_end_time_relative
                classify_accumulated_perproc=classify_accumulated_perproc+update_spent_time
                width = (update_spent_time)/go_time
                #use start position
                if width<0:
                    print("update_result error",update_result_relative, advect_end_time_relative)
                barh_list_update_result.append((offset+figsize_x*(advect_end_time_relative/go_time),width*figsize_x))


            if comm_start in line_strip:
                comm_start_time_relative=int(split_str[1])-go_start_time
            if comm_end in line_strip:
                comm_end_time_relative=int(split_str[1])-go_start_time
                #print("comm",comm_end_time_relative-comm_start_time_relative)
                comm_spent_time=comm_end_time_relative-comm_start_time_relative
                comm_accumulated_perproc=comm_accumulated_perproc+comm_spent_time
                width = (comm_spent_time)/go_time
                #use start position
                if width<0:
                    print("comm error",comm_end_time_relative, comm_start_time_relative)
                barh_list_comm.append((offset+figsize_x*(comm_start_time_relative/go_time),width*figsize_x))

            # send start/end
            if send_start in line_strip:
                send_start_time_relative=int(split_str[1])-go_start_time
            if send_end in line_strip:
                send_end_time_relative=int(split_str[1])-go_start_time
                send_spent_time=send_end_time_relative-send_start_time_relative
                sr_accumulated_perproc=sr_accumulated_perproc+send_spent_time
                width = (send_spent_time)/go_time
                #use start position
                if width<0:
                    print("send error",send_end_time_relative, send_start_time_relative)
                barh_list_actual_send.append((offset+figsize_x*(send_start_time_relative/go_time),width*figsize_x))

            # recv start/end
            if recv_start in line_strip:
                recv_start_time_relative=int(split_str[1])-go_start_time
            if recv_end in line_strip:
                recv_end_time_relative=int(split_str[1])-go_start_time
                recv_spent_time=recv_end_time_relative-recv_start_time_relative
                sr_accumulated_perproc=sr_accumulated_perproc+recv_spent_time
                width = (recv_spent_time)/go_time
                #use start position
                if width<0:
                    print("recv error",recv_end_time_relative, recv_start_time_relative)
                barh_list_actual_recv.append((offset+figsize_x*(recv_start_time_relative/go_time),width*figsize_x))

            if while_end in line_strip:
                while_end_time_relative = int(split_str[1])-go_start_time
                while_spent_time=while_end_time_relative-while_start_time_relative
                while_accumulate_perproc=while_accumulate_perproc+while_spent_time
                width = (while_spent_time)/go_time
                barh_list_while.append((offset+figsize_x*(while_start_time_relative/go_time),width*figsize_x))

                # terminated particles
                meta_spent_time=while_end_time_relative-comm_end_time_relative
                meta_accumulated_perproc=meta_accumulated_perproc+meta_spent_time
                width = (meta_spent_time)/go_time
                barh_list_update_terminated.append((offset+figsize_x*(comm_end_time_relative/go_time),width*figsize_x))

            #if rank==0:
            #    print(line_strip,"timediff",int(split_str[1])-go_start_time)
    
        fo.close()
        #if rank==0:
        #    print("barh_list_advec",barh_list_advec)
        #    print("barh_list_comm",barh_list_comm)

        #ax.broken_barh(xranges=barh_list_while,yrange=((i*figsize_y/procs,figsize_y/procs-0.1)),facecolors='tab:green', alpha=0.2)
        list_advec_all.append(barh_list_advec)
        list_comm_all.append(barh_list_comm)

        #put accumulated data into list
        #for each rank, store their results
        list_getp_accumulated.append(getp_accumulated_perproc)
        list_adv_accumulated.append(adv_accumulated_perproc)
        list_classify_accumulated.append(classify_accumulated_perproc)
        list_sr_accumulated.append(sr_accumulated_perproc)
        list_wait_accumulated.append(comm_accumulated_perproc-sr_accumulated_perproc)
        list_meta_accumulated.append(meta_accumulated_perproc) 
        list_while_accumulated.append(while_accumulate_perproc)

        print("rank", rank, "while loop number",len(barh_list_while))

        # draw the gant case
        if rank==0:
            # use label here
            
            ax.broken_barh(xranges=barh_list_init,yrange=(rank*bar_height,bar_height-0.1),facecolors='brown',label='Init')
            ax.broken_barh(xranges=barh_list_get_active_particles,yrange=(rank*bar_height,bar_height-0.1),facecolors='yellow',label='GetActiveParticles')
            ax.broken_barh(xranges=barh_list_advec,yrange=(rank*bar_height,bar_height-0.1),facecolors='tab:blue',label='Advec')
            ax.broken_barh(xranges=barh_list_update_result,yrange=(rank*bar_height,bar_height-0.1),facecolors='lightgrey',label='Classification')
            ax.broken_barh(xranges=barh_list_actual_send,yrange=(rank*bar_height,bar_height-0.1),facecolors='tab:green',label='Comm_Send')
            ax.broken_barh(xranges=barh_list_actual_recv,yrange=(rank*bar_height,bar_height-0.1),facecolors='tab:purple',label='Comm_Recv')
            # actual send recv will cover the pink part, so the pink part shown in the figure is the wait time
            ax.broken_barh(xranges=barh_list_comm,yrange=(rank*bar_height,bar_height-0.1),facecolors='tab:red',alpha=0.2,label='Comm_Wait')
            ax.broken_barh(xranges=barh_list_update_terminated,yrange=(rank*bar_height,bar_height-0.1),facecolors='orange',label='UpdateMetaData')
             
            #ax.broken_barh(xranges=barh_list_while,yrange=((rank*bar_height,bar_height-0.1)),facecolors='tab:green', alpha=0.1)

            #print("barh_list_advec",len(barh_list_advec), barh_list_advec)
            #print("barh_list_advec_raw",len(barh_list_advec_raw),barh_list_advec_raw)

            #print("barh_list_comm",barh_list_comm)
            #print("barh_list_actual_send",barh_list_actual_send)
            #print("barh_list_actual_recv",barh_list_actual_recv)            
        else:
            # no label here
            ax.broken_barh(xranges=barh_list_init,yrange=(rank*bar_height,bar_height-0.1),facecolors='brown')
            ax.broken_barh(xranges=barh_list_advec,yrange=(rank*bar_height,bar_height-0.1),facecolors='tab:blue')
            ax.broken_barh(xranges=barh_list_comm,yrange=(rank*bar_height,bar_height-0.1),facecolors='tab:red',alpha=0.2)
            ax.broken_barh(xranges=barh_list_actual_send,yrange=(rank*bar_height,bar_height-0.1),facecolors='tab:green')
            ax.broken_barh(xranges=barh_list_actual_recv,yrange=(rank*bar_height,bar_height-0.1),facecolors='tab:purple')
            ax.broken_barh(xranges=barh_list_get_active_particles,yrange=(rank*bar_height,bar_height-0.1),facecolors='yellow')
            ax.broken_barh(xranges=barh_list_update_result,yrange=(rank*bar_height,bar_height-0.1),facecolors='lightgrey')
            ax.broken_barh(xranges=barh_list_update_terminated,yrange=(rank*bar_height,bar_height-0.1),facecolors='orange')
            #ax.broken_barh(xranges=barh_list_while,yrange=((rank*bar_height,bar_height-0.1)),facecolors='tab:green', alpha=0.1)

    # get some space for legend in the center
    ax.broken_barh(xranges=[(0,1)],yrange=(procs*bar_height,bar_height),facecolors='None',edgecolor='None')
    plt.xlabel('Time(ms)', fontsize="large")
    plt.ylabel('Rank', fontsize="large")
    #advec_patch = mpatches.Patch(color='blue', label='Advec')
    #comm_patch = mpatches.Patch(color='red',alpha=0.2,label='Comm')
    #send_patch = mpatches.Patch(color='green',label='Comm_Send')
    #recv_patch = mpatches.Patch(color='purple'label='Comm_Recv')
    #other_patch = mpatches.Patch(color='white'label='Other')
    #ax.legend(handles=[advec_patch,comm_patch])
    #ax.legend(ncols=1,loc='upper right')
    ax.legend(ncols=4,loc='upper center')
    
    fig.savefig("gant.png",bbox_inches='tight')

    # draw the distribution figure for adv and comm
    advect_distribution(list_advec_all,go_time,figsize_x)
    comm_distribution(list_comm_all,go_time,figsize_x)

    #list_adv_accumulated.append(adv_accumulated_perproc)
    #list_classify_accumulated.append(classify_accumulated_perproc)
    #list_sr_accumulated.append(sr_accumulated_perproc)
    #list_wait_accumulated.append(comm_accumulated_perproc-sr_accumulated_perproc)
    #list_meta_accumulated.append(meta_accumulated_perproc) 
    # draw the accumulated time

    # try to do the sanity check to make sure the total sum match with measured data
    print(list_getp_accumulated)
    print("getp avg",statistics.mean(list_getp_accumulated),"getp stdev",statistics.stdev(list_getp_accumulated))

    print(list_adv_accumulated)
    print("adv avg",statistics.mean(list_adv_accumulated),"adv stdev",statistics.stdev(list_adv_accumulated))

    print(list_classify_accumulated)
    print("classify avg",statistics.mean(list_classify_accumulated),"classify stdev",statistics.stdev(list_classify_accumulated))

    print(list_sr_accumulated)
    print("sr avg",statistics.mean(list_sr_accumulated),"sr stdev",statistics.stdev(list_sr_accumulated))

    print(list_wait_accumulated)
    print("wait avg",statistics.mean(list_wait_accumulated),"wait stdev",statistics.stdev(list_wait_accumulated))

    print(list_meta_accumulated)
    print("meta avg",statistics.mean(list_meta_accumulated),"meta stdev",statistics.stdev(list_meta_accumulated))

    print("list_while_accumulated", list_while_accumulated)

    # draw the figure for target_rank
    for target_rank in range (0,procs,1):

        fig, ax = plt.subplots(figsize=(7,4.6))
        ax.set_xlabel('Time spent on key operations of rank ' + str(target_rank), fontsize='large')
        ax.set_ylabel('Time(ms)', fontsize='large')
        #ax.set_ylim([0,5000])
        ax.set_ylim([0,1500])


        N = 6
        ind = np.arange(N)    # the x locations for the groups
        width = 0.5       # the width of the bars
        ax.set_xticks(ind)
        ax.set_xticklabels(('GetParticles','Advec','Classify','Send/Recv','Wait',"Meta"), fontsize='large')
    
        barvalues=[list_getp_accumulated[target_rank],
        list_adv_accumulated[target_rank],
        list_classify_accumulated[target_rank],
        list_sr_accumulated[target_rank],
        list_wait_accumulated[target_rank],
        list_meta_accumulated[target_rank]
        ]

        ax.bar(ind, barvalues,  width, color="blue", capsize=3)
        filename = "rank_details_"+str(target_rank)
        fig.savefig(filename+".png",bbox_inches='tight')
        print("rank", target_rank, "barvalues",barvalues)