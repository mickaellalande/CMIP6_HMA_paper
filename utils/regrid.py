#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autopep8: https://pypi.org/project/autopep8/
# Check with http://pep8online.com/

# Make regrid with xESMF

import numpy as np
import xesmf as xe
import scipy


def regrid(
        ds_in,
        ds_out,
        method='bilinear',
        globe=True,
        periodic=True,
        reuse_weights=True):
    """
        Regrid using xESMF (https://xesmf.readthedocs.io/en/latest/) and keep
        attributes from initial xarray data.

        Parameters
        ----------
        ds_in, ds_out : xarray DataSet, or dictionary
            Contain input and output grid coordinates. Look for variables
            ``lon``, ``lat``, and optionally ``lon_b``, ``lat_b`` for
            conservative method.

            Shape can be 1D (n_lon,) and (n_lat,) for rectilinear grids,
            or 2D (n_y, n_x) for general curvilinear grids.
            Shape of bounds should be (n+1,) or (n_y+1, n_x+1).

        method : str, optional
            Regridding method. Default to bilinear. Options are

            - 'bilinear'
            - 'conservative', **need grid corner information**
            - 'patch'
            - 'nearest_s2d'
            - 'nearest_d2s'

        globe : bool, optional
            Does the data has global coverage? If False, Nan values will be
            attributed outside of the domain. Default to True.

        periodic : bool, optional
            Periodic in longitude? Default to True.
            Only useful for global grids with non-conservative regridding.
            Will be forced to False for conservative regridding.

        reuse_weights : bool, optional
            Whether to read existing weight file to save computing time.
            False by default (i.e. re-compute, not reuse).


        Returns
        -------
        regridder : xesmf.frontend.Regridder
            xESMF regridder object with NaN outside of the grid.

        Example
        -------
        >>> import xarray as xr
        >>> import sys
        >>> sys.path.insert(1, '/home/mlalande/notebooks/utils')
        >>> import utils as u
        >>>
        >>> obs = xr.open_dataset(...)
        >>> model = xr.open_dataset(...)
        >>> obs_regrid = u.regrid(
                            obs,
                            model,
                            'bilinear',
                            globe=True,
                            periodic=True,
                            reuse_weights=True)


    """

    # Save the initial attributes
    attrs_in = ds_in.attrs

    # Make the regridder
    regridder = xe.Regridder(ds_in, ds_out, method=method,
                             periodic=periodic, reuse_weights=reuse_weights)

    # If the data is not global add NaNs value outside of the domain
    if not globe:
        regridder = add_matrix_NaNs(regridder)

    # Make the regrid
    ds_in_regrid = regridder(ds_in)

    # Add back initial attributes
    ds_in_regrid.attrs.update(attrs_in)

    return ds_in_regrid


def add_matrix_NaNs(regridder):
    """
        Add NaN values outside of the grid (otherwise 0 values are put by
        default in xESMF)

        See more: https://github.com/JiaweiZhuang/xESMF/issues/15

        Parameters
        ----------
        regridder : xesmf.frontend.Regridder
            Default regridder with 0 outside of the grid.

        Returns
        -------
        regridder : xesmf.frontend.Regridder
            Regridder with NaN outside of the grid.

        Example
        -------
        >>> import xarray as xr
        >>> import xesmf as xe
        >>>
        >>> obs = xr.open_dataset(...)
        >>> model = xr.open_dataset(...)
        >>> regridder = xe.Regridder(obs, model, 'bilinear', periodic=True,\
                        reuse_weights=True)
        >>> regridder = add_matrix_NaNs(regridder)
        >>> obs_regrid = regridder(obs)

    """

    X = regridder.weights
    M = scipy.sparse.csr_matrix(X)
    num_nonzeros = np.diff(M.indptr)
    M[num_nonzeros == 0, 0] = np.NaN
    regridder.weights = scipy.sparse.coo_matrix(M)

    return regridder
