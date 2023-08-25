## Process data
"""
Created on Fri Nov 12 2021
@authors: Jonathan Rheinlænder
"""

import xarray as xr
import numpy as np
from brkup_utils.boxnames import *

#########################################################
#class LoadDataset():
    
def load_moorings(indir, months, years, region=None, period=None):
    """
    Parameters:
    -----------
    indir : (str) input directory
    months : list(float) 
    years : list(float)
    region : (str) region to subset from BOXNAMES 
    period : pandas.datetime offset alias (str) 
        period to average over, e.g. 'D' (daily)

    Returns:
    --------
    sel: boolean mask (0=not a lead or 1=lead)
    leadfrac: fraction of the grid cell characterized as a lead
    """
    
    # CHECK INPUT DATA    
    if not months:
        print("months is not defined...using all months")
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    else:
        print("months:", months)

    if not years:
        print("years is not defined...using all years")
        years = np.array(range(1995, 2019))
    else:
        print("years:", years)

    ###### READ NEXTSIM DATA
    files = [f"{indir}/{year}/nextsim/Moorings_{year}m{month}.nc" for year in years for month in months]

    ds=xr.open_mfdataset(files, concat_dim="time", combine="nested",
                      data_vars='minimal', coords='minimal', compat='override')

    ##### SUBSET REGION
    if region is not None:
        ds = subset_data_region(ds, region)

    ##### average in time
    if period is not None:
        
        if period=='daily':
            ds = daily_average(ds, period)
        else:
            ds = time_average(ds, period)

    print('DONE!')

    return ds

def subset_data_region(ds, region=None):

    if region is None: # if region is not defined
        region = 'Large_Arctic'

    print("bbox for", region, ':', BOXNAMES[region])

    [x1, x2, y1, y2] = BOXNAMES[region]

    sel = ds.sel(x=slice(x1, x2), y=slice(y1, y2))
    return sel

def time_average(ds, period):
    print('calculating time average')
    sel = ds.resample(time=period).mean(dim='time')
    return sel

def daily_average(ds, period):
    print('calculating daily average')
    # set all dates to have time at 00h so multiple measurements in a day have the same label
    ds.coords['time'] = ds.time.dt.floor('1D')
    sel = ds.groupby('time').mean()
    return sel


def monthly_mean_by_year(ds):
    
    """
    Calculates average of xarray.dataset or xarray.dataarray over each year and month using multi-indexing
    """
    
    import pandas as pd

    year_month_idx = pd.MultiIndex.from_arrays([np.array(ds['time.year']), 
                                                np.array(ds['time.month'])])
    # add year_month to coordinates
    ds.coords['year_month'] = ('time', year_month_idx)

    ds_monthly = ds.groupby('year_month').mean()
    
    return ds_monthly
