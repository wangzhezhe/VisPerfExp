import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import numpy as np

gblue = '#4486F4'
gred = '#DA483B'
gyellow = '#FFC718'
ggreen = '#1CA45C'

ticksize=20
labelSize=26
legendSize=22

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(7,4))
    # set titles
    ax.set_ylabel('Ratio', fontsize=16)
    ax.set_xlabel('Iteration', fontsize=16)
    ax.grid(axis='y')
    ax.set_axisbelow(True)
    ax.set_ylim([0,1.1])

    ax.tick_params(axis='both', which='major', labelsize=13.6)

    # set tick
    N = 5
    #ind = np.arange(N)    # the x locations for the groups
    #width = 0.15       # the width of the bars
    #.set_xticks(ind + 1.5*width)
    #ax.set_xticklabels(('256/32/8', '512/64/16' , '1024/128/32', '2048/256/64', '4096/512/128'), fontsize='large')

    # plt.xticks(range(N), ['256/32/8', '512/64/16' , '1024/128/32', '2048/256/64', '4096/512/128'], fontsize='large')
    # set the value of the figure here
    # use the capsize to control the error bar
    tpMeans = (1,
0.6021499811,
0.6103426246,
0.5617581249,
0.5319503928,
0.5272688452,
0.5079360226,
0.5130619706,
0.5151190786)
    p1 = ax.plot(tpMeans, color=gblue, marker='.', label='Tokamak')


    tpMeans = (1,
0.5723250158,
0.4896107855,
0.4677498361,
0.5108355195,
0.4142804463,
0.4086449818,
0.4217199504,
0.4848772804)
    p2 = ax.plot( tpMeans,  color=gred, marker='.', label='Supernova')

    tpMeans = (1,
0.465079496,
0.4427869887,
0.4926041323,
0.4704107744,
0.3976917329,
0.3802361239,
0.3889815848,
0.3772877976)
    p3 = ax.plot(tpMeans, color=gyellow, marker='.', label='Hydraulics')


    tpMeans = (1,
0.1057602435,
0.1004066811,
0.08965463003,
0.08729474675,
0.0857651246,
0.08818528176,
0.07849038983,
0.08761452036)
    p4 = ax.plot( tpMeans, color=ggreen, marker='.',  label='CloverLeaf3D')
    
    tpMeans = (1,
0.9878708484,
0.501261816,
0.5173327111,
0.4992041117,
0.5072044209,
0.5057679634,
0.513391589,
0.5091553044)
    p5 = ax.plot( tpMeans,  color='purple', marker='.',  label='Synthetic')

    # add the lengend for the data by defualt
    # this can be at the centric legend
    ax.legend(ncol=2, fontsize=14)
    # ax.legend((p1[0], p2[0], p3[0], p4[0]), ('producer-responsible', 'consumer-responsible','metadata-polling','topic-matching'),fontsize='large')
    # customize the legend
    #legend_elem_1 = [Patch(facecolor='#B4E1FF', edgecolor='black', label='Cache hit at remote DTN'),
    #                     Patch(facecolor='#AB87FF', edgecolor='black', label='Cache hit at local DTN')]
    #legend1 = plt.legend(handles=legend_elem_1, loc='upper center', ncol=2, bbox_to_anchor=(0.475, 1.1), fontsize=12)
    #ax.add_artist(legend1)
    plt.savefig("core_time_ratio.pdf", bbox_inches='tight')
    plt.savefig("core_time_ratio.png", bbox_inches='tight')