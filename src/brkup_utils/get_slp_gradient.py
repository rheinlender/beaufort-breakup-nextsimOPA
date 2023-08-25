"""
Created on Fri Sep 16 2022
@authors: Jonathan Rheinlænder
"""

def get_slp_gradient(da, point0, point1):
    """
    
    Calculate difference in pressure between point0 and point1
    
    Parameters:
    -----------
    da : dataArray
    point0 : start point (longitude,latitude)
    point1 : end point (longitude,latitude)
        
    Returns:
    --------
    diff : dataArray
        difference between point0 and point1
    """
    
    print('start point:', (point0), '\n', 'end point:', (point1))
    
    # convert longitude from 0:360 to -180:180
    da.coords['longitude'] = (da.coords['longitude'] + 180) % 360 - 180
    da = da.sortby(da.longitude)

    end_point = da.sel(longitude=str(point1[0]),
                       latitude=str(point1[1]),
                       method="nearest")
    
    start_point = da.sel(longitude=str(point0[0]),
                         latitude=str(point0[1]),
                         method="nearest")
    
    diff = start_point - end_point

    return diff