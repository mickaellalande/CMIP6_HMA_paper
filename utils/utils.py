#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autopep8: https://pypi.org/project/autopep8/
# Check with http://pep8online.com/

# =============================================================================
# Import modules
# =============================================================================
import psutil
import sys
import numpy as np
import xarray as xr
from cartopy.util import add_cyclic_point

# Personnal functions
from models import *  # for loading models on CICLAD
from variables import *  # get var infos and cmap
from clim import *  # makes weighted montlhy computations
from zones import *  # make zones
from LMDZ_tools import *  # LMDZ tools
from obs import *  # Load observations
from regrid import *  # Regrid
from figures import *  # Make plots
from param_SCF import * # Parameterization SCF


# =============================================================================
# Basic functions
# =============================================================================
def check_python_version():
    print(sys.version)


def check_virtual_memory():
    # https://psutil.readthedocs.io/en/latest/#psutil.virtual_memory
    values = psutil.virtual_memory()
    print("Virtual memory usage - " +
          "total: " +
          str(get_human_readable_size(values.total)) +
          " / " +
          "available: " +
          str(get_human_readable_size(values.available)) +
          " / " +
          "percent used: " +
          str(values.percent) +
          " %")


def get_human_readable_size(num):
    # https://stackoverflow.com/questions/21792655/\
    # psutil-virtual-memory-units-of-measurement
    exp_str = [(0, 'B'), (10, 'KB'), (20, 'MB'),
               (30, 'GB'), (40, 'TB'), (50, 'PB'), ]
    i = 0
    while i + 1 < len(exp_str) and num >= (2 ** exp_str[i + 1][0]):
        i += 1
        rounded_val = round(float(num) / 2 ** exp_str[i][0], 2)
    return '%s %s' % (int(rounded_val), exp_str[i][1])


def check_period_size(period, ds_sub, ds, frequency='monthly'):
    """
        Check if the data size is equal the actual period size.

        Parameters
        ----------
        period : slice
            Applied period slicing (time dimension needs to be named 'time').

        ds_sub : xarray.core.dataarray.DataArray, xarray.core.dataset.Dataset
            Subset data.

        ds : xarray.core.dataarray.DataArray, xarray.core.dataset.Dataset
            Data before subset.

        frequency : str
            Frequency of the data (ex: 'monthly', 'daily', etc.).

        Example
        -------
        >>> import numpy as np
        >>> import xarray as xr
        >>> import sys
        >>> sys.path.insert(1, '/home/mlalande/notebooks/utils')
        >>> import utils as u
        >>>
        >>> period = slice('1979','2014')
        >>> ds = xr.open_dataset(...)
        >>> ds_sub = ds.sel(time=period)
        >>> u.check_period(period, ds_sub, ds, frequency='monthly')

    """

    # Compute the expected size of the period 
    if frequency == 'monthly':
        expected_period = (int(period.stop) - int(period.start) + 1) * 12
    else:
        raise ValueError(f"Invalid frequency argument: '{frequency}'.\
        Valid names are: 'monthly'.")

    # Check that the expected period fits with the subset of the data
    np.testing.assert_equal(
        expected_period,
        ds_sub.time.size,
        err_msg=f"Invalid period argument: '{period}'.\
        Valid period: {ds.isel(time=0)['time.year'].values}\
        to {ds.isel(time=-1)['time.year'].values}."
    )


def check_first_last_year(period, ds):
    """
        Check if the data is fitting in the period.

        Parameters
        ----------
        period : slice
            Applied period slicing (time dimension needs to be named 'time').

        ds : xarray.core.dataarray.DataArray, xarray.core.dataset.Dataset
            Data.

        Example
        -------
        >>> import xarray as xr
        >>> import sys
        >>> sys.path.insert(1, '/home/mlalande/notebooks/utils')
        >>> import utils as u
        >>>
        >>> period = slice('1979','2014')
        >>> ds = xr.open_dataset(...)
        >>> u.check_first_last_year(period, ds)

    """

    # Check that the expected period fits in the data period
    np.testing.assert_array_less(
        int(ds.isel(time=0)['time.year'].values) - 1,
        int(period.start),
        err_msg=f"Invalid period.start argument: '{period.start}'.\
        Min period: '{ds.isel(time=0)['time.year'].values}'."
    )

    np.testing.assert_array_less(
        int(period.stop),
        int(ds.isel(time=-1)['time.year'].values) + 1,
        err_msg=f"Invalid period.stop argument: '{period.stop}'.\
        Max period: '{ds.isel(time=-1)['time.year'].values}'."
    )


# =============================================================================
# Geophysical functions
# =============================================================================

def deg2km(nlon, nlat, lat):
    # Gives the size of a grid cell in km at the corresponding latitude
    R_earth = 6371
    x = 2 * np.pi * R_earth / nlon * np.cos(np.deg2rad(lat))
    y = np.pi * R_earth / nlat
    return {'x': x, 'y': y, 'units': 'km'}


# https://pangeo.io/use_cases/physical-oceanography/sea-surface-height.html
def spatial_average(da):

    # Get the longitude and latitude names + other dimensions to test that the
    # sum of weights is right
    lat_str = ''
    lon_str = ''
    other_dims_str = []
    for dim in da.dims:
        if dim in ['lat', 'latitude']:
            lat_str = dim
        elif dim in ['lon', 'longitude']:
            lon_str = dim
        else:
            other_dims_str.append(dim)

    # Compute the weights
    coslat = np.cos(np.deg2rad(da.lat)).where(~da.isnull())
    weights = coslat / coslat.sum(dim=(lat_str, lon_str))

    # Test that the sum of weights equal 1
    np.testing.assert_allclose(
        weights.sum(dim=(lat_str, lon_str)).values,
        np.ones([da.coords[dim_str].size for dim_str in other_dims_str]),
        rtol=1e-06
    )

    with xr.set_options(keep_attrs=True):
        return (da * weights).sum(dim=(lat_str, lon_str))


# https://github.com/darothen/plot-all-in-ncfile/blob/master/plot_util.py
def cyclic_dataarray(da, coord='lon'):
    """ Add a cyclic coordinate point to a DataArray along a specified
    named coordinate dimension.
    """
    assert isinstance(da, xr.DataArray)

    lon_idx = da.dims.index(coord)
    cyclic_data, cyclic_coord = add_cyclic_point(da.values,
                                                 coord=da.coords[coord],
                                                 axis=lon_idx)

    # Copy and add the cyclic coordinate and data
    new_coords = dict(da.coords)
    new_coords[coord] = cyclic_coord
    new_values = cyclic_data

    new_da = xr.DataArray(new_values, dims=da.dims, coords=new_coords)

    # Copy the attributes for the re-constructed data and coords
    for att, val in da.attrs.items():
        new_da.attrs[att] = val
    for c in da.coords:
        for att in da.coords[c].attrs:
            new_da.coords[c].attrs[att] = da.coords[c].attrs[att]

    return new_da
