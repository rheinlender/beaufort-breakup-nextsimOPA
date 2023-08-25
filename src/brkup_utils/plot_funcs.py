## Plotting funcs for nextsim data
"""
Created on Tue Dec 07 2021
@authors: Jonathan Rheinlænder
"""

import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.dates as mdates
import numpy as np
import datetime
import cmocean
import cartopy.crs as ccrs

#########################################################

def prepare_grid(ds, proj):

    # Get x-y grid from model
    lons = ds.longitude[:]
    lats = ds.latitude[:]
    x,y = proj.pyproj(lons.values, lats.values) # init grid using x,y coords of grid
    x_extent = [(x,y)[0][0][0], (x,y)[0][0][-1]]
    y_extent = [(x,y)[1][0][0], (x,y)[1][-1][0]]
    ex_lim=1
    x_extent = [(x,y)[0][0][ex_lim], (x,y)[0][0][-ex_lim]]
    y_extent = [(x,y)[1][ex_lim][0], (x,y)[1][-ex_lim][0]]

    grid = dict(
        x_extent=x_extent,
        y_extent=y_extent,
        )

    return grid

def plot_multipanel(xarr, axes, year, ylim=[0,1],
                    suptitle=None, ylabel=None, figsize=None):
    """
    Parameters:
    -----------
    array : xarray.DataArray
        array to plot
    axes: list
        [nrow, ncol]
    year : list
        [start_year, end_year]        
    **kwargs for plt.imshow()
    
    Returns:
    --------
    fig : matplotlib.figure.Figure
    ax : matplotlib.axes._subplots.AxesSubplot
    """
    if axes is None:
        fig = plt.figure(figsize=figsize)
        axes = fig.add_subplot(111)
    else:
        fig, axes = plt.subplots(nrows=axes[0], ncols=axes[1], figsize=(14,12))
        
    i=0
    for ax, year in zip(axes.flatten(), range(year[0],year[1])):
        
        xarr.sel(time=str(year)).plot.line(ax=ax, hue=str(year))
         
        # date formatting
        weeks = mdates.WeekdayLocator()
        months = mdates.MonthLocator(interval=1)  # every month
        dtFmt = mdates.DateFormatter('%b') # define the formatting 

        ax.set_xticklabels([])
        ax.set(xlabel=None, ylabel=None)    
        ax.set_ylim(ylim)
        ax.set_title(str(year), y=.8)  
        ax.grid(linestyle='--', alpha=0.4) 

        i+=1
    
    if axes.ndim > 1:
        for ax in axes[-1][:].flat: 
            # date formatting
            months = mdates.MonthLocator(interval=1)  # every month
            dtFmt = mdates.DateFormatter('%b') # define the formatting 

            ax.xaxis.set_major_formatter(dtFmt)
            ax.xaxis.set_major_locator(months)
    else: # if only 1by
        for ax in axes.flat: 
            ax.xaxis.set_major_formatter(dtFmt)
            ax.xaxis.set_major_locator(months)
        
    # set super title
    if suptitle is not None:
        plt.suptitle(suptitle)

    # check for empty axes
    if i < axes.size:
        for idax in range(i, axes.size):
            axes.flat[idax].set_visible(False) # to remove last plot
    
    # Common centered ylabel
    if ylabel is not None:    
        fig.add_subplot(111, frameon=False)
        plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
        plt.ylabel(ylabel)
        
    return fig, axes 


def plot_transect(ax, vname, add_insetmap=True):
    
    global clabel, figname, cmap, clim, cb_extend, zlev
    clabel, figname, cmap, clim, cb_extend, zlev = _PLOT_INFO[vname]
    
    print("Plotting transect", vname)
    
    if np.size(clim)==2: #contineous colormap 
        cf = ax.contourf(vtimes, yvals, transect.transpose(), 
        vmin=clim[0], vmax=clim[1], cmap=cmap, extend=cb_extend)
    else: #discrete colormap
        clevs = np.arange(clim[0], clim[1]+clim[2],clim[2])
        cf = ax.contourf(vtimes, yvals, transect.transpose(), 
            levels=clevs, cmap=cmap, extend=cb_extend)

    if zlev is not None:
        # add single contour line
        cline = ax.contour(vtimes, yvals, transect.transpose(), levels=zlev,  colors='k', linewidths=1)
    
    # add colorbar
    pos = ax.get_position() 
    cax = fig.add_axes([pos.xmax+.015, pos.y0, 0.01, pos.ymax-pos.y0 ])
    cbar=fig.colorbar(cf,cax=cax)
    cbar.set_label(clabel)
    ticks = clevs[::5]
    cbar.set_ticks(ticks)
    
    # set labels
    days = mdates.DayLocator()  # every day
    dtFmt = mdates.DateFormatter('%b %d') # define the formatting 
    ax.xaxis.set_major_formatter(dtFmt)
    ax.xaxis.set_minor_locator(days)

    # add map 
    if add_insetmap:
        proj = ccrs.NorthPolarStereo(central_longitude=-45)
        ax_inset = inset_axes(ax, height='50%', width='50%',
                              loc=3, bbox_to_anchor=(0,0,0.3,1), bbox_transform=ax.transAxes,
                              axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                              axes_kwargs=dict(map_projection=proj))
        plot_map(ax_inset) 


def plot_map(ax):

    lons = ds.longitude[:] #dims:y,x
    lats = ds.latitude[:]

    # find lon,lat coordinates for x,y points
    lon0 = lons[ypoint[0]][xpoint[0]]
    lon1 = lons[ypoint[1]][xpoint[1]]
    lat0 = lats[ypoint[0]][xpoint[0]]
    lat1 = lats[ypoint[1]][xpoint[1]]
    lon = (lon0, lon1)
    lat = (lat0, lat1)
    
    proj = ccrs.NorthPolarStereo(central_longitude=-45)
    ax.set_extent([-2611832.880671568, -369765.49428808136, -1058480.3928495955, 1951306.484993737], crs=ax.projection)
    
    ax.add_feature(cartopy.feature.LAND,zorder=1,alpha=1,color="lightgrey") 
    ax.coastlines(resolution='50m', linewidth=0.5) 
    ax.gridlines(draw_labels=False, linestyle='--', alpha=0.5,  linewidth=0.3)
    ax.plot(lon, lat, 'ro-',linewidth=1, markersize=3, transform=ccrs.Geodetic()) # geodetic plots shortest distance 

    
def polarCentral_set_latlim(lat_lims, ax):
    
    ax.set_extent([-180, 180, lat_lims[0], lat_lims[1]], ccrs.PlateCarree(central_longitude=-190))
    
    # Compute a circle in axes coordinates, which we can use as a boundary
    # for the map. We can pan/zoom as much as we like - the boundary will be
    # permanently circular.
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)

    ax.set_boundary(circle, transform=ax.transAxes)
