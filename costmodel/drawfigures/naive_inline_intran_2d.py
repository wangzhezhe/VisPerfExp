import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

gblue = '#4486F4'
gred = '#DA483B'
gyellow = '#FFC718'
ggreen = '#1CA45C'
slightred = '#F00285'
deepblue= '#58508d'
purple='#AB6EC4'
orange='#F7710A'

def tran_2():
    arr = [
        [-51,-51,-51,-51,-51,-51,-51,-51,-51,-51],
        [-51,-2,-2,-2,-2,-2,-2,-2,-2,-2],
        [-51,-2,47,47,47,47,47,47,47,47],
        [-51,-2,47,96,96,96,96,96,96,96],
        [-51,-2,47,96,145,145,145,145,145,145],
        [-51,-2,47,98,145,194,194,194,194,194],
        [-51,-2,47,96,145,194,243,243,243,243],
        [-51,-2,47,96,145,194,243,292,292,292],
        [-51,-2,47,96,145,194,243,292,341,341],
        [-51,-2,47,96,145,194,243,292,341,390]
    ]

    fig, ax = plt.subplots(figsize=(6.0,6.0))
    im=plt.imshow(arr,cmap='viridis_r',vmin=-150, vmax=400)



    ax.set_ylabel('Ana/Vis exec time',  fontsize=18)
    ax.set_xlabel('Sim exec time', fontsize=18)
    
    offset = 0.06
    dist = 1
    xindex=[]
    for i in range (0,10):
        xindex.append(offset+i*dist)

    print(xindex)

    ax.set_xticks(xindex)

    x_labels = [1,2,3,4,5,6,7,8,9,10] 
    ax.set_xticklabels(x_labels)


    offset = 0.1
    dist = 1
    yindex=[]
    for i in range (0,10):
        yindex.append(offset+i*dist)

    print(yindex)

    ax.set_yticks(yindex)

    y_labels = [1,2,3,4,5,6,7,8,9,10] 
    ax.set_yticklabels(y_labels)



    divider = make_axes_locatable(ax)
    cax = divider.append_axes('top', size='2%', pad=0.25)

    fig.colorbar(im, cax=cax, orientation="horizontal")
    plt.savefig("naive_inline_intran_tran2_2d.png", bbox_inches='tight')
    plt.savefig("naive_inline_intran_tran2_2d.pdf", bbox_inches='tight')

def tran_4():
    arr = [
        [-151,-151,-151,-151,-151,-151,-151,-151,-151,-151],
        [-151,-102,-102,-102,-102,-102,-102,-102,-102,-102],
        [-151,-102,-53,-53,-53,-50,-53,-53,-53,-53],
        [-151,-102,-53,-4,-4,-4,-4,-4,-4,2],
        [-151,-102,-53,-4,45,45,45,45,45,45],
        [-151,-102,-53,-4,45,94,94,94,94,94],
        [-151,-102,-53,-4,45,94,143,143,143,143],
        [-151,-102,-53,-4,45,94,143,192,192,192],
        [-151,-102,-53,-4,45,94,143,192,241,241],
        [-151,-102,-53,-4,45,94,143,192,241,290]
    ]

    fig, ax = plt.subplots(figsize=(6.0,6.0))
    im=plt.imshow(arr,cmap='viridis_r',vmin=-150, vmax=400)



    ax.set_ylabel('Ana/Vis exec time',  fontsize=18)
    ax.set_xlabel('Sim exec time', fontsize=18)
    
    offset = 0.06
    dist = 1
    xindex=[]
    for i in range (0,10):
        xindex.append(offset+i*dist)

    print(xindex)

    ax.set_xticks(xindex)

    x_labels = [1,2,3,4,5,6,7,8,9,10] 
    ax.set_xticklabels(x_labels)


    offset = 0.1
    dist = 1
    yindex=[]
    for i in range (0,10):
        yindex.append(offset+i*dist)

    print(yindex)

    ax.set_yticks(yindex)

    y_labels = [1,2,3,4,5,6,7,8,9,10] 
    ax.set_yticklabels(y_labels)



    divider = make_axes_locatable(ax)
    cax = divider.append_axes('top', size='2%', pad=0.25)

    fig.colorbar(im, cax=cax, orientation="horizontal")
    plt.savefig("naive_inline_intran_tran4_2d.png", bbox_inches='tight')
    plt.savefig("naive_inline_intran_tran4_2d.pdf", bbox_inches='tight')

def concrete_inline_intran():
    
    fig, ax = plt.subplots(figsize=(8,4.6))
    ax.set_xlabel('Ana/Vis execution time', fontsize='large')
    ax.set_ylabel('Workflow execution time', fontsize='large')  

    # set tick
    offset = 0
    dist=1
    xindex=[]
    for i in range (0,10):
        xindex.append(offset+i*dist)
    ax.set_xticks(xindex)
    ax.set_xticklabels(('1','2','3','4','5','6','7','8','9','10'), fontsize='large')

    sim6_tightly=(350,400,450,500,550,600,650,700,750,800)
    pal=ax.plot(sim6_tightly, color=gblue, linestyle='-', label="sim6_tightly")
    
    sim6_loosely_tran2=(401,402,403,404,405,406,456,506,553,606)
    pal=ax.plot(sim6_loosely_tran2, color=gred, linestyle='-', label="sim6_loosely_tran2")

    sim6_loosely_tran4=(501,502,503,504,505,506,556,606,656,706)
    pal=ax.plot(sim6_loosely_tran4, color=gred, linestyle='--', label="sim6_loosely_tran4")

    legend = ax.legend(loc='upper right', ncol=1, bbox_to_anchor=(0.50, 1.0), fontsize=16)

    plt.savefig("concrete_inline_intran.png", bbox_inches='tight')
    plt.savefig("concrete_inline_intran.pdf", bbox_inches='tight')


if __name__ == "__main__":
    #tran_2()
    #tran_4()
    concrete_inline_intran()
