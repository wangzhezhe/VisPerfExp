# the data set comes from https://docs.google.com/spreadsheets/d/18CZWkj6amHAlZv-FcGp4goXa21XrmkYdFJCnlTaCtUs/edit?usp=sharing

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np


gblue = '#4486F4'
gred = '#DA483B'
gyellow = '#FFC718'
ggreen = '#1CA45C'

ticksize=15
legendsize=11

def draw_astro_weakscale():
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize=ticksize)
    ax.set_ylabel('Time(ms) (log scale)', fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([7.5,23])

    # set tick
    N = 5

    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (258.076000,320.496000,474.643000,747.654000,1074.158000)
    p1 = ax.plot(np.log2(step_50), color=gblue, label='Step=50')

    step_100 = ( 510.783000,803.907000,1528.412000,2774.308000,4498.726000)
    p2 = ax.plot(np.log2(step_100), color=gred, label='Step=100')

    step_500 = ( 1502.149000,2639.681000,5542.308000,8422.152000,15915.459000)
    p3 = ax.plot(np.log2(step_500), color=gyellow, label='Step=500')

    step_1000 = (1807.770000, 3960.569000,9751.240000,12736.243000,40163.814000)
    p4 = ax.plot(np.log2(step_1000), color=ggreen, label='Step=1000')
    
    step_2000 = (2100.566000, 6377.275000,16464.272000,22266.060000,92132.543000)
    p4 = ax.plot(np.log2(step_2000), color='purple', label='Step=2000')


    ax.legend(ncol=3, loc='upper center', fontsize=legendsize)

    plt.savefig("draw_astro_weakscale_time.pdf", bbox_inches='tight')
    plt.savefig("draw_astro_weakscale_time.png", bbox_inches='tight')

    # efficiency of weak scale
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize=ticksize)
    ax.set_ylabel('Weak scaling efficiency',fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)
    ax.set_ylim([0,1.25])
    # set tick
    N = 5
    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    step_50_eff = [step_50[0]/v for v in step_50]
    p1 = ax.plot(step_50_eff, color=gblue, label='Step=50')

    #print(step_50_eff)
    step_100_eff = [step_100[0]/v for v in step_100]
    p2 = ax.plot(step_100_eff, color=gred, label='Step=100')

    step_500_eff = [step_500[0]/v for v in step_500]
    p3 = ax.plot(step_500_eff, color=gyellow, label='Step=500')

    step_1000_eff = [step_1000[0]/v for v in step_1000]
    p4 = ax.plot(step_1000_eff, color=ggreen, label='Step=1000')

    step_2000_eff = [step_2000[0]/v for v in step_2000]
    p4 = ax.plot(step_2000_eff, color='purple', label='Step=2000')
    ax.legend(ncol=3, loc='upper center', fontsize=legendsize)

    plt.savefig("draw_astro_weakscale_eff.pdf", bbox_inches='tight')
    plt.savefig("draw_astro_weakscale_eff.png", bbox_inches='tight')

def draw_fishtank_weakscale():
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize=ticksize)
    ax.set_ylabel('Time(ms) (log scale)', fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([7.5,23])

    # set tick
    N = 5

    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (297.619000,425.723000,483.097000,622.801000,1000.654000)
    
    p1 = ax.plot(np.log2(step_50), color=gblue, label='Step=50')

    step_100 = (476.124000,660.840000,794.918000,1092.481000,1925.061000)
    p2 = ax.plot(np.log2(step_100), color=gred, label='Step=100')

    step_500 = (1214.262000,1649.678000,2067.996000,3044.389000,5094.329000)
    p3 = ax.plot(np.log2(step_500), color=gyellow, label='Step=500')

    step_1000 = (1423.630000,1977.669000,2467.479000,3614.343000,6022.233000)
    p4 = ax.plot(np.log2(step_1000), color=ggreen, label='Step=1000')
    
    step_2000 = (1516.090000,	2130.307000,	2659.044000,	3910.404000,	6585.829000 )
    p4 = ax.plot(np.log2(step_2000), color='purple', label='Step=2000')


    ax.legend(ncol=3, loc='upper center', fontsize=legendsize)

    plt.savefig("draw_fishtank_weakscale.pdf", bbox_inches='tight')
    plt.savefig("draw_fishtank_weakscale.png", bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize=ticksize)
    ax.set_ylabel('Weak scaling efficiency', fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)
    ax.set_ylim([0,1.25])
    # set tick
    N = 5
    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    step_50_eff = [step_50[0]/v for v in step_50]
    p1 = ax.plot(step_50_eff, color=gblue, label='Step=50')

    #print(step_50_eff)
    step_100_eff = [step_100[0]/v for v in step_100]
    p2 = ax.plot(step_100_eff, color=gred, label='Step=100')

    step_500_eff = [step_500[0]/v for v in step_500]
    p3 = ax.plot(step_500_eff, color=gyellow, label='Step=500')

    step_1000_eff = [step_1000[0]/v for v in step_1000]
    p4 = ax.plot(step_1000_eff, color=ggreen, label='Step=1000')

    step_2000_eff = [step_2000[0]/v for v in step_2000]
    p4 = ax.plot(step_2000_eff, color='purple', label='Step=2000')
    ax.legend(ncol=3, loc='upper center', fontsize=legendsize)

    plt.savefig("draw_fishtank_weakscale_eff.pdf", bbox_inches='tight')
    plt.savefig("draw_fishtank_weakscale_eff.png", bbox_inches='tight')

def draw_fusion_weakscale():
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize=ticksize)
    ax.set_ylabel('Time(ms) (log scale)', fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([7.5,23])

    # set tick
    N = 5

    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (239.024000,282.016000,371.916000,480.013000,539.107000)
    
    p1 = ax.plot(np.log2(step_50), color=gblue, label='Step=50')

    step_100 = (402.658000,	477.712000,	677.778000,	874.209000,	1002.778000)
    p2 = ax.plot(np.log2(step_100), color=gred, label='Step=100')

    step_500 = (1558.789000,	2435.911000,	3454.862000,	4177.237000,	5019.272000)
    p3 = ax.plot(np.log2(step_500), color=gyellow, label='Step=500')

    step_1000 = (2901.121000,	4588.999000,	6261.203000,	7572.991000,	9829.443000)
    p4 = ax.plot(np.log2(step_1000), color=ggreen, label='Step=1000')
    
    step_2000 = (5689.222000,	8474.597000,	11369.773000,	14633.478000,	19520.140000 )
    p4 = ax.plot(np.log2(step_2000), color='purple', label='Step=2000')


    ax.legend(ncol=3, loc='upper center', fontsize=legendsize)

    plt.savefig("draw_fusion_weakscale.pdf", bbox_inches='tight')
    plt.savefig("draw_fusion_weakscale.png", bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize=ticksize)
    ax.set_ylabel('Weak scaling efficiency', fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)
    ax.set_ylim([0,1.25])
    # set tick
    N = 5
    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    step_50_eff = [step_50[0]/v for v in step_50]
    p1 = ax.plot(step_50_eff, color=gblue, label='Step=50')

    #print(step_50_eff)
    step_100_eff = [step_100[0]/v for v in step_100]
    p2 = ax.plot(step_100_eff, color=gred, label='Step=100')

    step_500_eff = [step_500[0]/v for v in step_500]
    p3 = ax.plot(step_500_eff, color=gyellow, label='Step=500')

    step_1000_eff = [step_1000[0]/v for v in step_1000]
    p4 = ax.plot(step_1000_eff, color=ggreen, label='Step=1000')

    step_2000_eff = [step_2000[0]/v for v in step_2000]
    p4 = ax.plot(step_2000_eff, color='purple', label='Step=2000')
    ax.legend(ncol=3, loc='upper center', fontsize=legendsize)

    plt.savefig("draw_astro_weakscale_eff.pdf", bbox_inches='tight')
    plt.savefig("draw_astro_weakscale_eff.png", bbox_inches='tight')


def draw_cloverleaf_weakscale():
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize=ticksize)
    ax.set_ylabel('Time(ms) (log scale)', fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([7.5,23])

    # set tick
    N = 5

    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (304.810000,387.139000,592.253000,1014.135000,1523.190000)
    
    p1 = ax.plot(np.log2(step_50), color=gblue, label='Step=50')

    step_100 = (618.046000,785.226000,1340.487000,2517.550000,3810.020000)
    p2 = ax.plot(np.log2(step_100), color=gred, label='Step=100')

    step_500 = (3030.954000,4376.861000,10701.690000,18607.122000,36782.186000 )
    p3 = ax.plot(np.log2(step_500), color=gyellow, label='Step=500')

    step_1000 = ( 6158.103000,10471.921000,29537.392000,47852.609000,101932.251000)
    p4 = ax.plot(np.log2(step_1000), color=ggreen, label='Step=1000')
    
    step_2000 = ( 12605.805000,34055.785000,50192.493000,107640.017000,235403.245000)
    p4 = ax.plot(np.log2(step_2000), color='purple', label='Step=2000')


    ax.legend(ncol=3, loc='upper center', fontsize=legendsize)

    plt.savefig("draw_cloverleaf_weakscale.pdf", bbox_inches='tight')
    plt.savefig("draw_cloverleaf_weakscale.png", bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize=ticksize)
    ax.set_ylabel('Weak scaling efficiency', fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)
    ax.set_ylim([0,1.25])
    # set tick
    N = 5
    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    step_50_eff = [step_50[0]/v for v in step_50]
    p1 = ax.plot(step_50_eff, color=gblue, label='Step=50')

    #print(step_50_eff)
    step_100_eff = [step_100[0]/v for v in step_100]
    p2 = ax.plot(step_100_eff, color=gred, label='Step=100')

    step_500_eff = [step_500[0]/v for v in step_500]
    p3 = ax.plot(step_500_eff, color=gyellow, label='Step=500')

    step_1000_eff = [step_1000[0]/v for v in step_1000]
    p4 = ax.plot(step_1000_eff, color=ggreen, label='Step=1000')

    step_2000_eff = [step_2000[0]/v for v in step_2000]
    p4 = ax.plot(step_2000_eff, color='purple', label='Step=2000')
    ax.legend(ncol=3, loc='upper center', fontsize=legendsize)

    plt.savefig("draw_cloverleaf_weakscale_eff.pdf", bbox_inches='tight')
    plt.savefig("draw_cloverleaf_weakscale_eff.png", bbox_inches='tight')

def draw_fusion_weakscale():
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize=ticksize)
    ax.set_ylabel('Time(ms) (log scale)', fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([7.5,23])

    # set tick
    N = 5

    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (239.024000,282.016000,371.916000,480.013000,539.107000)
    
    p1 = ax.plot(np.log2(step_50), color=gblue, label='Step=50')

    step_100 = (402.658000,477.712000,677.778000,874.209000,1002.778000)
    p2 = ax.plot(np.log2(step_100), color=gred, label='Step=100')

    step_500 = (1558,2435,3454,4177,5019)
    p3 = ax.plot(np.log2(step_500), color=gyellow, label='Step=500')

    step_1000 = (2901,4588,6261,7572,9829)
    p4 = ax.plot(np.log2(step_1000), color=ggreen, label='Step=1000')
    
    step_2000 = (5689,8474,11369,14633,19520)
    p4 = ax.plot(np.log2(step_2000), color='purple', label='Step=2000')

    ax.legend(ncol=3, loc='upper center', fontsize=legendsize)

    plt.savefig("draw_fusion_weakscale.pdf", bbox_inches='tight')
    plt.savefig("draw_fusion_weakscale.png", bbox_inches='tight')


    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize=ticksize)
    ax.set_ylabel('Weak scaling efficiency', fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)
    ax.set_ylim([0,1.25])
    # set tick
    N = 5
    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    step_50_eff = [step_50[0]/v for v in step_50]
    p1 = ax.plot(step_50_eff, color=gblue, label='Step=50')

    #print(step_50_eff)
    step_100_eff = [step_100[0]/v for v in step_100]
    p2 = ax.plot(step_100_eff, color=gred, label='Step=100')

    step_500_eff = [step_500[0]/v for v in step_500]
    p3 = ax.plot(step_500_eff, color=gyellow, label='Step=500')

    step_1000_eff = [step_1000[0]/v for v in step_1000]
    p4 = ax.plot(step_1000_eff, color=ggreen, label='Step=1000')

    step_2000_eff = [step_2000[0]/v for v in step_2000]
    p4 = ax.plot(step_2000_eff, color='purple', label='Step=2000')
    ax.legend(ncol=3, loc='upper center', fontsize=legendsize)

    plt.savefig("draw_fusion_weakscale_eff.pdf", bbox_inches='tight')
    plt.savefig("draw_fusion_weakscale_eff.png", bbox_inches='tight')

def draw_syn_weakscale():
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize=ticksize)
    ax.set_ylabel('Time(ms) (log scale)', fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([7.5,23])

    # set tick
    N = 5

    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (401,	406,	672,	1022,	1110  )
    
    p1 = ax.plot(np.log2(step_50), color=gblue, label='Step=50')

    step_100 = (712,	723,	1250,	1806,	2064 )
    p2 = ax.plot(np.log2(step_100), color=gred, label='Step=100')

    step_500 = (3039,	3089,	6272,	9366,	9319 )
    p3 = ax.plot(np.log2(step_500), color=gyellow, label='Step=500')

    step_1000 = (5982,	6094,	12533,	19025,	21751 )
    p4 = ax.plot(np.log2(step_1000), color=ggreen, label='Step=1000')
    
    step_2000 = (11796,	11967,	25351,	37331,	41957 )
    p4 = ax.plot(np.log2(step_2000), color='purple', label='Step=2000')

    ax.legend(ncol=3, loc='upper center', fontsize=legendsize)

    plt.savefig("draw_syn_weakscale.pdf", bbox_inches='tight')
    plt.savefig("draw_syn_weakscale.png", bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize=ticksize)
    ax.set_ylabel('Weak scaling efficiency', fontsize=ticksize)
    ax.grid(axis='y')
    ax.set_axisbelow(True)
    ax.set_ylim([0,1.25])
    # set tick
    N = 5
    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize=ticksize)
    step_50_eff = [step_50[0]/v for v in step_50]
    p1 = ax.plot(step_50_eff, color=gblue, label='Step=50')

    #print(step_50_eff)
    step_100_eff = [step_100[0]/v for v in step_100]
    p2 = ax.plot(step_100_eff, color=gred, label='Step=100')

    step_500_eff = [step_500[0]/v for v in step_500]
    p3 = ax.plot(step_500_eff, color=gyellow, label='Step=500')

    step_1000_eff = [step_1000[0]/v for v in step_1000]
    p4 = ax.plot(step_1000_eff, color=ggreen, label='Step=1000')

    step_2000_eff = [step_2000[0]/v for v in step_2000]
    p4 = ax.plot(step_2000_eff, color='purple', label='Step=2000')
    ax.legend(ncol=3, loc='upper center', fontsize=legendsize)

    plt.savefig("draw_syn_weakscale_eff.pdf", bbox_inches='tight')
    plt.savefig("draw_syn_weakscale_eff.png", bbox_inches='tight')

if __name__ == "__main__":
    draw_astro_weakscale()
    draw_fishtank_weakscale()
    draw_cloverleaf_weakscale()
    draw_fusion_weakscale()
    draw_syn_weakscale()
    