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

# parse the timetrace log and draw the gantt chart
if __name__ == "__main__":
    
    if len(sys.argv)!=2:
        print("<binary> <dirpath>")
        exit()

    dirPath=sys.argv[1]

    dirname = dirPath.split("/")[-2]

    file_name = dirPath+"/timetrace.0.out"
    
    filter_start="FilterStart_"+str(0)+" "
    filter_end="FilterEnd_"+str(0)+" "
        
    filter_start_time=0
    filter_end_time=0

    fo=open(file_name, "r")

    for line in fo:
        line_strip=line.strip()
        split_str= line_strip.split(" ")
        if filter_start in line_strip:
            filter_start_time = float(split_str[1])       
        if filter_end in line_strip:
            filter_end_time = float(split_str[1])

    fo.close()

    filter_time = filter_end_time-filter_start_time
    print(dirname,filter_time)