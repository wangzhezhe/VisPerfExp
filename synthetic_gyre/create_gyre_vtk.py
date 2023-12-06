

# refer to https://github.com/jollybao/LCS/blob/master/src/double_gyre.py
# refer to https://shaddenlab.berkeley.edu/uploads/LCS-tutorial/examples.html

# define necessary parameter values


# compute the velocity through the x y position
# domain x is [0,2], y is [0,1]


import numpy as np
import pylab as plt
import matplotlib.animation as animation
import vtk as vtk
from vtk.util import numpy_support
from vtkmodules.vtkCommonDataModel import vtkStructuredPoints


fig, ax = plt.subplots(1,1,figsize=(10,5))

# Initialized parameters
pi = np.pi
A = 0.1
epsilon = 0.25
w = pi/15
delta = 0.0001
dt = 0.1
dimx=20
dimy=10

def writeDS(fname, ds) :
    writer = vtk.vtkDataSetWriter()
    writer.SetFileTypeToBinary()
    writer.SetFileName(fname)
    writer.SetInputData(ds)
    writer.Update()
    writer.Write()

def phi(x,y,t):
    f_phi = A*np.sin(pi*f(x,t))*np.sin(pi*y)
    return f_phi

def f(x,t):
    at = epsilon*np.sin(w*t)
    bt = 1-2*epsilon*np.sin(w*t)
    return at*x**2+bt*x

def compute_velocity(x,y,t):
    vx = (phi(x,y+delta,t)-phi(x,y-delta,t))/(2*delta)
    vy = (phi(x-delta,y,t)-phi(x+delta,y,t))/(2*delta)
    return -1.0*vx,-1.0*vy

# function that computes velocity of particle at each point
def update(r,t):
    x = r[0]
    y = r[1]
    vx = (phi(x,y+delta,t)-phi(x,y-delta,t))/(2*delta)
    vy = (phi(x-delta,y,t)-phi(x+delta,y,t))/(2*delta)
    return np.array([-1*vx,-1*vy],float)

# make a 2D mesh grid of size 40*20
xrange=[0,2]
yrange=[0,1]
X,Y = plt.meshgrid(np.arange(xrange[0],xrange[1],(xrange[1]-xrange[0])/dimx),np.arange(yrange[0],yrange[1],(yrange[1]-yrange[0])/dimy))

def simulate(step):
    t=step
    dt=1.0/10.0
    Vx,Vy = compute_velocity(X,Y,t)
    # the Vx and Vy is the velocity at each point
    # compose them into vector
    nr,nc = np.shape(Vx) # 10*20 
    # print("step",step,nr,nc)
    # bottom left is 0,0
    velocity_list=[]
    for y in range(0,nr,1):
        for x in range(0,nc,1):
            # for vx and vy, the first dim is row
            velocity=(Vx[y][x],Vy[y][x],0.0)
            velocity_list.append(velocity)
    #print(Vx)
    #print(Vy)
    #print(velocity_list)
    velocity_numpy = np.array(velocity_list)
    vtkarray = numpy_support.numpy_to_vtk(velocity_numpy)
    vtkarray.SetName("velocity")

    # output the results into vtk file
    xdim=dimx
    ydim=dimy
    zdim=1
    structured_dataset = vtkStructuredPoints()
    structured_dataset.SetDimensions(xdim, ydim, zdim)
    structured_dataset.SetOrigin(0, 0, 0)
    # n vertex in each dims contains n-1 cells
    structured_dataset.SetSpacing(2.0/(xdim-1), 1.0/(ydim-1), 1)


    structured_dataset.GetPointData().AddArray(vtkarray)
    structured_dataset.GetPointData().SetActiveScalars("velocity")
    
    file_name = "gyre_"+str(step)+".vtk"
    writeDS(file_name,structured_dataset)



total_steps=100
for step in range(0,total_steps,1):
    simulate(step)