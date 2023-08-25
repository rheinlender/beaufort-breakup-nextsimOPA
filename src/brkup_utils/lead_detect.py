## Lead detection
"""
Created on Tue Dec 07 2021
@authors: Jonathan Rheinlænder
"""

import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
import cmocean

#########################################################

# create functions for mapping leads 

def map_leads(ds, case_name, clim):
    """
    Parameters:
    -----------
    ds : xarray.DataSet
    case_name : str
    clim: int
        cut-off value 
        
    Returns:
    --------
    leadmask: boolean mask (0=not a lead or 1=lead)
    leadfrac: fraction of the grid cell characterized as a lead
    """
    #  set default cutoff value
    if clim is None:
        clim=0.05 
    else:
        clim=clim
            
    if (case_name == "breakup_paper"):
        owfraction = 1 - ds['sic']
        leadfrac = owfraction + ds['sic_thin']
        leadmask = xr.where(leadfrac>clim, 1, 0)
     
    elif (case_name=="Olason2021"):    
        owfraction = 1 - ds['sic']
        sic_thin = ds['sic_thin']
        hthin = ds['sit_thin']/sic_thin # slab ice thickness
        hthin = hthin.where(sic_thin>0, other=0) # slab thickness is zero if sic_thin is also zero
        sic_thin = sic_thin.where(hthin<=0.1, other=0) # exclude ice that is thicker than 10 cm

        leadfrac = owfraction + sic_thin
#        clim = 0.01 # when thin_ice_conc is larger than 1%
        leadmask = xr.where(leadfrac>clim, 1, 0)

    elif (case_name=="Willmes2019"):
        # Thin-ice thickness (TIT) threshold: TIT ≤ 0.2
        hthin = ds['sit_thin']/ds['sic_thin'] # slab ice thickness
        leadfrac = hthin.where(hthin<=0.2, other=0) # exclude ice that is thicker than 20 cm
        leadmask = xr.where(leadfrac>clim, 1, 0)
        
    elif (case_name=="Martin2004"):
        # Thin-ice thickness (TIT) threshold: TIT ≤ 0.1
        hthin = ds['sit_thin']/ds['sic_thin'] # slab ice thickness
        leadfrac = hthin.where(hthin<0.1, other=0)
        leadmask = xr.where(leadfrac>0, 1, 0)
     
    elif (case_name=="open-water"):
        
        if clim is None:
            clim=0.1
        
        owfraction = 1 - ds['sic']
        leadfrac = owfraction
        
        leadmask = xr.where(leadfrac>=clim, 1, 0)
    
    elif (case_name=="frazil-formation"):
        # find locations where there is non-zero newice production
        frazil = ds['newice']
        leadfrac = []
        leadmap = xr.where(frazil>0, 1, 0)
    
    # apply land mask
    landmask = ds['sit'].where(ds['sit'].isnull(), other =1)

    leadmask = leadmask.where(landmask==1)
    
    return leadfrac, leadmask