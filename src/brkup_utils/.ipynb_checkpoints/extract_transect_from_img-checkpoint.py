"""
Created on Tue Sep 05 2022
@authors: Jonathan Rheinlænder
"""

import scipy.ndimage
import numpy as np

def extract_transect_from_img(xa, xy_pts, num, mode='nearest'):
    """
    Extract transect from image in x-y coordinates based on interpolation method ndimage.map_coordinates
    
    Parameters:
    -----------
    xa: xarray.DataArray
        array to plot
    xy_pts: tuple (x0,y0,x1,y1)
        start and end points in _pixel_ coordinates!!
    num: number of points to interpolate onto
    
    Returns:
    --------
    zi : Interpolated values along transect
    
    """
    # set all NaN's to zero. This is required for the interpolation method to work. Make sure that your points are not over land (=NaN). 
    z = xa.fillna(value=0)
    nt=z.shape[0]
    
    # zi = np.empty((nt, num))
    #-- Extract the line...
    # Make a line with "num" points...
    x0, y0 = xy_pts[0], xy_pts[1] # These are in _pixel_ coordinates!!
    x1, y1 = xy_pts[2], xy_pts[3]     
    x, y = np.linspace(x0, x1, num), np.linspace(y0, y1, num)

    # Extract the values along the line, using cubic interpolation
    zi = scipy.ndimage.map_coordinates(z.values, np.vstack((x,y)), mode=mode, output=z.dtype)

    return zi