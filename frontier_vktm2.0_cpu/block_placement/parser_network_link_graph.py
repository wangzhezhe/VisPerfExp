import os
import sys
import math
import numpy as np
import graphviz

# compute the networking connectivity between all ranks
# parser counter.<rank>.out
def get_dst_rank_list(log_dir_path, rank):
    file_name = log_dir_path+"/counter."+str(rank)+".out"
    print("est file name",file_name)
    fo=open(file_name, "r")
    dest_rank_list_time=[]
    dest_rank_list_pnum=[]

    for line in fo:
        line_strip=line.strip()
        #print(line_strip)
        if "[" in line_strip:
            # sample input [9:82,6:3,]
            split_line = line_strip.split("[")[1]
            # remove last paragraph then getting dest info
            dest_info = split_line[:-1].split(",")
            #print(dest_info, len(dest_info))
            for dest_content in dest_info:
                if ":" in dest_content:
                    dest_rank_list_time.append(int(dest_content.split(":")[0]))
                    dest_rank_list_pnum.append(int(dest_content.split(":")[1]))

    return dest_rank_list_time,dest_rank_list_pnum


if __name__ == "__main__":

    if len(sys.argv)!=3:
        print("<binary> <log dir> <proc num>",flush=True)
        exit()
    
    log_dir_path=sys.argv[1]
    num_rank=int(sys.argv[2])

    # init an adjacent table, the size is rank*rank
    adjacent_matrix_num_comm = np.zeros((num_rank, num_rank))
    adjacent_matrix_num_particles = np.zeros((num_rank, num_rank))

    # go through each count log
    # return a list that show this rank send particle to which dest

    for src_rank in range(0,num_rank,1):
        dest_rank_list_time,dest_rank_list_pnum=get_dst_rank_list(log_dir_path, src_rank)
        #print(dest_rank_list)
        #go through dest list, update adjacent map
        for index, dest in enumerate(dest_rank_list_time):
            dest_rank=int(dest)
            adjacent_matrix_num_comm[src_rank][dest_rank]=adjacent_matrix_num_comm[src_rank][dest_rank]+1
            adjacent_matrix_num_particles[src_rank][dest_rank]=adjacent_matrix_num_particles[src_rank][dest_rank]+dest_rank_list_pnum[index]

    #np.set_printoptions(threshold=np.inf)
    #print(adjacent_matrix)


# draw adjacent table through the graphiviz
g = graphviz.Digraph('pv-networking',format='pdf')

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