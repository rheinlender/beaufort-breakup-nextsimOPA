## Estimate ice growth from nextsim Moorings

"""
Created on Mon Dec 06 2021
@authors: Jonathan Rheinlænder
"""

import xarray as xr
import numpy as np
#import pandas as pd

#########################################################
class IceGrowth:
    
    def __init__(self, dataset):
        
        self.dataset = dataset
        self.variables = ['newice', 'del_vi_thin', 'del_hi']
        return
        
    def fix_growthrate(self):

        '''
        Get the growth rate pr. unit output freq (i.e. 6 hrs)

        NB! in the NANUK output the 'newice' and 'del_vi_thin' are in units "volume", 
        i.e. the slab-thickness has already been multiplied by the area fraction. 
        '''

        # get freq from mooring
        dt_in_hours = self.dataset.time.dt.hour[1] - self.dataset.time.dt.hour[0]
        output_timestep = dt_in_hours.values/24 
        output_freq = 1/output_timestep

        print("output frequency ", output_freq)

        # apply to growth rate variables
        for var in self.variables:
            print(var)
            self.dataset[var] = self.dataset[var]/output_freq

            if var=='del_hi': # fix units
                self.dataset['del_vi'] = self.dataset['del_hi']*(self.dataset['sic'] - self.dataset['sic_thin'])      
        return

    def calc_vol_growth(self, mask):
        '''
        Calculates the ice volume growth from nextsim moorings

            Parameters:
                ds (xr.Dataset): Xarray dataset 
                mask (boolean): region mask (1 or 0)

            Returns:
                delVsum (xr.Dataset): Total ice volume growth (m3/output_freq) 

        '''
        area = self.dataset['mod_area']    
        
        # update variable list
        if self.variables == ['newice', 'del_vi_thin', 'del_hi']:
            self.variables = ['newice', 'del_vi_thin', 'del_vi'] 
        
        delVsum=xr.Dataset()
        for var in self.variables:
              
            # convert to volume growth
            delV = area*self.dataset[var] # in m3/?hrs

            # apply mask
            mask = mask*(~np.isnan(self.dataset['sic'][0])) # remove nans
            delVmsk = delV.where(mask==1)

            delVsum[var] = delVmsk.sum(dim=("x", "y"), skipna=True) # m3/?hrs total volume growth
            
            # fix attributes 
            delVsum[var].attrs = {'units':'m2'}
            
        return  delVsum

    def get_total_growth(self, dVol):
        '''
        Calculates the total amount of ice volume growth
            Parameters:
                dVol (xr.DataArray): ice growth 

            Returns:
                total_growth (dict):  Cumulative ice volume growth (m3) 
        '''

        # group by year
        yearly = dVol.groupby('time.year')

        total_growth = {}
        for var in self.variables:
            csum=[]
            for year, darr in yearly:
                # cumulative sum
                csum.append(darr[var].cumsum(axis=0).values[-1])

            total_growth[var] = np.array(np.float32(csum))    
        return total_growth