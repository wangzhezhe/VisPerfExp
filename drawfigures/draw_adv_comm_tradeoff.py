import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import numpy as np

gblue = '#4486F4'
gred = '#DA483B'
gyellow = '#FFC718'
ggreen = '#1CA45C'

customize_red='#F0B3B4'
customize_blue='#2077B4'

labelSize = 16
tickSize=16

if __name__ == "__main__":
    # typical bar example
    fig, ax = plt.subplots(figsize=(7,4.5))

    # set titles
    
    ax.set_xlabel('Number of recievers for the Supernova data set', fontsize=labelSize)
    ax.set_ylabel('Time(ms)', fontsize=labelSize)

    ax.set_ylim([0,110500])

    # set tick
    N = 3
    ind = np.arange(3)    # the x locations for the groups
    width = 0.5     # the width of the bars
    ax.set_xticks(ind )
    ax.set_xticklabels(('64','256','1024'), fontsize=tickSize)

    # set the value of the figure here
    # use the capsize to control the error bar
    accAdv = np.array([21867.66667,39941.33333,50688])
    p1 = ax.bar(ind, accAdv,  width, facecolor=customize_blue, edgecolor='None')

    accWait = np.array([59937.66667,31549.33333,15368])
    checkStd = ()
    p2 = ax.bar(ind , accWait, width, facecolor=customize_red, bottom=accAdv, edgecolor='None')

    anaMeans = np.array([14075.39533,23840.66667,31529])
    anaStd = ()
    p3 = ax.bar(ind , anaMeans,  width, facecolor='tab:gray', bottom=accAdv+accWait, alpha=0.25, edgecolor='None')

    ax.set_axisbelow(True)

    # add the lengend for the data by defualt
    ax.legend((p1[0], p2[0], p3[0]), ('Advection', 'Communication & wait', 'Other'), fontsize='large', ncol=3, loc='upper center' )
    
    #The following code shows how to customize the legend manually based on capability of Patch
    #legend_elem_1 = [Patch(facecolor='#B4E1FF', edgecolor='black', label='label1'),
    #                 Patch(facecolor='#AB87FF', edgecolor='black', label='label2')]
    #legend1 = plt.legend(handles=legend_elem_1, loc='upper center', ncol=2, bbox_to_anchor=(0.475, 1.0), fontsize=12)
    #ax.add_artist(legend1)
    
    plt.savefig("SupernovaChangeRecvs.png",bbox_inches='tight')
    plt.savefig("SupernovaChangeRecvs.pdf",bbox_inches='tight')