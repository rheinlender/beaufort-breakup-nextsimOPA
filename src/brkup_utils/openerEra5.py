"""
Opener function for ERA5

Created on Thu Dec 09 2021
@authors: Jonathan Rheinlænder
"""

# Load modules
from netCDF4 import Dataset
from string import Template
from pynextsim.openers import OpenerVariable, Opener
from pynextsim.gmshlib import GmshMesh
import os

# set environment
os.environ['INPUT_OBS_DATA_DIR'] = '/home/rheinlender/shared-simstore-ns9829k/data/'

class OpenerEra5(Opener):

    name = 'ERA5'
    name_mask = Template('ERA5/daily/ERA5_${varname}_y%Y_daily.nc')
    varname = 'Atm. forcing'
    variables = dict()
    averaging_period = 0 # snapshots

    def __init__(self, varname):
        self.name_mask = self.name_mask.safe_substitute(dict(varname=varname))
        self.varname = varname
        self.variables = {
                varname : OpenerVariable(varname), #can set any scale and offset here
                }
        
        
    def get_lonlat(file):
        
        with Dataset(file) as ds:
        
            lon = ds['longitude'][:]
            lat = ds['latitude'][:]

        return lon, lat    