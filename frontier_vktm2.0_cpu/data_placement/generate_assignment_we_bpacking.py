import os
import sys


def get_estimated_info(file_name):
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


if __name__ == "__main__":

    if len(sys.argv)!=4:
        print("<binary> <workload estimation log> <block num> <proc num>",flush=True)
        exit()

    workload_estimation_log = sys.argv[1]
    block_num=int(sys.argv[2])
    # the number of procs we want to put the bin into
    proc_num=int(sys.argv[3])
    
    print("workload_estimation_log",workload_estimation_log,"block_num",block_num,"proc_num",proc_num)


    # parse the workload estimation log
    # extract info from estimated data
    estimated_adv_popularity,estimated_in_particles,estimated_out_particles=get_estimated_info(workload_estimation_log)
    print("estimated_adv_popularity")
    print(estimated_adv_popularity)
    # print("estimated_in_particles")
    # print(estimated_in_particles)
    # print("estimated_out_particles")
    # print(estimated_out_particles)

    # using this information to decide the data placement strategy
    # first fit strategy
    # it attempts to place each new item into the first bin in which it fits.
    # for each new loaded data block

    # init the bin size
    bin_remaining_space_list=[]
    block_list_for_proc=[]
    avg_bin_size = 1.0/(1.0*proc_num)
    
    # init the bin_remaining_space_list
    for i in range(0,proc_num,1):
        bin_remaining_space_list.append(avg_bin_size)
        block_list_for_proc.append([])
    
    print ("init status bin_remaining_space_list", bin_remaining_space_list, "block_list_for_proc", block_list_for_proc)

    # sorting the list, using the first-fit decreasing
    # if the largest popularity is larger than the average bin size
    # just mark assign a separate bin for that block
    # sort the estimated_adv_popularity with the block id

    estimated_adv_popularity_for_sorting = [] 

    for index, popularity in enumerate(estimated_adv_popularity):
        estimated_adv_popularity_for_sorting.append([index,popularity])

    #print(estimated_adv_popularity_for_sorting)

    # sorting list according to the second popularity
    sorted_estimated_adv_popularity=sorted(estimated_adv_popularity_for_sorting, key=lambda x: x[1], reverse=True)

    print("sorted_estimated_adv_popularity:", sorted_estimated_adv_popularity)


    for bin_info in sorted_estimated_adv_popularity:
        bin_popularity = bin_info[1]
        block_id = bin_info[0]
        #find a bin for current block_id
        #go through all bin_remaining_space_list, find one that can hold current bin
        find_bin=False
        for bin_index, bin_remaining in enumerate(bin_remaining_space_list):
            # if looking at the new bin, it means that the package size 
            # is larger than bin size
            if (bin_remaining<bin_popularity):
                if (abs(bin_remaining-avg_bin_size)<0.0000001):
                    block_list_for_proc[bin_index].append(block_id)
                    # update space
                    bin_remaining_space_list[bin_index]-=bin_popularity
                    find_bin=True
                    break    
            
            # if there is enough space
            if bin_remaining>=bin_popularity:
                # put block into associated bins
                block_list_for_proc[bin_index].append(block_id)
                # update space
                bin_remaining_space_list[bin_index]-=bin_popularity
                find_bin=True
                break
        if find_bin==False:
            print("error failed to find bin for bin_popularity",bin_popularity,"curr bin_remaining",bin_remaining)
        
    print("block_list_for_proc",block_list_for_proc)

    outputfile = "assign_options.config"
    with open(outputfile, 'w') as f:
        for block_list in block_list_for_proc:
            # for each block
            index = 0
            for block in block_list:
                if index>0:
                    f.write(" "+str(block))
                else:
                    f.write(str(block))
                index+=1
            f.write('\n')