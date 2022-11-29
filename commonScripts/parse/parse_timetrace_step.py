
from os import system
from os.path import exists
import sys
import matplotlib
import matplotlib.pyplot as plt





if __name__ == "__main__":
    
    if len(sys.argv)!=3:
        print("<binary> <filename> <step>")
        exit()

    file_name = sys.argv[1]
    step=int(sys.argv[2])

    fo=open(file_name, "r")
    
    adevct_start="AdvectStart_"+str(step)+" "
    adevct_end="AdvectEnd_"+str(step)+" "

    comm_start="CommStart_"+str(step)+" "
    comm_end="CommEnd_"+str(step)+" "

    go_start = "GoStart_"+str(step)+" "
    go_end = "GoEnd_"+str(step)+" "

    # compute the total time and use this to compute the bar length
    # there is variance for multiprocess case 
    offset=0
    for line in fo:
        line_strip=line.strip()
        split_str= line_strip.split(" ")
        if go_start in line_strip:
            go_start_time = int(split_str[1])       
        if go_end in line_strip:
            go_end_time = int(split_str[1])

    fo.close() 
    
    go_time = (go_end_time - go_start_time)
    print("total time ",go_time)

    while_start = "WhileStart_" +str(step)+" "
    while_end = "WhileEnd_" +str(step)+" "

    advect_start_time_relative=0
    advect_end_time_relative=0
    comm_start_time_relative=0
    comm_end_time_relative=0
    while_start_time_relative=0
    
    # all the width should be proportional to this figsize_x
    # when we use the micro second, some iteration happens quickly and 
    # the start time is the same with the end time
    # the granularity is 1ms, if the two timer is less than 1ms, we could not draw it
    figsize_x = 16
    fig, ax = plt.subplots(1, figsize=(figsize_x,2))
    plt.xticks([0,8,16], [0,go_time/2, go_time])

    barh_list_advec=[]
    barh_list_comm=[]
    barh_list_while=[]

    # read file again
    fo=open(file_name, "r")
    for line in fo:
        line_strip=line.strip()
        split_str= line_strip.split(" ")

        if while_start in line_strip:
            while_start_time_relative = int(split_str[1])-go_start_time

        if while_end in line_strip:
            while_end_time_relative = int(split_str[1])-go_start_time
            width = (while_end_time_relative-while_start_time_relative)/go_time
            barh_list_while.append((figsize_x*(while_start_time_relative/go_time),width*figsize_x))

        if adevct_start in line_strip:
            advect_start_time_relative=int(split_str[1])-go_start_time
            #print(advect_start_time_relative)
        if adevct_end in line_strip:
            advect_end_time_relative=int(split_str[1])-go_start_time
            #print(advect_end_time_relative)
            #update plot
            #print("advec",advect_end_time_relative-advect_start_time_relative)
            #the second parameter is the width of the plot
            width = (advect_end_time_relative-advect_start_time_relative)/go_time
            if width<0:
                print("advec error",advect_end_time_relative, advect_start_time_relative)
            # use start position
            barh_list_advec.append((figsize_x*(advect_start_time_relative/go_time),width*figsize_x))

        if comm_start in line_strip:
            comm_start_time_relative=int(split_str[1])-go_start_time
        if comm_end in line_strip:
            comm_end_time_relative=int(split_str[1])-go_start_time
            #print("comm",comm_end_time_relative-comm_start_time_relative)
            width = (comm_end_time_relative-comm_start_time_relative)/go_time
            #use start position
            if width<0:
                print("comm error",comm_end_time_relative, comm_start_time_relative)
            barh_list_comm.append((figsize_x*(comm_start_time_relative/go_time),width*figsize_x))

    
    fo.close()
    #print(barh_list_advec)

    ax.broken_barh(xranges=barh_list_advec,yrange=(0,1),facecolors='tab:blue')
    ax.broken_barh(xranges=barh_list_comm,yrange=(0,1),facecolors='tab:red')
    #ax.broken_barh(xranges=barh_list_while,yrange=(0,1),facecolors='tab:green', alpha=0.2)

    plt.savefig("gant.png",bbox_inches='tight')