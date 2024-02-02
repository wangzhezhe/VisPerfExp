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


def get_estimated_info(slname, dataset_name,num_rank, dirPath, num_test_points, nxyz, pc):
    file_name = dirPath+"/"+slname+"_estimate_"+dataset_name+"_r"+str(num_rank)+ "_tp" + str(num_test_points)+ "_nxyz"+str(nxyz)+"_pc" + pc+ ".log"
    print("est file name",file_name)
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

def draw_three_lines(actual_data, s1_estimated_data,s2_estimated_data, actual_title, s1_estimated_title,s2_estimated_title,figure_name):

    fig, ax = plt.subplots(figsize=(9,4.5))
    p1 = ax.plot(actual_data, color=gblue, marker='^', label=actual_title)
    p2 = ax.plot(s1_estimated_data, '--', color=gred, marker='o', label=s1_estimated_title)
    p3 = ax.plot(s2_estimated_data, '-', color=ggreen, marker='x', label=s2_estimated_title)

    ylimit1 = max(actual_data)
    ylimit2 = max(s1_estimated_data)
    ylimit3 = max(s2_estimated_data)

    ylimit = max(max(ylimit1,ylimit2),ylimit3)
    ax.set_ylim([0,1.2*ylimit])
    ax.legend(ncol=2, loc='upper left', fontsize='large')
    plt.savefig(figure_name+".png", bbox_inches='tight')

if __name__ == "__main__":
    if len(sys.argv)!=8:
        print("<binary> <dataset name> <runDirPath> <estimate dir path> <num_rank> <num_test_points> <nxyz> <pc>",flush=True)
        exit()
    dataset_name=sys.argv[1]
    dirPath=sys.argv[2]
    estPath=sys.argv[3]
    num_rank=int(sys.argv[4])
    num_test_points=int(sys.argv[5])
    nxyz=int(sys.argv[6])
    pc=str(sys.argv[7])

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
    sl1_estimated_adv_popularity,sl1_estimated_in_particles,sl1_estimated_out_particles=get_estimated_info("sl1",dataset_name,num_rank,estPath,num_test_points,nxyz,pc)
    print("sl1_estimated_adv_popularity")
    print(sl1_estimated_adv_popularity)
    print("sl1_estimated_in_particles")
    print(sl1_estimated_in_particles)
    print("sl1_estimated_out_particles")
    print(sl1_estimated_out_particles)


    sl2_estimated_adv_popularity,sl2_estimated_in_particles,sl2_estimated_out_particles=get_estimated_info("sl2",dataset_name,num_rank,estPath,num_test_points,nxyz,pc)
    print("sl2_estimated_adv_popularity")
    print(sl2_estimated_adv_popularity)
    print("sl2_estimated_in_particles")
    print(sl2_estimated_in_particles)
    print("sl2_estimated_out_particles")
    print(sl2_estimated_out_particles)



    suffix="_tp" + str(num_test_points)+ "_nxyz"+str(nxyz)+"_pc" + pc

    # draw it, from rank 0 to rank n-1
    # steps
    fig_name=dataset_name+"_rank"+str(num_rank)+suffix+"_advsteps"
    draw_three_lines(actual_acc_advect_steps_popularity,sl1_estimated_adv_popularity, sl2_estimated_adv_popularity, "actual popularity","sl1 estimated popularity","sl2 estimated popularity",fig_name)

    #particle in
    fig_name=dataset_name+"_rank"+str(num_rank)+suffix+"_particle_in"
    draw_three_lines(actual_acc_in_particles_num,sl1_estimated_in_particles,sl2_estimated_in_particles,"actual received particle","sl1 estimated received particle","sl2 estimated received particle",fig_name)


    #particle out
    fig_name=dataset_name+"_rank"+str(num_rank)+suffix+"_particle_out"
    draw_three_lines(actual_acc_out_particles_num,sl1_estimated_out_particles,sl2_estimated_out_particles,"actual send particle","sl1 estimated send particle","sl2 estimated send particle",fig_name)
