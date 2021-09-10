#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autopep8: https://pypi.org/project/autopep8/
# Check with http://pep8online.com/

import proplot as plot

# =============================================================================
# Select variable on CICLAD
# =============================================================================


def get_table(var):
    if var in ['tas', 'pr', 'prsn', 'ta']:
        table = 'Amon'
    elif var in ['snc']:
        table = 'LImon'
    else:
        raise NameError('The variable ' + name + ' is not defined')

    return table


def get_var_infos(var):
    """
        Get default informations about variable as: label, units, levels, cmap,
        extend for regular plot, differences and bias.

        Parameters
        ----------
        var : str
            Variable name. Options are:

            - 'snc', 'frac_snow' (Snow Cover Extent)
            - 'tas', 't2m', 'tmp (Near-Surface Air Temperature)
            - 'pr' (Total Precipitation)
            - 'ta' (Air Temperature)

        Returns
        -------
        label : str
            Name of the variable.

        units : str
            Usual units of the variable.

        levels, levels_diff, levels_bias : ndarray
            Levels.

        cmap, cmap_diff, cmap_bias : str
            Usual colormap for the varibale.

        extend, extend, extend : {{'neither', 'min', 'max', 'both'}}
            Where to assign unique colors to out-of-bounds data and draw
            "extensions" (triangles, by default) on the colorbar.

        Example
        -------
        >>> import sys
        >>> sys.path.insert(1, '/home/mlalande/notebooks/utils')
        >>> import utils as u
        >>>
        >>> label, units, \
            levels, cmap, extend, \
            levels_diff, cmap_diff, extend_diff, \
            levels_bias, cmap_bias, extend_bias = u.get_var_infos('snc')

    """

    # Snow Cover Extent
    if var in ['snc', 'frac_snow']:
        label = 'Snow Cover Extent'
        units = '%'

        levels = plot.arange(0, 100, 10)
        cmap = 'viridis'
        extend = 'neither'

        levels_diff = plot.arange(-50, 50, 10)
        cmap_diff = 'BuRd_r'
        extend_diff = 'both'

        levels_bias = plot.arange(-50, 50, 10)
        cmap_bias = 'BuRd_r'
        extend_bias = 'both'

    # Near-Surface Air Temperature
    elif var in ['tas', 't2m', 'tmp']:
        label = 'Near-Surface Air Temperature'
        units = '°C'

        levels = plot.arange(-30, 30, 5)
        cmap = 'CoolWarm'
        extend = 'neither'

        levels_diff = plot.arange(-5, 5, 1)
        cmap_diff = 'BuRd'
        extend_diff = 'both'

        levels_bias = plot.arange(-14, 14, 2)
        cmap_bias = 'BuRd'
        extend_bias = 'both'

    # Total Precipitation
    elif var in ['pr', 'tp', 'precip']:
        label = 'Total Precipitation'
        units = 'mm/day'

        levels = plot.arange(0, 5, 0.5)
        cmap = 'DryWet'
        extend = 'neither'

        levels_diff = plot.arange(-1, 1, 0.2)
        cmap_diff = 'BuRd_r'
        extend_diff = 'both'

        levels_bias = plot.arange(-5, 5, 1)
        cmap_bias = 'BuRd_r'
        extend_bias = 'both'

    # Snowfall
    elif var == 'prsn':
        label = 'Snowfall'
        units = 'mm/day'
        cmap = 'DryWet'
        levels = plot.arange(0, 5, 0.5)

    # Eastward Wind
    elif var == 'ua':
        label = 'Eastward Wind'
        units = 'm/s'
        cmap = 'CoolWarm'
        levels = plot.arange(-7, 7, 1)

    # Air Temperature
    elif var == 'ta':
        label = 'Air Temperature'
        units = '°C'
        
        levels = plot.arange(-30, 30, 2)
        cmap = 'Spectral'
        extend = 'both'

        levels_diff = plot.arange(-1, 1, 0.2)
        cmap_diff = 'BuRd'
        extend_diff = 'both'

        levels_bias = plot.arange(-7, 7, 1)
        cmap_bias = 'BuRd'
        extend_bias = 'neither'

    else:
        raise ValueError(
            f"""Invalid variable argument: '{var}'. Valid names are:
                - 'snc', 'frac_snow' (Snow Cover Extent)
                - 'tas', 't2m', 'tmp (Near-Surface Air Temperature)
                - 'pr' (Total Precipitation)
                - 'ta' (Air Temperature)
             """
        )

    return label, units, \
        levels, cmap, extend, \
        levels_diff, cmap_diff, extend_diff, \
        levels_bias, cmap_bias, extend_bias
