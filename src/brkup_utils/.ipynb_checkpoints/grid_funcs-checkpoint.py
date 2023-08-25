"""
grid functions

Created on Thu Dec 09 2021
@authors: Jonathan Rheinlænder
"""

# Load modules
from netCDF4 import Dataset
from pynextsim.projection_info import ProjectionInfo
import os
import numpy as np
from brkup_utils.boxnames import *

def get_xy(nlon, nlat):
    """
    
    Get x and y coordinates from nextsim grid
    
    Parameters:
    -----------
    nlon : 2d array in longitude coordinates
    nlat : 2d array in latitude coordinates
        
    Returns:
    --------
    x, y: x and y array for grid
    """
    
    proj = ProjectionInfo() # default projection for nextsim
    x,y = proj.pyproj(nlon, nlat)
    
    return x, y

class CREGgrid:
    "Class for loading variables from the CREG grid"
    
    def __init__(self, grid_dir, bbox=None):
        """Initialize object from path
         Parameters:
        -----------
        grid_dir : path to grid files (str)
        
        bbox :  list(float)
            can use this to reduce the grid [xmin, xmax, ymin, ymax]  
        """
        
        grid_list = ['CREG025.L75_byte_mask.nc', 'CREG025.L75_mesh_hgr.nc', 'CREG025.L75_mesh_zgr.nc']       
        
        self.mod_grid_f, self.mod_hgr_f, self.mod_zgr_f = [os.path.join(
            grid_dir,ncf) for ncf in grid_list]
        
        self.bbox = bbox    
    
    #@staticmethod
    def get_var_from_netcdf(self, ncfil, varlist):
        """
        Parameters:
        -----------
        varlist : list(str) variable names
        
        Returns:
        --------
        var: (array) variables from netcdf file
        """
        #print(ncfil, varlist)
        
        with Dataset(ncfil) as nc:
            varout = [np.array(nc.variables[var]) for var in varlist]

            # reduce grid with bbox
            if self.bbox is not None: 
                varout = self.reduce_2dgrid(varout)

        return varout
    
    def reduce_2dgrid(self, varlist):
        """
        Apply boundary box 'bbox'
        
        Parameters:
        -----------
        varlist : list(array) variables
        
        Returns:
        --------
        varout: list(array) variables
        """
        [x0, x1, y0, y1] = self.bbox
        varout=[]
        for arr in varlist: # loop over varlist
            # apply bbox over last 2-dim (y,x)
            if arr.ndim==3:                
                varout.append(arr[:, y0:y1, x0:x1])
            elif arr.ndim==4:
                varout.append(arr[:, :, y0:y1, x0:x1])    
            else: varout.append(arr)
        return varout
    
    def get_area(self):
        """Returns grid cell area (in m2) for the CREG grid. Land is nan"""
        e1t, e2t = self.get_var_from_netcdf(self.mod_hgr_f, ['e1t', 'e2t'])
        tmask = self.get_var_from_netcdf(self.mod_grid_f, ['tmask'])[0]
        
        tmask = np.squeeze(tmask[0,0,:,:])
        e1t = np.squeeze(e1t[0,:])
        e2t = np.squeeze(e2t[0,:])

        mod_area = e1t*e2t
        
        # mask land
        mod_area[tmask==0] = np.nan
        
        return mod_area

    def get_depth(self):
        """Returns depth (in m) for the CREG grid"""
        
        mod_depth = self.get_var_from_netcdf(self.mod_zgr_f, ['gdept_1d'])
        mbathy = self.get_var_from_netcdf(self.mod_zgr_f, ['mbathy'])

        mod_depth = np.squeeze(mod_depth)
        mbathy = np.squeeze(mbathy)
        
        depth = np.zeros(np.shape(mbathy))
        for i in range(0,np.shape(depth)[0]):
            for j in range(0,np.shape(depth)[1]):
                depth[i,j] = mod_depth[mbathy[i,j]]
        return depth