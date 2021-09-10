#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autopep8: https://pypi.org/project/autopep8/
# Check with http://pep8online.com/

# Make different plot types

import proplot as plot
from variables import get_var_infos
from zones import get_zone


def plot_ref_new_obs(
    var, ref, new, obs, label, units,
    levels, cmap, extend,
    levels_diff, cmap_diff, extend_diff,
    levels_bias, cmap_bias, extend_bias,
    save=False, dpi=300
):
    """
        Plot 2 simulations versus observations. First row contains the 2
        simulations and their differences (diff). Second raw contains their
        bias regarding to observation and the observation itself.

        Parameters
        ----------
        var : str
            Variable name. Options are:

            - 'snc', 'frac_snow'
            - 'tas'
            - 'pr'

        label : str
            Name of the variable.

        units : str
            Units of the variables.

        ref, new, obs : DataArray
            Reference, new simulation and observation. The following attributes
            are needed:
                - 'title' for the name of the plots 
                - 'period' for the suptitle and saving the figure
                - 'season' for the suptitle and saving the figure
                - 'zone' for the suptitle and saving the figure

        levels, levels_diff, levels_bias : numpy.ndarray, optional
            Levels for the plots.

        cmap, cmap_diff, cmap_bias : colormap spec
            Colormaps for the plots.

        extend, extend_diff, extend_bias : numpy.ndarray
            Extends for the plots.

        save : bool, optional
            Save the figure or not. Default is None (does not save the figure).
            Save figures to jpg, png and pdf.

        dpi : int, optional
            DPI of the figure. Default is 300.

        Example
        -------
        >>> import xarray as xr
        >>> import proplot as plot
        >>> import sys
        >>> sys.path.insert(1, '/home/mlalande/notebooks/utils')
        >>> import utils as u
        >>>
        >>> period = slice('1979','2014')
        >>> var = 'snc'
        >>> label, units, cmap = u.get_var_infos('snc')
        >>>
        >>> ref = xr.open_dataarray(...); ref.attrs['title'] = ...
        >>> new = xr.open_dataarray(...); new.attrs['title'] = ...
        >>> obs = xr.open_dataarray(...); obs.attrs['title'] = ...
        >>>
        >>> clim_ref = u.clim(ref.sel(time=period))
        >>> clim_new = u.clim(ref.sel(time=period))
        >>> clim_obs = u.clim(ref.sel(time=period))
        >>>
        >>> levels = plot.arange(0,100,10)
        >>> extend = 'neither'
        >>>
        >>> levels_diff = plot.arange(-30,30,5)
        >>> cmap_diff = 'BuRd_r'
        >>> extend_diff = 'both'
        >>>
        >>> levels_bias = plot.arange(-100,100,20)
        >>> cmap_bias = 'BuRd_r'
        >>> extend_bias = 'neither'
        >>>
        >>> u.plot_ref_new_obs(
                var, clim_ref, clim_new, clim_obs, label, units,
                levels, cmap, extend,
                levels_diff, cmap_diff, extend_diff,
                levels_bias, cmap_bias, extend_bias,
                save=False, dpi=300
            )


    """
    
    # Change orientation for some zones
    if ref.attrs['zone'] not in ['NH']:
        axwidth = 2.5
        ncols = 3; nrows = 2; cbar_loc = 'r'
        i_ref = 0; i_new = 1; i_diff = 2
        i_ref_bias = 3; i_new_bias = 4; i_obs = 5
    else:
        axwidth = 4.5
        ncols = 2; nrows = 3; cbar_loc = 'b'
        i_ref = 0; i_new = 2; i_diff = 4
        i_ref_bias = 1; i_new_bias = 3; i_obs = 5
    
    
    fig, axs = plot.subplots(proj='cyl', ncols=ncols, nrows=nrows, 
                             axwidth=axwidth)

    # Reference simulation
    m0 = axs[i_ref].pcolormesh(ref, cmap=cmap, levels=levels, extend=extend)
    axs[i_ref].format(title=ref.title)

    # New simulation
    axs[i_new].pcolormesh(new, cmap=cmap, levels=levels, extend=extend)
    axs[i_new].format(title=new.title)
    axs[i_new].colorbar(m0, label=label + ' [' + units + ']', loc=cbar_loc)

    # Differences between the new and reference simulation
    m2 = axs[i_diff].pcolormesh(new - ref, cmap=cmap_diff, levels=levels_diff,
                           extend=extend_diff)
    axs[i_diff].format(title=ref.title + '\n - ' + new.title)
    axs[i_diff].colorbar(m2, 
                         label='Difference of\n' + label + ' [' + units + ']',
                         loc=cbar_loc)

    # Bias of reference simulation regarding to observation
    m3 = axs[i_ref_bias].pcolormesh(ref - obs, cmap=cmap_bias, 
                                    levels=levels_bias, extend=extend_bias)
    axs[i_ref_bias].format(title=ref.title + '\n - ' + obs.obs_name)

    # Bias of new simulation regarding to observation
    axs[i_new_bias].pcolormesh(new - obs, cmap=cmap_bias, levels=levels_bias,
                      extend=extend_bias)
    axs[i_new_bias].format(title=new.title + '\n - ' + obs.obs_name)
    axs[i_new_bias].colorbar(m3, 
                             label='Bias of\n' + label + ' [' + units + ']',
                             loc=cbar_loc)

    # Observation
    axs[i_obs].pcolormesh(obs, cmap=cmap, levels=levels, extend=extend)
    axs[i_obs].format(title=obs.obs_name)
    axs[i_obs].colorbar(m0, label=label + ' [' + units + ']', loc=cbar_loc)

    axs.format(
        labels=True,
        coast=True,
        borders=True,
        latlim=(ref.lat.min(), ref.lat.max()),
        lonlim=(ref.lon.min(), ref.lon.max()),
        suptitle=label + " " + ref.attrs['season'] + " climatology: " + \
            new.attrs['period'],
        abc=True
    )

    if save:
        for extension in ['jpg', 'png', 'pdf']:
            fig.save(
                'img/' +
                new.attrs['title'] +
                '/' +
                var +
                '_' +
                ref.attrs['zone'] +
                '_' +
                ref.attrs['season'] +
                '_clim_' +
                new.attrs['period'] +
                '_' +
                new.attrs['title'] +
                '_REF_' +
                obs.attrs['obs_name'] +
                '.' +
                extension)
            
            
            
def plot_zonal_bias_HMA(
    var, ref, new, obs, label, units,
    levels_diff, cmap_diff, extend_diff,
    levels_bias, cmap_bias, extend_bias,
    save=False, dpi=300
):
    """
        Plot zonal climatology bias of 2 simulations versus observations and 
        their differences. First (second) row contains the first (second) 
        simulation versus observations and the third row contains the 
        differences. The three columns correspond to global, HMA and global
        without HMA domains.

        Parameters
        ----------
        var : str
            Variable name. Options are: 'ta'.

        label : str
            Name of the variable.

        units : str
            Units of the variables.

        ref, new, obs : DataArray
            Reference, new simulation and observation. The following attributes
            are needed:
                - 'title' for the name of the plots 
                - 'period' for the suptitle and saving the figure
                - 'season' for the suptitle and saving the figure
                - 'zone' for the suptitle and saving the figure

        levels_diff, levels_bias : numpy.ndarray, optional
            Levels for the plots.

        cmap_diff, cmap_bias : colormap spec
            Colormaps for the plots.

        extend_diff, extend_bias : numpy.ndarray
            Extends for the plots.

        save : bool, optional
            Save the figure or not. Default is None (does not save the figure).
            Save figures to jpg, png and pdf.

        dpi : int, optional
            DPI of the figure. Default is 300.

        Example
        -------
        >>> import xarray as xr
        >>> import proplot as plot
        >>> import sys
        >>> sys.path.insert(1, '/home/mlalande/notebooks/utils')
        >>> import utils as u
        >>>
        >>> period = slice('1979','2014')
        >>> var = 'ta'
        >>> label, units, cmap = u.get_var_infos(var)
        >>>
        >>> ref = xr.open_dataarray(...); ref.attrs['title'] = ...
        >>> new = xr.open_dataarray(...); new.attrs['title'] = ...
        >>> obs = xr.open_dataarray(...); obs.attrs['title'] = ...
        >>>
        >>> clim_ref = u.clim(ref.sel(time=period))
        >>> clim_new = u.clim(ref.sel(time=period))
        >>> clim_obs = u.clim(ref.sel(time=period))
        >>>
        >>> label, units, \
            levels, cmap, extend, \
            levels_diff, cmap_diff, extend_diff, \
            levels_bias, cmap_bias, extend_bias = u.get_var_infos(var)
        >>>
        >>> u.plot_ref_new_obs(
                var, clim_ref, clim_new, clim_obs, label, units,
                levels_diff, cmap_diff, extend_diff,
                levels_bias, cmap_bias, extend_bias,
                save=False, dpi=300
            )


    """
    
    fig, axs = plot.subplots(nrows=3, ncols=3)

    k = 0 # Index for axes
    color = 'black' # Line color for climatology contour
    lw = 0.6 # Line width for climatology contour
    alpha = 0.8 # Transparence for climatology contour
    ylim = (1000,0)
    
    latlim, lonlim = get_zone('HMA')
    
    ################################################
    # Bias between simulations versus observations #
    ################################################
    
    for simu in [ref, new]:
        bias = simu - obs
        
        # Global
        m = axs[k].contourf(
            bias.mean('lon', skipna=False),
            cmap=cmap_bias,
            levels=levels_bias,
            extend=extend_bias
        )
        axs[k].contour(
            simu.mean('lon', skipna=False),
            color=color,
            lw=lw,
            alpha=alpha,
            labels=True
        )
        axs[k].format(
            ylim=ylim,
            title=''
        )
        k += 1
        
        # HMA
        axs[k].contourf(
            bias.sel(lon=lonlim).mean('lon', skipna=False),
            cmap=cmap_bias,
            levels=levels_bias,
            extend=extend_bias
        )
        axs[k].contour(
            simu.sel(lon=lonlim).mean('lon', skipna=False),
            color=color,
            lw=lw,
            alpha=alpha,
            labels=True
        )
        axs[k].format(
            ylim=ylim,
            title=simu.attrs['title'] + '\n - ' + obs.attrs['obs_name']
        )
        k += 1

        # Global without HMA
        axs[k].contourf(
            bias.where(
                (bias.lon < lonlim.start) | (bias.lon > lonlim.stop),
                drop=True
            ).mean('lon', skipna=False),
            cmap=cmap_bias,
            levels=levels_bias,
            extend=extend_bias
        )
        axs[k].contour(
            simu.where(
                (bias.lon < lonlim.start) | (bias.lon > lonlim.stop),
                drop=True
            ).mean('lon', skipna=False),
            color=color,
            labels=True,
            lw=lw,
            alpha=alpha
        )
        axs[k].format(
            ylim=ylim,
            title=''
        )
        k += 1

    fig.colorbar(
        m, 
        label='Bias of ' + label + ' [' + units + ']',
        loc='r',
        rows=(1, 2)
    )
    
    ###########################################
    # Differences between the two simulations #
    ###########################################
    
    diff = new - ref
    
    # Global
    m = axs[k].contourf(
        diff.mean('lon', skipna=False),
        cmap=cmap_diff,
        levels=levels_diff,
        extend=extend_diff
    )
    axs[k].contour(
        new.mean('lon', skipna=False),
        color=color,
        lw=lw,
        alpha=alpha,
        labels=True
    )
    axs[k].format(
        ylim=ylim,
        title=''
    )
    k += 1

    # HMA
    axs[k].contourf(
        diff.sel(lon=lonlim).mean('lon', skipna=False),
        cmap=cmap_diff,
        levels=levels_diff,
        extend=extend_diff
    )
    axs[k].contour(
        new.sel(lon=lonlim).mean('lon', skipna=False),
        color=color,
        lw=lw,
        alpha=alpha,
        labels=True
    )
    axs[k].format(
        ylim=ylim,
        title=new.attrs['title'] + '\n - ' + ref.attrs['title']
    )
    k += 1

    # Global without HMA
    axs[k].contourf(
        diff.where(
            (diff.lon < lonlim.start) | (diff.lon > lonlim.stop),
            drop=True
        ).mean('lon', skipna=False),
        cmap=cmap_diff,
        levels=levels_diff,
        extend=extend_diff
    )
    axs[k].contour(
        new.where(
            (bias.lon < lonlim.start) | (bias.lon > lonlim.stop),
            drop=True
        ).mean('lon', skipna=False),
        color=color,
        labels=True,
        lw=lw,
        alpha=alpha
    )
    axs[k].format(
        ylim=ylim,
        title=''
    )
    k += 1
    
    fig.colorbar(
        m, 
        label='Difference of ' + label + ' [' + units + ']',
        loc='r',
        row=3
    )
    
    ##########
    # Format #
    ##########
    
    axs.format(
        suptitle=label + " " + ref.attrs['season'] + " zonal climatology bias: " + \
            new.attrs['period'], 
        abc=True,
        collabels=[
            'Global', 
            'HMA ('+str(lonlim.start)+'°E-'+str(lonlim.stop)+'°E)',
            'Global without HMA',
            
        ],
        ylabel='Level (hPa)'
    )

    if save:
        for extension in ['jpg', 'png', 'pdf']:
            fig.save(
                'img/' +
                new.attrs['title'] +
                '/' +
                var +
                '_' +
                ref.attrs['zone'] +
                '_' +
                ref.attrs['season'] +
                '_zonal_clim_bias_diff_' +
                new.attrs['period'] +
                '_' +
                new.attrs['title'] +
                '_REF_' +
                obs.attrs['obs_name'] +
                '.' +
                extension)
