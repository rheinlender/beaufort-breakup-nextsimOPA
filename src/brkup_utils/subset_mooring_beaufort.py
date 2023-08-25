"""
Created on Mon Nov 15 2021
@authors: Jonathan Rheinlænder
"""
# read moorings 
import xarray as xr
import numpy as np
import process_data

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
years = list(range(1995, 2019))

ds =  process_data.subset_data_dailyMean(months, years, region='Beaufort')

#print('save to netcdf')
# save to netcdf
#ds.load().to_netcdf('moorings_daily_1995-2018_beaufort.nc')



