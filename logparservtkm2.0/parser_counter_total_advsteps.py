from os import system
from os.path import exists
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import ticker
import statistics
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# parse the counter file
# x axis represents the rank value
# y axis represents the total advected steps executed by this rank
if __name__ == "__main__":
    
    if len(sys.argv)!=3:
        print("<binary> <procs> <dirpath>")
        exit()

    procs=int(sys.argv[1])
    dirPath=sys.argv[2]

    simSycle=0

    total_advec_steps=[0]*procs
    for rank in range(0,procs,1):
        file_name = dirPath+"/counter."+str(rank)+".out"
        fo=open(file_name, "r")

        # go through all log entries
        for line in fo:
            line_strip=line.strip()
            split_str= line_strip.split(",")
            # the first sim sycle
            if split_str[0]=='0':
                #print(split_str)
                total_advec_steps[rank]=total_advec_steps[rank]+int(split_str[2])
        fo.close()

    print(total_advec_steps)

    fig, ax = plt.subplots()

    ind = np.arange(procs)

    #ax.set_xticks([0,2,4,6])
    #ax.set_xticklabels(['zero','two','four','six'])

    ax.set_xlabel('Index of rank', fontsize='large')
    ax.set_ylabel('Number of total advected steps', fontsize='large')   
    p = ax.bar(ind,total_advec_steps,color='blue',alpha=0.8)
    fig.savefig("counter_total_advsteps.png",bbox_inches='tight')

