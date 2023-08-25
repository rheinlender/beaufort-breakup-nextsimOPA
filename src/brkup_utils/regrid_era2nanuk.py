"""
Created on Fri Sep 16 2022
@authors: Jonathan Rheinlænder
"""

from netCDF4 import Dataset
import numpy as np
from scipy.interpolate import RectBivariateSpline
import datetime as dt
import xarray as xr
from openerEra5 import OpenerEra5

def regrid_era2nanuk(era_file, mooring_file, dates=None):    
    """
    
    Regrid ERA5 atmospheric data on regular lat/lon grid to NANUK irregular grid (ORCA tripolar)
    The function uses 'RectBivariateSpline' to interpolate the ERA5 variable to NANUK grid. 
    
    Parameters:
    -----------
    era_file : (str)
    mooring_file : str
    dates: (str) e.g. '2000-01-01'
       can be used to subset the ERA5 data
        
    Returns:
    --------
    ds_m : xarray.Dataset
    
        Interpolated variable (time, lat, lon) or (lat, lon).         Same shape as mooring data.
    
    """
    
    
    # get model lat-lon
    with Dataset(mooring_file) as ds:
        lon_m = ds['longitude'][:]
        lat_m = ds['latitude'][:]

    lon_m[lon_m < 0] += 360 # shift longitude to go from 0-->360 

    
    # get era5 variable with Xarray    
    ds = xr.open_dataset(era_file)
    
    # subset data
    if dates is not None:
        ds = ds.sel(time = slice(dates[0],dates[1]), drop=True)
    
    # get time 
    time = ds.time.data
    
    # get variable name
    for varname in ds.data_vars:
        var_e = ds[varname][:,::-1]

    # get era5 lat/lon
    lat_e = ds.latitude.values
    lon_e = ds.longitude.values
    lat_e = lat_e[::-1] # make sure latitude is increasing  

    #print(var_e.shape)
    
    # Interpolating ERA5 using RectBivariateSpline
    var_m = np.empty((var_e.shape[0], lon_m.shape[0], lon_m.shape[1])) # initialize
    
    for t in range(var_e.shape[0]): # loop over time dim
        
        s = RectBivariateSpline(lat_e, lon_e, var_e[t], kx=1, ky=1)

        var_m_flat = s(lat_m.flatten(), lon_m.flatten(), grid=False)
        var_m[t::] = np.reshape(var_m_flat, lon_m.shape)
    
    ################ convert to dataset ##################
    
    # define coordinates
    coords = {'time': (['time'], time),
              'longitude': (['y','x'], lon_m.data), 
              'latitude': (['y','x'], lat_m.data),
             }

    # define data variables 
    data_vars={varname:(( "time", "y","x"), var_m)           
                   } 

    # new dataset
    ds_m = xr.Dataset(
        coords=coords,   
        data_vars=data_vars, 
    )

    return ds_m