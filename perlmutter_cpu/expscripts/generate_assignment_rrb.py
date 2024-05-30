import os
import sys

if __name__ == "__main__":

    if len(sys.argv)!=3:
        print("<binary> <blocks num> <proc num>",flush=True)
        exit()

    data_blocks = int(sys.argv[1])
    proc_num=int(sys.argv[2])
    proc_block_list=[]
    for proc in range(0,proc_num,1):
        proc_block_list.append([])


    # for each block, decide it is in which proc
    for block_id in range(0,data_blocks,1):
        proc_id = block_id%proc_num
        proc_block_list[proc_id].append(block_id)

    print(proc_block_list)

    outputfile = "assign_options.config"
    with open(outputfile, 'w') as f:
        for block_list in proc_block_list:
            # for each block
            index = 0
            for block in block_list:
                if index>0:
                    f.write(" "+str(block))
                else:
                    f.write(str(block))
                index+=1
            f.write('\n')