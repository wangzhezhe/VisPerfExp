# the data set comes from https://docs.google.com/spreadsheets/d/18CZWkj6amHAlZv-FcGp4goXa21XrmkYdFJCnlTaCtUs/edit?usp=sharing

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np


gblue = '#4486F4'
gred = '#DA483B'
gyellow = '#FFC718'
ggreen = '#1CA45C'

labelSize=20
ticksize=18
legendsize=22
lwidth=2.5

ylim_low=0
ylim_high=6

ytick_list=['0','10','10^2','10^3','10^4','10^5','10^6']

figsize_y=7


def draw_astro_exec(ax):
    # set titles
    #ax.set_xlabel('(b.1) Supernova', fontsize=labelSize)
    ax.title.set_text('(b.1) Supernova')
    ax.title.set_fontsize(labelSize)
    
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([ylim_low,ylim_high])

    # set tick
    N = 5
    ax.tick_params(axis='y', labelsize=ticksize)
    ax.set_xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (258.076000,320.496000,474.643000,747.654000,1074.158000)
    p1 = ax.plot(np.log10(step_50), color=gblue, label='Step=50',linewidth=lwidth )

    step_100 = ( 510.783000,803.907000,1528.412000,2774.308000,4498.726000)
    p2 = ax.plot(np.log10(step_100), color=gred, label='Step=100',linewidth=lwidth)

    step_500 = ( 1502.149000,2639.681000,5542.308000,8422.152000,15915.459000)
    p3 = ax.plot(np.log10(step_500), color=gyellow, label='Step=500',linewidth=lwidth)

    step_1000 = (1807.770000, 3960.569000,9751.240000,12736.243000,40163.814000)
    p4 = ax.plot(np.log10(step_1000), color=ggreen, label='Step=1000',linewidth=lwidth)
    
    step_2000 = (2100.566000, 6377.275000,16464.272000,22266.060000,92132.543000)
    p4 = ax.plot(np.log10(step_2000), color='purple', label='Step=2000',linewidth=lwidth)
    
    offset = figsize_y/(1.0*(len(ytick_list)-1))
    ax.set_yticks([0,offset,offset*2,offset*3,offset*4,offset*5,offset*6],ytick_list)

def draw_fishtank_exec(ax):
    # set titles
    #ax.set_xlabel('Number of ranks (log scale)', fontsize=labelSize)
    #ax.set_ylabel('Time(ms) (log scale)', fontsize=labelSize)
    #ax.set_xlabel('(c.1) Hydraulics', fontsize=labelSize)
    ax.title.set_text('(c.1) Hydraulics')
    ax.title.set_fontsize(labelSize)

    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([ylim_low,ylim_high])

    # set tick
    N = 5
    ax.tick_params(axis='y', labelsize=ticksize)
    ax.set_xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (297.619000,425.723000,483.097000,622.801000,1000.654000)
    
    p1 = ax.plot(np.log10(step_50), color=gblue, label='Step=50',linewidth=lwidth)

    step_100 = (476.124000,660.840000,794.918000,1092.481000,1925.061000)
    p2 = ax.plot(np.log10(step_100), color=gred, label='Step=100',linewidth=lwidth)

    step_500 = (1214.262000,1649.678000,2067.996000,3044.389000,5094.329000)
    p3 = ax.plot(np.log10(step_500), color=gyellow, label='Step=500',linewidth=lwidth)

    step_1000 = (1423.630000,1977.669000,2467.479000,3614.343000,6022.233000)
    p4 = ax.plot(np.log10(step_1000), color=ggreen, label='Step=1000',linewidth=lwidth)
    
    step_2000 = (1516.090000,	2130.307000,	2659.044000,	3910.404000,	6585.829000 )
    p4 = ax.plot(np.log10(step_2000), color='purple', label='Step=2000',linewidth=lwidth)

    offset = figsize_y/(1.0*(len(ytick_list)-1))
    ax.set_yticks([0,offset,offset*2,offset*3,offset*4,offset*5,offset*6],ytick_list)

def draw_cloverleaf_exec(ax):
    #ax.set_xlabel('(d.1) CloverLeaf3D', fontsize=labelSize)
    ax.title.set_text('(d.1) CloverLeaf3D')
    ax.title.set_fontsize(labelSize)

    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([ylim_low,ylim_high])

    # set tick
    N = 5
    ax.tick_params(axis='y', labelsize=ticksize)
    ax.set_xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    step_50 = (304.810000,387.139000,592.253000,1014.135000,1523.190000)
    
    p1 = ax.plot(np.log10(step_50), color=gblue, label='Step=50',linewidth=lwidth)

    step_100 = (618.046000,785.226000,1340.487000,2517.550000,3810.020000)
    p2 = ax.plot(np.log10(step_100), color=gred, label='Step=100',linewidth=lwidth)

    step_500 = (3030.954000,4376.861000,10701.690000,18607.122000,36782.186000 )
    p3 = ax.plot(np.log10(step_500), color=gyellow, label='Step=500',linewidth=lwidth)

    step_1000 = ( 6158.103000,10471.921000,29537.392000,47852.609000,101932.251000)
    p4 = ax.plot(np.log10(step_1000), color=ggreen, label='Step=1000',linewidth=lwidth)
    
    step_2000 = ( 12605.805000,34055.785000,50192.493000,107640.017000,235403.245000)
    p4 = ax.plot(np.log10(step_2000), color='purple', label='Step=2000',linewidth=lwidth)

    offset = figsize_y/(1.0*(len(ytick_list)-1))
    ax.set_yticks([0,offset,offset*2,offset*3,offset*4,offset*5,offset*6],ytick_list)

def draw_fusion_exec(ax):
    ax.set_ylabel('Time(ms)', fontsize=labelSize)
    #ax.set_xlabel('Number of ranks (log scale) \n(a) Tokamak', fontsize=labelSize)
    #ax.set_xlabel('(a.1) Tokamak', fontsize=labelSize)
    ax.title.set_text('(a.1) Tokamak')
    ax.title.set_fontsize(labelSize)


    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([ylim_low,ylim_high])

    # set tick
    N = 5
    ax.tick_params(axis='y', labelsize=ticksize)
    ax.set_xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    step_50 = (239.024000,282.016000,371.916000,480.013000,539.107000)
    
    p1 = ax.plot(np.log10(step_50), color=gblue, label='Step=50',linewidth=lwidth)

    step_100 = (402.658000,477.712000,677.778000,874.209000,1002.778000)
    p2 = ax.plot(np.log10(step_100), color=gred, label='Step=100',linewidth=lwidth)

    step_500 = (1558,2435,3454,4177,5019)
    p3 = ax.plot(np.log10(step_500), color=gyellow, label='Step=500',linewidth=lwidth)

    step_1000 = (2901,4588,6261,7572,9829)
    p4 = ax.plot(np.log10(step_1000), color=ggreen, label='Step=1000',linewidth=lwidth)
    
    step_2000 = (5689,8474,11369,14633,19520)
    p4 = ax.plot(np.log10(step_2000), color='purple', label='Step=2000',linewidth=lwidth)

    # only label the y tick for fusion data
    # figure size is 7*5
    offset = figsize_y/(1.0*(len(ytick_list)-1))
    ax.set_yticks([0,offset,offset*2,offset*3,offset*4,offset*5,offset*6],ytick_list)



def draw_syn_exec(ax):
    #ax.set_xlabel('(e.1) Synthetic', fontsize=labelSize)
    ax.title.set_text('(e.1) Synthetic')
    ax.title.set_fontsize(labelSize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([ylim_low,ylim_high])

    # set tick
    N = 5
    ax.tick_params(axis='y', labelsize=ticksize)
    ax.set_xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    step_50 = (401,	406,	672,	1022,	1110  )
    
    p1 = ax.plot(np.log10(step_50), color=gblue, label='Step=50',linewidth=lwidth)

    step_100 = (712,	723,	1250,	1806,	2064 )
    p2 = ax.plot(np.log10(step_100), color=gred, label='Step=100',linewidth=lwidth)

    step_500 = (3039,	3089,	6272,	9366,	9319 )
    p3 = ax.plot(np.log10(step_500), color=gyellow, label='Step=500',linewidth=lwidth)

    step_1000 = (5982,	6094,	12533,	19025,	21751 )
    p4 = ax.plot(np.log10(step_1000), color=ggreen, label='Step=1000',linewidth=lwidth)
    
    step_2000 = (11796,	11967,	25351,	37331,	41957 )
    p4 = ax.plot(np.log10(step_2000), color='purple', label='Step=2000',linewidth=lwidth)

    offset = figsize_y/(1.0*(len(ytick_list)-1))
    ax.set_yticks([0,offset,offset*2,offset*3,offset*4,offset*5,offset*6],ytick_list)

    offset = figsize_y/(1.0*(len(ytick_list)-1))
    ax.set_yticks([0,offset,offset*2,offset*3,offset*4,offset*5,offset*6],ytick_list)

def draw_fusion_eff(ax):
    ax.set_ylabel('Weak scaling efficiency', fontsize=labelSize)
    #ax.set_xlabel('(a.2) Tokamak', fontsize=labelSize)
    ax.title.set_text('(a.2) Tokamak')
    ax.title.set_fontsize(labelSize)    
    step_50 = (239.024000,282.016000,371.916000,480.013000,539.107000)
    step_100 = (402.658000,477.712000,677.778000,874.209000,1002.778000)
    step_500 = (1558,2435,3454,4177,5019)
    step_1000 = (2901,4588,6261,7572,9829)    
    step_2000 = (5689,8474,11369,14633,19520)
    
    N = 5
    ax.tick_params(axis='y', labelsize=ticksize)
    ax.set_xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_ylim([0, 1.1])
    ax.set_axisbelow(True)

    step_50_eff = [step_50[0]/v for v in step_50]
    p1 = ax.plot(step_50_eff, color=gblue,linewidth=lwidth)

    #print(step_50_eff)
    step_100_eff = [step_100[0]/v for v in step_100]
    p2 = ax.plot(step_100_eff, color=gred,linewidth=lwidth)

    step_500_eff = [step_500[0]/v for v in step_500]
    p3 = ax.plot(step_500_eff, color=gyellow,linewidth=lwidth)

    step_1000_eff = [step_1000[0]/v for v in step_1000]
    p4 = ax.plot(step_1000_eff, color=ggreen,linewidth=lwidth)

    step_2000_eff = [step_2000[0]/v for v in step_2000]
    p4 = ax.plot(step_2000_eff, color='purple',linewidth=lwidth)
    

def draw_astro_eff(ax):
    #ax.set_xlabel('(b.2) Supernova', fontsize=labelSize)
    ax.title.set_text('(b.2) Supernova')
    ax.title.set_fontsize(labelSize)     
    step_50 = (258.076000,320.496000,474.643000,747.654000,1074.158000)
    step_100 = ( 510.783000,803.907000,1528.412000,2774.308000,4498.726000)
    step_500 = ( 1502.149000,2639.681000,5542.308000,8422.152000,15915.459000)
    step_1000 = (1807.770000, 3960.569000,9751.240000,12736.243000,40163.814000)    
    step_2000 = (2100.566000, 6377.275000,16464.272000,22266.060000,92132.543000)

    N = 5
    ax.tick_params(axis='y', labelsize=ticksize)
    ax.set_xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_ylim([0, 1.1])
    ax.set_axisbelow(True)

    step_50_eff = [step_50[0]/v for v in step_50]
    p1 = ax.plot(step_50_eff, color=gblue, label='Step=50',linewidth=lwidth)

    step_100_eff = [step_100[0]/v for v in step_100]
    p2 = ax.plot(step_100_eff, color=gred, label='Step=100',linewidth=lwidth)

    step_500_eff = [step_500[0]/v for v in step_500]
    p3 = ax.plot(step_500_eff, color=gyellow, label='Step=500',linewidth=lwidth)

    step_1000_eff = [step_1000[0]/v for v in step_1000]
    p4 = ax.plot(step_1000_eff, color=ggreen, label='Step=1000',linewidth=lwidth)

    step_2000_eff = [step_2000[0]/v for v in step_2000]
    p4 = ax.plot(step_2000_eff, color='purple', label='Step=2000',linewidth=lwidth)

def draw_fishtank_eff(ax):
    #ax.set_xlabel('(c.2) Hydraulics', fontsize=labelSize)
    ax.title.set_text('(c.2) Hydraulics')
    ax.title.set_fontsize(labelSize)  
    step_50 = (297.619000,425.723000,483.097000,622.801000,1000.654000)
    step_100 = (476.124000,660.840000,794.918000,1092.481000,1925.061000)
    step_500 = (1214.262000,1649.678000,2067.996000,3044.389000,5094.329000)
    step_1000 = (1423.630000,1977.669000,2467.479000,3614.343000,6022.233000)    
    step_2000 = (1516.090000,	2130.307000,	2659.044000,	3910.404000,	6585.829000 )
    
    N = 5
    ax.tick_params(axis='y', labelsize=ticksize)
    ax.set_xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_ylim([0, 1.1])
    ax.set_axisbelow(True)

    step_50_eff = [step_50[0]/v for v in step_50]
    p1 = ax.plot(step_50_eff, color=gblue, label='Step=50',linewidth=lwidth)

    #print(step_50_eff)
    step_100_eff = [step_100[0]/v for v in step_100]
    p2 = ax.plot(step_100_eff, color=gred, label='Step=100',linewidth=lwidth)

    step_500_eff = [step_500[0]/v for v in step_500]
    p3 = ax.plot(step_500_eff, color=gyellow, label='Step=500',linewidth=lwidth)

    step_1000_eff = [step_1000[0]/v for v in step_1000]
    p4 = ax.plot(step_1000_eff, color=ggreen, label='Step=1000',linewidth=lwidth)

    step_2000_eff = [step_2000[0]/v for v in step_2000]
    p4 = ax.plot(step_2000_eff, color='purple', label='Step=2000',linewidth=lwidth)

def draw_cloverleaf_eff(ax):

    step_50 = (304.810000,387.139000,592.253000,1014.135000,1523.190000)
    step_100 = (618.046000,785.226000,1340.487000,2517.550000,3810.020000)
    step_500 = (3030.954000,4376.861000,10701.690000,18607.122000,36782.186000 )
    step_1000 = ( 6158.103000,10471.921000,29537.392000,47852.609000,101932.251000)
    step_2000 = ( 12605.805000,34055.785000,50192.493000,107640.017000,235403.245000)

    N = 5
    #ax.set_xlabel('(d.2) CloverLeaf3D', fontsize=labelSize)
    ax.title.set_text('(d.2) CloverLeaf3D')
    ax.title.set_fontsize(labelSize) 
    
    ax.tick_params(axis='y', labelsize=ticksize)
    ax.set_xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_ylim([0, 1.1])
    ax.set_axisbelow(True)

    step_50_eff = [step_50[0]/v for v in step_50]
    p1 = ax.plot(step_50_eff, color=gblue, label='Step=50',linewidth=lwidth)

    step_100_eff = [step_100[0]/v for v in step_100]
    p2 = ax.plot(step_100_eff, color=gred, label='Step=100',linewidth=lwidth)

    step_500_eff = [step_500[0]/v for v in step_500]
    p3 = ax.plot(step_500_eff, color=gyellow, label='Step=500',linewidth=lwidth)

    step_1000_eff = [step_1000[0]/v for v in step_1000]
    p4 = ax.plot(step_1000_eff, color=ggreen, label='Step=1000',linewidth=lwidth)

    step_2000_eff = [step_2000[0]/v for v in step_2000]
    p4 = ax.plot(step_2000_eff, color='purple', label='Step=2000',linewidth=lwidth)

def draw_syn_eff(ax):

    step_50 = (401,	406,	672,	1022,	1110  )
    step_100 = (712,	723,	1250,	1806,	2064 )
    step_500 = (3039,	3089,	6272,	9366,	9319 )
    step_1000 = (5982,	6094,	12533,	19025,	21751 )    
    step_2000 = (11796,	11967,	25351,	37331,	41957 )

    N = 5
    #ax.set_xlabel('(e.2) Synthetic', fontsize=labelSize)
    ax.title.set_text('(e.2) Synthetic')
    ax.title.set_fontsize(labelSize) 

    ax.tick_params(axis='y', labelsize=ticksize)
    ax.set_xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_ylim([0, 1.1])
    ax.set_axisbelow(True)

    step_50_eff = [step_50[0]/v for v in step_50]
    p1 = ax.plot(step_50_eff, color=gblue, label='Step=50',linewidth=lwidth)

    step_100_eff = [step_100[0]/v for v in step_100]
    p2 = ax.plot(step_100_eff, color=gred, label='Step=100',linewidth=lwidth)

    step_500_eff = [step_500[0]/v for v in step_500]
    p3 = ax.plot(step_500_eff, color=gyellow, label='Step=500',linewidth=lwidth)

    step_1000_eff = [step_1000[0]/v for v in step_1000]
    p4 = ax.plot(step_1000_eff, color=ggreen, label='Step=1000',linewidth=lwidth)

    step_2000_eff = [step_2000[0]/v for v in step_2000]
    p4 = ax.plot(step_2000_eff, color='purple', label='Step=2000',linewidth=lwidth)


def all_exec_eff_time():
    fig, axs = plt.subplots(nrows=2, ncols=5, figsize=(7*5,5*2))
    #print(len(axs),len(axs[0]))
    draw_fusion_exec(axs[0][0])
    draw_astro_exec(axs[0][1])
    draw_fishtank_exec(axs[0][2])
    draw_cloverleaf_exec(axs[0][3])
    draw_syn_exec(axs[0][4])

    draw_fusion_eff(axs[1][0])
    draw_astro_eff(axs[1][1])
    draw_fishtank_eff(axs[1][2])
    draw_cloverleaf_eff(axs[1][3])
    draw_syn_eff(axs[1][4])

    handles, labels = axs[0][4].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=5, loc='upper center', fontsize=legendsize)

    fig.text(0.5, 0.04, 'Number of ranks', ha='center',fontsize=labelSize+5)

    plt.savefig("all_exec_eff_time.png", bbox_inches='tight')
    plt.savefig("all_exec_eff_time.pdf", bbox_inches='tight')


if __name__ == "__main__":
    all_exec_eff_time()    
