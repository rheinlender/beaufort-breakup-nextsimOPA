"""
Created on Wed Nov 03 2021
@authors: Jonathan Rheinlænder
Modified from Guillaume Boutin `/pytwin/gb_funcs.py`
"""

from pynextsim.projection_info import ProjectionInfo
from netCDF4 import Dataset, num2date, date2num
import numpy as np
import matplotlib.pyplot as plt
from brkup_utils.boxnames import *
from brkup_utils.grid_funcs import *

##########################################################
##########################################################
#### #### #### ####  MASKS AND BOXES  #### #### #### #### #### #### #### #### 
##########################################################
##########################################################
#####################
##########################################################
#### #### #### ####  MASKS AND BOXES  #### #### #### #### #### #### #### #### 
##########################################################
##########################################################

NANUK_GRIDDIR = '/home/rheinlender/shared-simstore-ns9829k/NANUK/NANUK025-I/'
NSIDC_GRIDDIR = '/home/rheinlender/Data/NSIDC/NSIDC_25km_grid.nc'

class Masking():
    
    def __init__(self, dataset, bbox=None):
        """
        Parameters:
        -----------
        dataset : xarray.DataSet 
        
        bbox :  list(float)
            can use this to reduce the grid [xmin, xmax, ymin, ymax]   
        """ 
        self.dataset=dataset  
        self.bbox=bbox
        self.check_latlon_2d()

    def check_latlon_2d(self):
        
        lon = self.dataset.longitude
        lat = self.dataset.latitude  
        shp = lon.shape
        
        if len(shp)>2:
            # Drop time dimension - lon lat should be 2D 
            self.dataset['longitude'] = lon.isel(time=0, drop=True)
            self.dataset['latitude'] = lat.isel(time=0, drop=True)
           
    def get_nsidc_mask(self, mask_name, depth=None):
        """
        Get mask from NSIDC
        
        Parameters:
        -----------
        
        mask_name : (str) 
            Name of NSIDC region to get mask for
        
        depth : int
            depth in meters e.g. to mask out shallow regions 
            
        Returns:         
        --------
        Dict("data":mask_box, "name":box_name)
       
       """ 
        
        # check that mask name exists in dictionary
        region = [value for value in NSIDC_region_dic.keys() if value in mask_name]
        if region:
            index_region=NSIDC_region_dic[region[0]]
        else:
            raise ValueError("Unknown region name:", mask_name)       
        
        # get x-y coordinates of nextsim grid
        x, y = get_xy(self.dataset.longitude, self.dataset.latitude)
    
        mask_box = self.calculate_mask(x,y,index_region)
        
        
        if depth is not None:
            mask_name = [mask_name +"_d"+str(depth)]# update name

            mask_box = self.mask_depth(mask_box, depth)        
    
        print('Getting mask for ', mask_name)
        
        return {"data":mask_box,"name":mask_name}
    
    def mask_depth(self, mask_box, depth):
        
        """Mask areas that are shallower than 'depth'"""
        
        # get model depth from CREG
        creg = CREGgrid(NANUK_GRIDDIR, self.bbox)
        mdepth = creg.get_depth()
        
        # check that dimensions fit
        if not(mask_box.shape==mdepth.shape):
            print(mask_box.shape, mdepth.shape)
            raise TypeError("Dimensions does not match!")
        else:
            mask_box[np.where(mdepth[:,:] < depth)]=0.     
            mask_box = mask_box.astype(bool) 
        
        return mask_box

    def calculate_mask(self, x, y, index_region):
        """
        Function that calculates the mask based on x and y coordinates of grid
        
        Parameters:
        -----------
        x : numpy.ndarray
            x array for grid
        y : numpy.ndarray
            y array for grid
        region_index : np.int
             select region based on its index
        
        Returns:         
        --------
        mask : boolean array
        """ 
        
        ####n  -> Choose the region you want to select with its index
        # The projection used by NSIDC
        map = ProjectionInfo.osisaf_nsidc_np_stere().pyproj
        #  The grid lon,lat and mask
        with Dataset(NSIDC_GRIDDIR, mode='r') as ncm:
            masks_nsidc = ncm["mask"][:]
            lon_nsidc   = ncm["lon"][:]
            lat_nsidc   = ncm["lat"][:]
            x_nsidc,y_nsidc= map(lon_nsidc,lat_nsidc)  

        # I want an array with 0s everywhere but within the region I am interested
        mask_nsidc=np.zeros(masks_nsidc.shape)
        mask_nsidc[masks_nsidc==index_region]=1

        # Project model lon, lat on the nsidc projection and get 1d vector out of them
        x=np.array(x) ; y=np.array(y)
        Nx     = x.size
        shp    = x.shape
        x_1d   = x.reshape(Nx)
        y_1d   = y.reshape(Nx)

        # use matplotlib to find the contour of region
        all_paths = plt.contour(x_nsidc,y_nsidc,mask_nsidc,[0.5]).collections[0].get_paths()
        plt.close()
        
        # look for the biggest contour : WARNING, I might forget some little bits by doing that, I haven't checked too carefully
        max_len=0
        for i in range(len(all_paths)):
            if len(all_paths[i])>max_len:
                max_len=len(all_paths[i])
                bbPath=all_paths[i]
        
        # select all the indexes that are within the (biggest) contour of my region
        coords = np.array([x_1d,y_1d]).transpose()
        mask_1d= np.array(bbPath.contains_points(coords),dtype=bool)
        
        # Back to 2d
        mask   = mask_1d.reshape(shp)
        
        return mask
    
    def get_large_Beaufort_mask(self):

        lat = self.dataset.latitude
        lon = self.dataset.longitude
        
        # get land/ocean mask from CREG
        creg = CREGgrid(NANUK_GRIDDIR, self.bbox)
        mod_area = creg.get_area()
        tmask = ~np.isnan(mod_area)  
        
        mask = 0*np.ones(lat.shape)
        mask[(lat<81)&(lat<81)&(lon<=-125)&(lon>-155)] = 1
        mask[tmask[:,:]==0] = 0 
        
        return mask
        
            
    def get_Moore2022_Beaufort_mask(self):

        lat = self.dataset.latitude
        lon = self.dataset.longitude
        
        # get land/ocean mask from CREG
        creg = CREGgrid(NANUK_GRIDDIR, self.bbox)
        mod_area = creg.get_area()
        tmask = ~np.isnan(mod_area)  
        
        mask = 0*np.ones(lat.shape)
        mask[(lat<78)&(lat>69)&(lon>-160)&(lon<-120)] = 1
        mask[tmask[:,:]==0] = 0
        
        return mask