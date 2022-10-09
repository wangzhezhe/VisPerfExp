
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



if __name__ == "__main__":
    render_datasize_procnum()
    contour_datasize_procnum()
    streamline_datasize_procnum()
    
    #render_datacontents()
    #contour_datacontents()
    #streamline_datacontents()

    #render_imgsize_procnum()
    #contour_isonumber_values_procnum()
    #streamline_seedsnum_procnum()



