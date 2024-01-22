"""
Kernel Density Estimation functionality
"""

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from scipy import stats
from matplotlib.colors import ListedColormap


# Color map for density plots
def get_my_cmap(cmap='CMRmap'):
    cmap = plt.get_cmap(cmap)
    my_cmap = cmap(np.arange(cmap.N))
    my_cmap[:, -1] = np.linspace(0, 1, cmap.N)
    my_cmap = ListedColormap(my_cmap)
    return my_cmap


def kernel_density(lats, longs, projection, k, extend):
    geo = ccrs.Geodetic()

    h = projection.transform_points(geo, lats, longs)[:, :2].T

    kde = stats.gaussian_kde(h)

    # Coordinates of the four corners of the map.
    x0, x1, y0, y1 = extend
    # Create the grid.
    tx, ty = np.meshgrid(np.linspace(x0, x1, 2 * k),
                        np.linspace(y0, y1, k))
    # Reshape the grid for the kde() function.
    mesh = np.vstack((tx.ravel(), ty.ravel()))
    # Evaluate the kde() function on the grid.
    v = kde(mesh).reshape((k, 2 * k))
    # output is reshaped to grid mesh shape
    
    return v
