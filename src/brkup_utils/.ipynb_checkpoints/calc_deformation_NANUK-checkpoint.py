## Calculate deformation from neXtSIM moorings

"""
Created on Fri Apr 21 2023
@authors: Jonathan Rheinlænder
"""

import numpy as np
import datetime
import metpy.calc as mpcalc
from metpy.units import units

#########################################################
def calc_deformation_rate(uv, dx, dy, dt=24*60*60, x_dim=-1, y_dim=-2):
    '''
    Parameters:
    -----------
    uv : list of u and v components of winds with dims (time,y,x) 
    dx : spacing in x-direction (columns). Can be array or scalar
    dy: spacing in y-direction (rows). Can be array or scalar
    dt: time conversion, e.g. from sec to day 
    x_dim (int, optional) – Axis number of x dimension. Defaults to -1 (implying […, Y, X] order).
    y_dim (int, optional) – Axis number of y dimension. Defaults to -2 (implying […, Y, X] order).
    
    Returns:
    --------
    shear, divergence and total deformation. Dimensions: (time, y, x)
    '''
    # check if 'dx' has same dims as 'uv'  
    ndims = uv[0].ndim
    
    if hasattr(dx, "__len__"):    
        if dx.ndim < ndims:
            print('adding new dimension')
            # add new singleton dimension
            dx = dx[np.newaxis]
            
    if hasattr(dy, "__len__"):    
        if dy.ndim < ndims:
            print('adding new dimension')
            # add new singleton dimension        
            dy = dy[np.newaxis]

    u = uv[0]
    v = uv[1]
    
    # calculate gradient using interpolation (np.gradient)
    # axis=1 is rows (y) axis=2 is columns 
    du_rows, du_cols = np.gradient(u, axis=(y_dim,x_dim))
    dv_rows, dv_cols = np.gradient(v, axis=(y_dim,x_dim))

    # divide by spacing in x and y direction
    dudx = du_cols / dx # [1/s ==> 1/d]
    dudy = du_rows / dy 
    dvdy = dv_rows / dy
    dvdx = dv_cols / dx
    
    div = dt*(dudx + dvdy)
    shear = dt*np.hypot(dudx - dvdy, dudy + dvdx)   
    deform = np.hypot(div, shear)
             
    return shear, div, deform


def calc_deformation_rate_Metpy(u, v, dx, dy, dt=24*60*60):
    '''
    Using MetPy.gradient to calculate deformation
    
    Parameters:
    -----------
    uv : list
        uv = [u, v] with u, v x/y or lon/lat components of wind/ice velocity
    res: resolution of moorings
    dt: time conversion from sec to day    
        
    '''
    u = u * units.meter_per_second
    v = v * units.meter_per_second
    dx = dx[:,0:-1] * units.meter
    dy = dy[0:-1] * units.meter
    
    # NB: deltas should be one item less than the size of input data along the applicable axis. Here I remove the last point 
    
    # [1/s ==> 1/d]
    u_y, u_x = mpcalc.gradient(u, deltas=(dy, dx)) 
    v_y, v_x = mpcalc.gradient(v, deltas=(dy, dx))
    
    div = dt*(u_x + v_y)
    shear = dt*np.hypot(u_x - v_y, u_y + v_x)   
    deform = dt*np.hypot(div, shear)
             
    return shear, div, deform

