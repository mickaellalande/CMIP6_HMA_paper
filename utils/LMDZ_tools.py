#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autopep8: https://pypi.org/project/autopep8/
# Check with http://pep8online.com/

import numpy as np


def phys2dyn(da_phys, grid):
    """
        Convert a DataArray from the LMDZ physical grid to a regular dynamical
        grid (without redundant grid points in longitudes as in LMDZ).

        - Physical grid : single index (from the North Pole to the South Pole)
        - Dynamical grid: global lonxlat grid with redundant grid points at the
                          poles

        See for more details on the LMDZ grid:
            - https://www.lmd.jussieu.fr/~lmdz/manuelGCM/main/node3.html

        See for more details on DataArray:
            - http://xarray.pydata.org/en/stable/data-structures.html

        Parameters
        ----------
        da_phys : DataArray
            Variable on the physical grid that you want to convert to the
            dynamical grid (ex: ZMEA from startphy.nc).
        grid : Dataset
            Grid Dataset used to make the conversion (grilles_gcm.nc).

        Returns
        -------
        da_dyn : DataArray
            Variable on the dynamical grid.

        Example
        -------
        >>> import xarray as xr
        >>> startphy = xr.open_dataset('startphy.nc')
        >>> grid = xr.open_dataset('grilles_gcm.nc')
        >>> da_dyn = phys2dyn(startphy.ZMEA, grid)
    """

    # Copy the grid "grille_s" (latu,lonv) without the last duplicated
    # longitude
    da_dyn = grid.grille_s.isel(lonv=slice(0, -1)).copy()

    # Check that the size of "points_physiques" fit with the dynamic grid
    np.testing.assert_equal(
        da_dyn.lonv.size * da_dyn.latu.size - 2 * (da_dyn.lonv.size - 1),
        da_phys.size
    )

    # Fill the values from the physical grid to the dynamic grid
    da_dyn[0] = da_phys[0]  # Replicate North Pole point
    da_dyn[-1] = da_phys[-1]  # Replicate South Pole point
    k = 0  # Fill other values
    for lat in range(da_dyn.latu.size - 2):
        for lon in range(da_dyn.lonv.size):
            da_dyn[1:-1, :][lat, lon] = da_phys[k + 1]
            k += 1

    # Check that we felt all values (except poles)
    np.testing.assert_equal(k, da_phys.size - 2)

    # lonv: [180,540] -> [0,360]; latu: [90,-90] -> [-90,90]
    da_dyn = da_dyn.roll(
        lonv=int(grid.lonv.size / 2), roll_coords=True
    ).sortby('latu')
    da_dyn.coords['lonv'] = np.arange(0, 360, 360 / da_dyn.lonv.size)
    da_dyn.coords['lonv'].attrs = grid.lonv.attrs

    # Rename da_dyn
    da_dyn.name = da_phys.name
    da_dyn.attrs = da_phys.attrs
    da_dyn = da_dyn.rename({'latu': 'lat', 'lonv': 'lon'})

    return da_dyn
