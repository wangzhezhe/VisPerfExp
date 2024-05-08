import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator

# refer to 
# https://stackoverflow.com/questions/20407936/matplotlib-not-displaying-intersection-of-3d-planes-correctly

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.view_init(elev=10, azim=45)

# Make data.
X = np.arange(0, 1, 0.1)
Y = np.arange(0, 3, 0.1)
X, Y = np.meshgrid(X, Y)
Z1 = 1.1*(1+X)/(1+Y)
Z2 = 1.25*(1+X)/(1+Y)
Z3 = 1.5*(1+X)/(1+Y)

Z4 = np.ones_like(Z1)


# Plot the surface.
surf1 = ax.plot_surface(X, Y, Z1, cmap=cm.Blues,
                       linewidth=0, antialiased=False)

surf2 = ax.plot_surface(X, Y, Z2, cmap=cm.Greens,
                       linewidth=0, antialiased=False)

surf3 = ax.plot_surface(X, Y, Z3, cmap=cm.Oranges,
                       linewidth=0, antialiased=False)

surf4 = ax.plot_surface(X, Y, Z4, cmap=cm.Purples,
                       linewidth=0, antialiased=False, alpha=0.5)

# Customize the z axis.
ax.set_zlim(0, 2)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
#fig.colorbar(surf, shrink=0.5, aspect=5)

plt.savefig("in-situ-cost-3d_plot.png", bbox_inches='tight')
