
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.colors

import matplotlib.pyplot as plt
from itertools import cycle
import numpy as np
import json
from matplotlib.ticker import PercentFormatter
from matplotlib.patches import Patch
import matplotlib

from math import log
import math

from mpl_toolkits.axes_grid1 import make_axes_locatable

gblue = '#4486F4'
gred = '#DA483B'
gyellow = '#FFC718'
ggreen = '#1CA45C'

def render_datasize_procnum():

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.set_xlabel('Number of processes', fontsize='medium')
    ax.set_ylabel('Mesh size', fontsize='medium')
    ax.set_zlabel('Rendering time (ms)', fontsize='medium')  

    # set tick
    N = 4
    ind = np.array([1,2,4,8])/8.0   # the x locations 
    width = 1.0       # the width of the bars
    ax.set_xticks(ind*width)
    ax.set_xticklabels(('16','32','64','128'), fontsize=8)
    
    ax.set_ylim([0,8])
    offset=0
    ax.set_yticks([offset+1,offset+2,offset+4,offset+8])
    ax.set_yticklabels(('64^3','128^3','256^3','512^3'), fontsize=8)

    #ax.set_zlim([0,100])

    X=[ind*width,ind*width,ind*width,ind*width]
    Y=[[1,1,1,1],[2,2,2,2],[4,4,4,4],[8,8,8,8]]
    Z= np.array(
        [
        [2155.19,1458.29,1113.61,1009.52],
        [2349.14,1604.54,1179.75,1044.22],
        [3015.46,1879,1315.08,1127.65],
        [4171.36,2466.64,1596.26,1294.83]
        ])


    ax.plot_surface(X, Y, Z, cmap='viridis',edgecolor='none')
    #ax.plot_wireframe(X, Y, Z)

    plt.savefig("render_datasize_procnum.pdf",bbox_inches='tight', pad_inches=0.2)
    plt.savefig("render_datasize_procnum.png",bbox_inches='tight', pad_inches=0.2)   

def contour_datasize_procnum():

    #fig,ax = plt.subplots(figsize=(10,6),projection='3d')

    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')


    #ax = plt.axes(projection='3d')

    ax.set_xlabel('Number of processes', fontsize='medium')
    ax.set_ylabel('Mesh size', fontsize='medium')
    ax.set_zlabel('Contour filter execution time(ms)', fontsize='medium')  

    # set tick
    N = 4
    ind = np.array([1,2,4,8])/8.0   # the x locations 
    width = 1.0       # the width of the bars
    ax.set_xticks(ind*width)
    ax.set_xticklabels(('16','32','64','128'), fontsize=8)
    
    ax.set_ylim([0,8])
    offset=0
    ax.set_yticks([offset+1,offset+2,offset+4,offset+8])
    ax.set_yticklabels(('64^3','128^3','256^3','512^3'), fontsize=8)

    #ax.set_zlim([0,100])

    X=[ind*width,ind*width,ind*width,ind*width]
    Y=[[1,1,1,1],[2,2,2,2],[4,4,4,4],[8,8,8,8]]
    Z= np.array(
        [
        [761.184,450.164,240.407,160.095],
        [2036.86,1522.03,1267.6,673.296],
        [4210.18,3375.15,2949.53,1767.29],
        [21096.6,14616.5,11368.3,6599.18]
        ])


    ax.plot_surface(X, Y, Z, cmap='viridis',edgecolor='none')
    #ax.plot_wireframe(X, Y, Z)

    plt.savefig("contour_datasize_procnum.pdf",bbox_inches='tight', pad_inches=0.2)
    plt.savefig("contour_datasize_procnum.png",bbox_inches='tight', pad_inches=0.2)  

def streamline_datasize_procnum():
    # use the bar graph for this data
    # since there are no obvious distribution with the change of datasize

    fig,ax = plt.subplots(figsize=(8,4.5))
    bar_width=0.2
    
    ax.set_xticks([0.3,1.3,2.3,3.3,4.3])
    ax.set_xticklabels(('8','16','32','64','128'), fontsize=16)

    courses = np.arange(5)

    mesh_64_avg=[37.4608, 29.48256667,24.37223333,25.41123333,29.61726667]
    mesh_64_err=[1.798553744, 1.252455645,0.5369464995,1.570458444,0.9282260842]
    plt.bar(courses, mesh_64_avg, bar_width, color=gblue, yerr=mesh_64_err,ecolor='gray', capsize=3, label="64^3")
 
    mesh_128_avg=[36.63203333, 31.9496,24.6621,24.746,29.42026667]
    mesh_128_err=[0.313244702, 4.196328246,0.9307683493,1.017355061,0.8271436232]
    plt.bar(0.2+courses, mesh_128_avg, bar_width, color=gred, yerr=mesh_128_err,ecolor='gray', capsize=3, label="128^3")
 
    mesh_256_avg=[37.21386667, 32.6669,24.9342,31.07486667,30.8179]
    mesh_256_err=[0.3922259085, 4.57857049,0.4634800104,7.800728934,5.041808189]
    plt.bar(0.4+courses, mesh_256_avg, bar_width, color=gyellow, yerr=mesh_256_err,ecolor='gray', capsize=3, label="256^3")
 
    mesh_512_avg=[36.83, 29.54926667,24.47383333,25.69256667,31.67156667]
    mesh_512_err=[0.451447317, 0.08260976536,0.2165146723,1.399950215,3.55849329]
    plt.bar(0.6+courses, mesh_512_avg, bar_width, color=ggreen, yerr=mesh_512_err,ecolor='gray', capsize=3, label="512^3")
 
    plt.ylim([0, 46])
    
    plt.xlabel("Number of processes", fontsize=16)
    plt.ylabel("Particle advection execution time (ms)",fontsize=16)

    legend = ax.legend(loc='upper center', ncol=4, fontsize=14)

    plt.savefig("streamline_datasize_procnum.pdf",bbox_inches='tight')
    plt.savefig("streamline_datasize_procnum.png",bbox_inches='tight')  


def render_datacontents():
    fig, ax = plt.subplots(figsize=(8,4.6))
    ax.set_xlabel('Simulation computation step', fontsize=16)
    ax.set_ylabel('Rendering filter execution time (ms)', fontsize=12)  

    # set tick
    offset = 0 
    dist = 5.65
    xindex=[]
    for i in range (0,4):
        xindex.append(offset+i*dist)
    ax.set_xticks(xindex)

    ax.set_xticklabels(('2','6','12','18'), fontsize='large')
    
    p_16=(2463.21,2467.43,2450.22,2349.14,2376.88,2393.18,2389.53,2474.12,2448.68,2448.21,2407.66,2402.26,2478.07,2478.7,2476.81,2475.41,2476.99,2479.36)
    pal=ax.plot(p_16, color=gblue, linestyle='-', label="16 procs")
    
    p_32=(1618.99,1615.06,1614.96,1604.54,1593.6,1593.3,1582.49,1621.62,1604.81,1606.43,1582.45,1585.4,1626.04,1623.19,1643.18,1626.58,1625.99,1621.69)
    pal=ax.plot(p_32, color=gred, linestyle='-', label="32 procs")

    p_64=(1179.64,1177.33,1176.45,1179.75,1175.18,1179.46,1176.91,1182.95,1181.24,1180.87,1181.3,1187.87,1179.88,1190.05,1183.31,1181.92,1183.82,1186.18)
    pal=ax.plot(p_64, color=gyellow, linestyle='-', label="64 procs")

    p_128=(1042.74,1041.19,1042.97,1044.22,1041.46,1042.62,1041.86,1047.05,1042.48,1046.47,1045.63,1044.44,1041,1044.32,1058.61,1047.05,1044.78,1042.98)
    pal=ax.plot(p_128, color=ggreen, linestyle='-', label="128 procs")

    plt.savefig("render_datacontents.pdf",bbox_inches='tight')
    plt.savefig("render_datacontents.png",bbox_inches='tight')

def contour_datacontents():
    fig, ax = plt.subplots(figsize=(8,4.6))
    ax.set_xlabel('Simulation computation step', fontsize=16)
    ax.set_ylabel('Contour filter execution time (ms)', fontsize=12)  

    # set tick
    offset = 0 
    dist = 5.65
    xindex=[]
    for i in range (0,4):
        xindex.append(offset+i*dist)
    ax.set_xticks(xindex)

    ax.set_xticklabels(('2','6','12','18'), fontsize='large')
    
    p_16=(250.127,547.984,667.236,761.184,586.775,621.489,738.254,355.571,523.767,419.226,291.705,175.412,233.96,140.79,128.895,167.456,248.441,239.576,280.316)
    pal=ax.plot(p_16, color=gblue, linestyle='-', label="16 procs")
    
    p_32=(211.911,403.79,431.199,450.164,336.369,349.401,394.494,239.869,293.649,233.5,175.456,126.385,141.21,116.01,111,128.153,190.141,202.859,219.753)
    pal=ax.plot(p_32, color=gred, linestyle='-', label="32 procs")

    p_64=(193.307,307.266,263.337,240.407,197.116,203.548,218.959,156.974,173.946,173.906,122.557,101.519,122.025,104.807,101.496,117.866,176.489,177.001,172.949)
    pal=ax.plot(p_64, color=gyellow, linestyle='-', label="64 procs")

    p_128=(126.59,184.6,179.067,160.095,118.657,119.349,126.363,88.5581,116.026,113.67,118.209,67.2233,70.6061,67.8448,61.1904,66.8354,113.151,103.821,106.2)
    pal=ax.plot(p_128, color=ggreen, linestyle='-', label="128 procs")

    plt.savefig("contour_datacontents.pdf",bbox_inches='tight')
    plt.savefig("contour_datacontents.png",bbox_inches='tight')

def streamline_datacontents():
    fig, ax = plt.subplots(figsize=(8,4.6))
    ax.set_xlabel('Simulation computation step', fontsize=16)
    ax.set_ylabel('Streamline filter execution time (ms)', fontsize=12)  

    # set tick
    offset = 0 
    dist = 5.65
    xindex=[]
    for i in range (0,4):
        xindex.append(offset+i*dist)
    ax.set_xticks(xindex)

    ax.set_xticklabels(('2','6','12','18'), fontsize='large')
    
    p_8=(35.7476,35.4319,35.5895,37.1661,40.4976,42.7452,43.6398,44.868,45.6295,44.8202,52.7103,40.5267,43.3378,42.9458,43.9999,44.2738,42.7783,41.0809,40.2514)
    pal=ax.plot(p_8, color=gblue, linestyle='-', label="8 procs")
    
    p_16=(24.4053,24.6026,24.7762,28.7139,32.4622,35.0714,34.5611,33.0653,36.0957,37.4769,52.9509,39.8179,39.0102,36.2645,35.1233,32.0217,33.1785,34.0765,30.6297)
    pal=ax.plot(p_16, color=gred, linestyle='-', label="16 procs")

    p_32=(20.1517,23.1526,23.6768,23.7673,28.297,27.1589,25.6749,26.7626,34.19,37.4052,53.8437,40.823,42.9927,36.9218,35.7424,34.4199,35.4006,31.5214,30.028)
    pal=ax.plot(p_32, color=gyellow, linestyle='-', label="32 procs")

    plt.savefig("streamline_datacontents.pdf",bbox_inches='tight')
    plt.savefig("streamline_datacontents.png",bbox_inches='tight')   

if __name__ == "__main__":
    #render_datasize_procnum()
    #contour_datasize_procnum()
    #streamline_datasize_procnum()
    
    render_datacontents()
    contour_datacontents()
    streamline_datacontents()

    #render_imgsize_procnum()
    #contour_isonumber_values_procnum()
    #streamline_seedsnum_procnum()



