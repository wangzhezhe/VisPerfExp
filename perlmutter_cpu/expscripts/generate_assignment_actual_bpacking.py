import os
import sys


def get_actual_run_info(file_name):
    print("actual data parse file name",file_name)
    fo=open(file_name, "r")
    actual_acc_advect_steps_popularity=[]

    for line in fo:
        line_strip=line.strip()
        #print(line_strip)
        if "actual_acc_advect_steps_popularity" in line_strip:
            start =line_strip.find("[")
            end=line_strip.find("]")
            extract_num = line_strip[start+1:end-1]
            split_line = extract_num.split(",")
            #print(split_line)
            actual_acc_advect_steps_popularity = [float(v) for v in split_line]


    fo.close()

    return actual_acc_advect_steps_popularity


if __name__ == "__main__":

    if len(sys.argv)!=4:
        print("<binary> <actual log parser file log> <block num> <proc num>",flush=True)
        exit()

    actual_parse_log = sys.argv[1]
    block_num=int(sys.argv[2])
    # the number of procs we want to put the bin into
    proc_num=int(sys.argv[3])
    
    print("actual_parse_log",actual_parse_log,"block_num",block_num,"proc_num",proc_num)


    # parse the workload estimation log
    # extract info from estimated data
    actual_acc_advect_steps_popularity=get_actual_run_info(actual_parse_log)
    print("actual_acc_advect_steps_popularity")
    print(actual_acc_advect_steps_popularity)
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

    adv_popularity_for_sorting = [] 

    for index, popularity in enumerate(actual_acc_advect_steps_popularity):
        adv_popularity_for_sorting.append([index,popularity])

    #print(adv_popularity_for_sorting)

    # sorting list according to the second popularity
    sorted_actual_adv_popularity=sorted(adv_popularity_for_sorting, key=lambda x: x[1], reverse=True)

    print("sorted_actual_adv_popularity:", sorted_actual_adv_popularity)


    for bin_info in sorted_actual_adv_popularity:
        bin_popularity = bin_info[1]
        block_id = bin_info[0]
        #find a bin for current block_id
        #go through all bin_remaining_space_list, find one that can hold current bin
        find_bin=False
        for bin_index, bin_remaining in enumerate(bin_remaining_space_list):
            # when we looking at the new bin, the package size 
            # is larger than bin size, we just put packge in that bin
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