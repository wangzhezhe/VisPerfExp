# the data set comes from https://docs.google.com/spreadsheets/d/18CZWkj6amHAlZv-FcGp4goXa21XrmkYdFJCnlTaCtUs/edit?usp=sharing

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np


gblue = '#4486F4'
gred = '#DA483B'
gyellow = '#FFC718'
ggreen = '#1CA45C'

def draw_astro_weakscale():
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize='large')
    ax.set_ylabel('Time(ms) (log scale)', fontsize='large')
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([7.5,23])

    # set tick
    N = 5

    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize='large')
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (711,710,1002,1305,2127)
    p1 = ax.plot(np.log2(step_50), color=gblue, label='Step=50')

    step_100 = (1214,	1544,	4762,	7091,	19780 )
    p2 = ax.plot(np.log2(step_100), color=gred, label='Step=100')

    step_500 = (4869,	17819,	63444,	158763,	191289 )
    p3 = ax.plot(np.log2(step_500), color=gyellow, label='Step=500')

    step_1000 = (7738,	36380,	96901,	197271,	400920 )
    p4 = ax.plot(np.log2(step_1000), color=ggreen, label='Step=1000')
    
    step_2000 = (13421,	27666,	67997,	185826,	459255 )
    p4 = ax.plot(np.log2(step_2000), color='purple', label='Step=2000')


    ax.legend(ncol=3, loc='upper center', fontsize=11)

    plt.savefig("draw_astro_weakscale.pdf", bbox_inches='tight')
    plt.savefig("draw_astro_weakscale.png", bbox_inches='tight')

def draw_fishtank_weakscale():
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize='large')
    ax.set_ylabel('Time(ms) (log scale)', fontsize='large')
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([7.5,23])

    # set tick
    N = 5

    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize='large')
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (1092,	1133,	1466,1520,3118)
    
    p1 = ax.plot(np.log2(step_50), color=gblue, label='Step=50')

    step_100 = (1741,	1881,	2428,	2197,	7658 )
    p2 = ax.plot(np.log2(step_100), color=gred, label='Step=100')

    step_500 = (4238,	4304,	7133,	8340,	64107 )
    p3 = ax.plot(np.log2(step_500), color=gyellow, label='Step=500')

    step_1000 = (5739,	6098,	7882,	15028,	52725 )
    p4 = ax.plot(np.log2(step_1000), color=ggreen, label='Step=1000')
    
    step_2000 = (6897,	8548,	10319,	26775,	33338 )
    p4 = ax.plot(np.log2(step_2000), color='purple', label='Step=2000')


    ax.legend(ncol=3, loc='upper center', fontsize=11)

    plt.savefig("draw_fishtank_weakscale.pdf", bbox_inches='tight')
    plt.savefig("draw_fishtank_weakscale.png", bbox_inches='tight')

def draw_fusion_weakscale():
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize='large')
    ax.set_ylabel('Time(ms) (log scale)', fontsize='large')
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([7.5,23])

    # set tick
    N = 5

    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize='large')
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (537,589,	738,	909,	1465)
    
    p1 = ax.plot(np.log2(step_50), color=gblue, label='Step=50')

    step_100 = (878,	958,	1252,	1664,	3686)
    p2 = ax.plot(np.log2(step_100), color=gred, label='Step=100')

    step_500 = (3976,	4717,	11265,	6810,	26109)
    p3 = ax.plot(np.log2(step_500), color=gyellow, label='Step=500')

    step_1000 = (7138,	8039,	33216,	14440,	52557)
    p4 = ax.plot(np.log2(step_1000), color=ggreen, label='Step=1000')
    
    step_2000 = (6897,	8548,	10319,	26775,	33338 )
    p4 = ax.plot(np.log2(step_2000), color='purple', label='Step=2000')


    ax.legend(ncol=3, loc='upper center', fontsize=11)

    plt.savefig("draw_fusion_weakscale.pdf", bbox_inches='tight')
    plt.savefig("draw_fusion_weakscale.png", bbox_inches='tight')


def draw_cloverleaf_weakscale():
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize='large')
    ax.set_ylabel('Time(ms) (log scale)', fontsize='large')
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([7.5,23])

    # set tick
    N = 5

    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize='large')
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (850,	1005,	1226,	1520,	3823 )
    
    p1 = ax.plot(np.log2(step_50), color=gblue, label='Step=50')

    step_100 = (1388,	1676,	3358,	2197,	15057 )
    p2 = ax.plot(np.log2(step_100), color=gred, label='Step=100')

    step_500 = (6175,	7751,	12905,	8340,	171144 )
    p3 = ax.plot(np.log2(step_500), color=gyellow, label='Step=500')

    step_1000 = (11273,	17748,	32459,	15028,	199675 )
    p4 = ax.plot(np.log2(step_1000), color=ggreen, label='Step=1000')
    
    step_2000 = (21478,	35716,	63220,	26775,	387163 )
    p4 = ax.plot(np.log2(step_2000), color='purple', label='Step=2000')


    ax.legend(ncol=3, loc='upper center', fontsize=11)

    plt.savefig("draw_cloverleaf_weakscale.pdf", bbox_inches='tight')
    plt.savefig("draw_cloverleaf_weakscale.png", bbox_inches='tight')

def draw_fusion_weakscale():
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize='large')
    ax.set_ylabel('Time(ms) (log scale)', fontsize='large')
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([7.5,23])

    # set tick
    N = 5

    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize='large')
    # set the value of the figure here
    # use the capsize to control the error bar
    step_50 = (537,	589,	738,	909	,1465)
    
    p1 = ax.plot(np.log2(step_50), color=gblue, label='Step=50')

    step_100 = (878,	958,	1252,	1664,	3686)
    p2 = ax.plot(np.log2(step_100), color=gred, label='Step=100')

    step_500 = (3976,	4717,	11265,	6810,	26109)
    p3 = ax.plot(np.log2(step_500), color=gyellow, label='Step=500')

    step_1000 = (7138,	8039,	33216,	14440,	52557)
    p4 = ax.plot(np.log2(step_1000), color=ggreen, label='Step=1000')
    
    step_2000 = (12170,	14617,	198387,	22718,	175825)
    p4 = ax.plot(np.log2(step_2000), color='purple', label='Step=2000')

    ax.legend(ncol=3, loc='upper center', fontsize=11)

    plt.savefig("draw_fusion_weakscale.pdf", bbox_inches='tight')
    plt.savefig("draw_fusion_weakscale.png", bbox_inches='tight')

def draw_syn_weakscale():
    fig, ax = plt.subplots(figsize=(6,4.5))
    # set titles
    ax.set_xlabel('Number of ranks (log scale)', fontsize='large')
    ax.set_ylabel('Time(ms) (log scale)', fontsize='large')
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    ax.set_ylim([7.5,23])

    # set tick
    N = 5

    plt.xticks(range(N), ['8', '16' , '32', '64', '128'], fontsize='large')
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

    ax.legend(ncol=3, loc='upper center', fontsize=11)

    plt.savefig("draw_syn_weakscale.pdf", bbox_inches='tight')
    plt.savefig("draw_syn_weakscale.png", bbox_inches='tight')

if __name__ == "__main__":
    draw_astro_weakscale()
    draw_fishtank_weakscale()
    draw_cloverleaf_weakscale()
    draw_fusion_weakscale()
    draw_syn_weakscale()
    