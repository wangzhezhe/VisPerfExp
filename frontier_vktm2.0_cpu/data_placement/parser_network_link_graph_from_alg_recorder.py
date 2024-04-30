import os
import sys
import math
import numpy as np
import graphviz

# compute the networking connectivity between all ranks
# parser algorithmRecorder.<rank>.out
def get_dst_rank_list(log_dir_path, rank, start_time, end_time):
    file_name = log_dir_path+"/algorithmRecorder."+str(rank)+".out"
    print("est file name",file_name)
    fo=open(file_name, "r")
    dest_rank_list=[]
    dest_rank_list_pnum=[]

    for line in fo:
        line_strip=line.strip()
        #print(line_strip)
        if "SEND_PARTICLES_rank_np" in line_strip:
            # sample input [9:82,6:3,]
            split_info = line_strip.split(",")
            #print(split_info)
            #print(float(split_info[2]))
            send_time = float(split_info[0])
            # not at the start end time slot
            if(send_time<start_time or send_time>end_time):
                continue
            num_dest = int((len(split_info) - 2)/2)
            #print("num_dest",num_dest)
            for i in range(0,num_dest,1):
                dest_rank_list.append(int(split_info[2+i*2]))
                dest_rank_list_pnum.append(int(split_info[2+i*2+1]))

    return dest_rank_list,dest_rank_list_pnum


if __name__ == "__main__":

    if len(sys.argv)!=5:
        print("<binary> <log dir> <proc num> <start time> <end time>",flush=True)
        exit()
    
    # How to detct different stages?
    log_dir_path=sys.argv[1]
    num_rank=int(sys.argv[2])
    start_time=int(sys.argv[3])
    end_time=int(sys.argv[4])

    # init an adjacent table, the size is rank*rank
    adjacent_matrix_num_comm = np.zeros((num_rank, num_rank))
    adjacent_matrix_num_particles = np.zeros((num_rank, num_rank))

    # go through each count log
    # return a list that show this rank send particle to which dest

    for src_rank in range(0,num_rank,1):
        dest_rank_list_time,dest_rank_list_pnum=get_dst_rank_list(log_dir_path, src_rank, start_time, end_time)
        #print(dest_rank_list_time,dest_rank_list_pnum)
        #go through dest list, update adjacent map
        for index, dest in enumerate(dest_rank_list_time):
            dest_rank=int(dest)
            adjacent_matrix_num_comm[src_rank][dest_rank]=adjacent_matrix_num_comm[src_rank][dest_rank]+1
            adjacent_matrix_num_particles[src_rank][dest_rank]=adjacent_matrix_num_particles[src_rank][dest_rank]+dest_rank_list_pnum[index]

    #np.set_printoptions(threshold=np.inf)
    #print(adjacent_matrix)


# draw adjacent table through the graphiviz
g = graphviz.Digraph('pv-networking-start-'+str(start_time)+"-end"+str(end_time),format='pdf')

# adding node (make sure all nodes exist before adding edges)
for src_rank in range(0,num_rank,1):
    g.node(str(src_rank))
    
# adding edge
for src_rank in range(0,num_rank,1):
    for dst_rank in range(0,num_rank,1):
        if(adjacent_matrix_num_comm[src_rank][dst_rank]>0):
            label_str = str(int(adjacent_matrix_num_comm[src_rank][dst_rank])) + "(" + str(int(adjacent_matrix_num_particles[src_rank][dst_rank])) +")"
            g.edge(str(src_rank), str(dst_rank), label=label_str)

g.render(directory='pv-networking')