# refer to https://github.com/jollybao/LCS/blob/master/src/double_gyre.py
# refer to https://shaddenlab.berkeley.edu/uploads/LCS-tutorial/examples.html

# define necessary parameter values

# compute the velocity through the x y position
# domain x is [0,2], y is [0,1]


import numpy as np
import pylab as plt
import matplotlib.animation as animation

fig, ax = plt.subplots(1,1,figsize=(10,5))

# Initialized parameters
pi = np.pi
A = 0.1
epsilon = 0.25
w = pi/10
delta = 0.0001
dt = 0.1
dimx=20
dimy=10

#N = int(input("Enter number of particles: "))
N = 2
col = ['r','y','b','g','k','c','m','r','y','b',
       'g','k','c','m','r','y','b','g','k','c','m',
       'r','y','b','g','k','c','m']

def phi(x,y,t):
    f_phi = A*np.sin(pi*f(x,t))*np.sin(pi*y)
    return f_phi

def f(x,t):
    at = epsilon*np.sin(w*t)
    bt = 1-2*epsilon*np.sin(w*t)
    return at*x**2+bt*x

def velocity(x,y,t):
    # the input for x and y is matrix
    # this operation do matrix operation for each input point
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
Vx,Vy = velocity(X,Y,0.1)

# vector arrows
Q = ax.quiver(X,Y,Vx,Vy,scale=10)

# initialize array of particles
C = np.empty([N],plt.Circle)
# initialize different color of the particle
for i in range(0,N):
    C[i] = plt.Circle((-1,-1),radius = 0.03, fc = col[i])
    
R = np.empty([N,2],float)
R[0][0]=0.5
R[0][1]=0.5
R[1][0]=1.5
R[1][1]=0.5
C[0].center = (R[0][0],R[0][1])
ax.add_patch(C[0])
C[1].center = (R[1][0],R[1][1])
ax.add_patch(C[1])

# for i in range(0,N):
#     print("Enter x and y coordinates of the circle ",i+1)
#     R[i][0] = float(input())
#     R[i][1] = float(input())
#     C[i].center = (R[i][0],R[i][1])
#     ax.add_patch(C[i])
    

# animation for particle moving along the vector field
def animate(num,Q,X,Y,C,R,N):
    #print("num is", num)
    t = num/1
    dt = 1/10
    Vx,Vy = velocity(X,Y,t)
    Q.set_UVC(Vx,Vy)  
    
	# update particles' positions
    for i in range(0,N):
        for j in range(0,10):
            r = R[i][:]
            k1 = dt*update(r,t)
            k2 = dt*update(r+0.5*k1,t+0.5*dt)
            k3 = dt*update(r+0.5*k2,t+0.5*dt)
            k4 = dt*update(r+k3,t+dt)
            R[i][:] += (k1+2*k2+2*k3+k4)/6
    
        C[i].center = (R[i][0],R[i][1])
    return Q,C

ani = animation.FuncAnimation(fig, animate,
         fargs=(Q,X,Y,C,R,N),
    interval=100,blit=False,save_count=100)

FFwriter = animation.FFMpegWriter(fps=10)
ani.save('VF_demo.mp4',writer = FFwriter)

#plt.show()