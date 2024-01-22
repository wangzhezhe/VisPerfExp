import numpy as np
import time
import shutil
import os
import sys
import matplotlib.pyplot as plt
# draw the line for estimated value and actual values
# compute the particle in and particle out, draw the line
# using the data in algorithmRecorder.rank to get these information

gblue = '#4486F4'
gred = '#DA483B'
gyellow = '#FFC718'
ggreen = '#1CA45C'

def get_aectual_acc_advect_steps(dataset_name, num_rank, dirPath):
    acc_adv_step_list=[]
    for rank in range(0,num_rank):
        total_adv_steps=0        
        file_name = dirPath+"/actual_"+dataset_name+"_"+str(num_rank)+"/timetrace."+str(rank)+".out"
        fo=open(file_name, "r")
        for line in fo:
            line_strip=line.strip()
            if "ParticleAdvectInfo" not in line_strip:
                continue
            adv_steps= int(line_strip.split(" ")[0].split("_")[2])

            total_adv_steps=total_adv_steps+adv_steps
        acc_adv_step_list.append(total_adv_steps)
        fo.close()
    return acc_adv_step_list


def get_aectual_acc_in_out_particles_num(dataset_name, num_rank, dirPath):
    acc_in_particles_num_list=[]
    acc_out_particles_num_list=[]

    for rank in range(0,num_rank):
        total_adv_steps=0        
        file_name = dirPath+"/actual_"+dataset_name+"_"+str(num_rank)+"/algorithmRecorder."+str(rank)+".out"
        fo=open(file_name, "r")
        # for each rank
        acc_num_send_particles=0
        acc_num_recv_particles=0
        for line in fo:
            line_strip=line.strip()
            if "SEND_PARTICLES_rank_np" in line_strip:
                # parse the rank np out, such as: 178733,SEND_PARTICLES_rank_np, 3,1,2,161,1,1200,4,3630
                split_str = line_strip.split(",")
                if(len(split_str)%2!=0):
                    print("Error, the log length is wrong", split_str)
                for index in range(2,len(split_str),2):
                    #print("len(split_str) is",len(split_str),"index is", index)
                    num_send_particles=int(split_str[index+1])
                    acc_num_send_particles=acc_num_send_particles+num_send_particles


            if "RECEIVE_PARTICLES_rank_np" in line_strip:
                # parse the rank np in, recieving particles. such as: 716505,RECEIVE_PARTICLES_rank_np, 3,10,0,581,0,29,5,626
                split_str = line_strip.split(",")
                if(len(split_str)%2!=0):
                    print("Error, the log length is wrong", split_str)
                for index in range(2,len(split_str),2):
                    #print("len(split_str) is",len(split_str),"index is", index)
                    num_recv_particles=int(split_str[index+1])
                    acc_num_recv_particles=acc_num_recv_particles+num_recv_particles

        #put data into the list
        acc_out_particles_num_list.append(acc_num_send_particles)
        acc_in_particles_num_list.append(acc_num_recv_particles)

        fo.close()
    
    return acc_in_particles_num_list,acc_out_particles_num_list


def get_estimated_info(dataset_name,num_rank, dirPath, num_test_points):
    file_name = dirPath+"/estimate_"+dataset_name+"_r"+str(num_rank)+ "_tp" + str(num_test_points) + ".log"
    fo=open(file_name, "r")
    estimator_steps_popularity_list=[]
    estimator_particle_in_list=[]
    estimator_particle_out_list=[]

    for line in fo:
        line_strip=line.strip()
        #print(line_strip)
        if "NormBlockPopularity" in line_strip:
            start =line_strip.find("[")
            end=line_strip.find("]")
            extract_num = line_strip[start+1:end-1]
            split_line = extract_num.split(",")
            #print(split_line)
            estimator_steps_popularity_list = [float(v) for v in split_line]

        if "ParticlesIn" in line_strip:
            start =line_strip.find("[")
            end=line_strip.find("]")
            extract_num = line_strip[start+1:end-1]
            split_line = extract_num.split(",")
            #print(split_line)
            estimator_particle_in_list = [float(v) for v in split_line]

        if "ParticlesOut" in line_strip:
            start =line_strip.find("[")
            end=line_strip.find("]")
            extract_num = line_strip[start+1:end-1]
            split_line = extract_num.split(",")
            #print(split_line)
            estimator_particle_out_list = [float(v) for v in split_line]

    fo.close()

    if len(estimator_steps_popularity_list)==0:
        print("No NormBlockPopularity log")
        exit(0)

    return estimator_steps_popularity_list,estimator_particle_in_list,estimator_particle_out_list

def draw_two_lines(actual_data, estimated_data, actual_title, estimated_title,figure_name):

    fig, ax = plt.subplots(figsize=(9,4.5))
    p1 = ax.plot(actual_data, color=gblue, marker='^', label=actual_title)
    p2 = ax.plot(estimated_data, '--', color=gred, marker='o', label=estimated_title)
    ax.legend(ncol=2, loc='upper left', fontsize='large')
    plt.savefig(figure_name+".png", bbox_inches='tight')

if __name__ == "__main__":
    if len(sys.argv)!=5:
        print("<binary> <dataset name> <runDirPath> <num_rank> <num_test_points>",flush=True)
        exit()
    dataset_name=sys.argv[1]
    dirPath=sys.argv[2]
    num_rank=int(sys.argv[3])
    num_test_points=int(sys.argv[4])

    # extract info from actual data
    actual_acc_advect_steps=get_aectual_acc_advect_steps(dataset_name,num_rank,dirPath)
    actual_acc_in_particles_num, actual_acc_out_particles_num=get_aectual_acc_in_out_particles_num(dataset_name,num_rank,dirPath)
    print("actual_acc_advect_steps")
    print(actual_acc_advect_steps)

    adv_all_steps = sum(actual_acc_advect_steps)
    #acc_adv_step_list_norm = [float(i)/adv_all_steps for i in acc_adv_step_list]
    actual_acc_advect_steps_popularity = [float(v)/adv_all_steps for v in actual_acc_advect_steps]

    print("actual_acc_adv_steps_popularity")
    print(actual_acc_advect_steps_popularity)
    print("actual_acc_in_particles_num")
    print(actual_acc_in_particles_num)
    print("actual_acc_out_particles_num")
    print(actual_acc_out_particles_num)

    # print out rank that are larger than a threshold
    threshold=0.05
    rank=0
    for v in actual_acc_advect_steps_popularity:
        if v>threshold:
            print("overloaded id is ", rank)
        rank+=1

    # extract info from estimated data
    estimated_adv_popularity,estimated_in_particles,estimated_out_particles=get_estimated_info(dataset_name,num_rank,dirPath,num_test_points)
    print("estimated_adv_popularity")
    print(estimated_adv_popularity)
    print("estimated_in_particles")
    print(estimated_in_particles)
    print("estimated_out_particles")
    print(estimated_out_particles)

    # draw it, from rank 0 to rank n-1
    # steps
    fig_name=dataset_name+"_rank"+str(num_rank)+"_tp"+str(num_test_points)+"_advsteps"
    draw_two_lines(actual_acc_advect_steps_popularity,estimated_adv_popularity,"actual popularity","estimated popularity",fig_name)

    #particle in
    fig_name=dataset_name+"_rank"+str(num_rank)+"_tp"+str(num_test_points)+"_particle_in"
    draw_two_lines(actual_acc_in_particles_num,estimated_in_particles,"actual received particle","estimated received particle",fig_name)


    #particle out
    fig_name=dataset_name+"_rank"+str(num_rank)+"_tp"+str(num_test_points)+"_particle_out"
    draw_two_lines(actual_acc_out_particles_num,estimated_out_particles,"actual send particle","estimated send particle",fig_name)
