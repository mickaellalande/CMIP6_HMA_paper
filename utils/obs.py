#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autopep8: https://pypi.org/project/autopep8/
# Check with http://pep8online.com/

# Get observations and reanalyses

import numpy as np
import xarray as xr
from regrid import regrid
import utils as u


def get_obs(
        obs_name,
        version,
        var,
        period=slice(None),
        machine='CICLAD',
        regrid=None):
    """
        Get observation data in a DataArray
        (http://xarray.pydata.org/en/stable/data-structures.html) on a specific
        machine and performs a bilinear interpolation using xESMF
        (https://xesmf.readthedocs.io/en/latest/) if necessary. If not monthly
        the data is resample in monthly frequency.

        Parameters
        ----------
        obs_name : str
            Observation name. Options are:

            - 'NH_SCE_CDR': NOAA Climate Data Record (CDR) of Northern
            Hemisphere (NH) Snow Cover Extent (SCE), Version 1
            (https://doi.org/10.7289/V5N014G9)
            
            - 'NH_SCE_CDR_HR': NOAA Climate Data Record (CDR) of Northern
            Hemisphere (NH) Snow Cover Extent (SCE), Version 1 at 24 km 
            (not official; Contact: lawrence.mudryk@canada.ca)

            - 'MEaSUREs': MEaSUREs Northern Hemisphere Terrestrial Snow Cover
            Extent Daily 25km EASE-Grid 2.0, Version 1
            (https://nsidc.org/data/nsidc-0530)

            - 'CRU_TS': Climatic Research Unit
            (https://crudata.uea.ac.uk/cru/data/hrg/)

            - 'APHRO_MA': APHRODITE Monsoon Asia Daily precipitation
            (Yatagai et al., 2012)
            http://aphrodite.st.hirosaki-u.ac.jp/download/data/search/,
            http://aphrodite.st.hirosaki-u.ac.jp/download/ V1101 et V1101EX_R1
            domain MA
            
            - 'ERAI': ERA-Interim 
            (https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era-interim)


        version, var : str
            Version and variable of the dataset. Options are:
            - NH_SCE_CDR: 'v01r01' / 'snc'
            - NH_SCE_CDR_HR: 'v01r00' / 'snc'
            - MEaSUREs: 'v01r01' / 'snc'
            - CRU_TS: '4.00', '4.04' / 'tas'
            - APHRO_MA: 'V1101' / 'pr'
            - ERAI: '' / 'ta'

        period : slice, optional
            Time period (ex: slice('1979','2014')). Default is no slicing.

        machine : str, optional
            Machine name. Default is CICLAD. Options are: 'CICLAD'.

        regrid : DataArray, Dataset, optional
            Data towards which the observation will be regrided. Default does
            not make any interpolation.

        Returns
        -------
        obs : xarray.core.dataarray.DataArray
            Observation data on monthly time scale.

        Example
        -------
        >>> import xarray as xr
        >>> import sys
        >>> sys.path.insert(1, '/home/mlalande/notebooks/utils')
        >>> import utils as u
        >>>
        >>> snc_ref = xr.open_dataset(...)
        >>> obs = u.get_obs(
                        'NH_SCE_CDR',
                        'v01r01',
                        'snc',
                        period=slice('1979','2014'),
                        machine='CICLAD',
                        egrid=snc_ref)

    """

    #####################
    # Snow Cover Extent #
    #####################
    if var in ['snc', 'frac_snow']:

        # NOAA Climate Data Record (CDR) of Northern Hemisphere (NH) Snow Cover
        # Extent (SCE), Version 1 (https://doi.org/10.7289/V5N014G9)
        if obs_name == 'NH_SCE_CDR':
            if version not in ['v01r01']:
                raise ValueError(
                    f"Invalid version argument: '{version}'. "
                     "Valid version are: 'v01r01'."
                )

            # Select machine
            if machine in ['CICLAD']:
                path = '/data/mlalande/RUTGERS/' \
                    'nhsce_' + version + '_19661004_20191202.nc'
            else:
                raise ValueError(
                    f"Invalid machine argument: '{machine}'. "
                     "Valid names are: 'CICLAD'."
                )

            # Get raw data
            print('Get observation: ' + obs_name + '\n' + path + '\n')
            ds = xr.open_dataset(path)
            u.check_first_last_year(period, ds)

            # Get the snc variable, keep only land data and convert to %
            with xr.set_options(keep_attrs=True):
                obs = ds.sel(
                    time=period).snow_cover_extent.where(
                    ds.land == 1) * 100
            obs.attrs['units'] = '%'
            obs.attrs['obs_name'] = obs_name + '_' + version
            obs.attrs.update(ds.attrs)

            # Rename lon and lat for the regrid
            obs = obs.rename({'longitude': 'lon', 'latitude': 'lat'})

            # Resamble data per month (from per week)
            obs = obs \
                .resample(time='1MS') \
                .mean('time', skipna='False', keep_attrs=True)

            u.check_period_size(period, obs, ds, frequency='monthly')
            
            
        # NOAA Climate Data Record (CDR) of Northern Hemisphere (NH) Snow Cover
        # Extent (SCE), Version 1 at 24 km (not official) 
        # Contact: lawrence.mudryk@canada.ca
        if obs_name == 'NH_SCE_CDR_HR':
            if version not in ['v01r00']:
                raise ValueError(
                    f"Invalid version argument: '{version}'. "
                     "Valid version are: 'v01r00'."
                )

            # Select machine
            if machine in ['CICLAD']:
                path = '/data/mlalande/RUTGERS/' \
                    'G10035-rutgers-nh-24km-weekly-sce-' + version + \
                    '-19800826-20200831_newer_without_xy.nc'
            else:
                raise ValueError(
                    f"Invalid machine argument: '{machine}'. "
                     "Valid names are: 'CICLAD'."
                )

            # Get raw data
            print('Get observation: ' + obs_name + '\n' + path + '\n')
            
            # Select only values with valid lat and lon for regrid
            # (missing lat/lon values are set to ~9.9e+36)
            ds = (xr.open_dataset(path)).isel(x=slice(158,867), y=slice(158,867))
            u.check_first_last_year(period, ds)

            # Get the snc variable, keep only land data and convert to %
            with xr.set_options(keep_attrs=True):
                obs = ds.sel(
                    time=period).snow_cover_extent.where(
                    ds.land == 1) * 100
            obs.attrs['units'] = '%'
            obs.attrs['obs_name'] = obs_name + '_' + version
            obs.attrs.update(ds.attrs)

            # Rename lon and lat for the regrid
            obs = obs.rename({'longitude': 'lon', 'latitude': 'lat'})

            # Resamble data per month (from per week)
            obs = obs \
                .resample(time='1MS') \
                .mean('time', skipna='False', keep_attrs=True)

            u.check_period_size(period, obs, ds, frequency='monthly')
            

        # MEaSUREs Northern Hemisphere Terrestrial Snow Cover Extent Daily 25km
        # EASE-Grid 2.0, Version 1 (https://nsidc.org/data/nsidc-0530)
        elif obs_name == 'MEaSUREs':

            if version not in ['v01r01']:
                raise ValueError(
                    f"Invalid version argument: '{version}'. "
                     "Valid version are: 'v01r01'."
                )

            # Select machine
            if machine in ['CICLAD']:
                path = '/data/mlalande/MEaSUREs/monthly/' \
                    'nhtsd25e2_*_' + version + '.nc'
            else:
                raise ValueError(
                    f"Invalid machine argument: '{machine}'. "
                     "Valid names are: 'CICLAD'."
                )

            # Get raw data
            print('Get observation: ' + obs_name + '\n' + path + '\n')
            ds = xr.open_mfdataset(path, combine='by_coords')
            u.check_first_last_year(period, ds)

            # Select period
            obs = ds.sel(time=period)

            # Get the snc variable and convert to %
            with xr.set_options(keep_attrs=True):
                obs = ds.merged_snow_cover_extent * 100
            obs.attrs['units'] = '%'
            obs.attrs['title'] = "MEaSUREs Northern Hemisphere Terrestrial Snow\
            Cover Extent Daily 25km EASE-Grid 2.0, Version 1"
            obs.attrs['product_version'] = 'v01r01'
            obs.attrs['metadata_link'] = 'https://nsidc.org/data/nsidc-0530'
            obs.attrs['summary'] = "This data set, part of the NASA Making\
            Earth System Data Records for Use in Research Environments\
            (MEaSUREs) program, offers users 25 km Northern Hemisphere snow\
            cover extent represented by four different variables. Three of the\
            snow cover variables are derived from the Interactive Multisensor\
            Snow and Ice Mapping System, MODIS Cloud Gap Filled Snow Cover,\
            and passive microwave brightness temperatures, respectively. The\
            fourth variable merges the three source products into a single\
            representation of snow cover."
            obs.attrs['spatial_resolution'] = "25 km x 25 km"
            obs.attrs['spatial_coverage'] = "N: 90, S: 0, E: 180, W: -180"
            obs.attrs['temporal_coverage'] = "1 January 1999 to 31 December\
            2012"
            obs.attrs['temporal_resolution'] = "1 day"
            obs.attrs['data_contributors'] = "David Robinson, Dorothy Hall,\
            Thomas Mote"
            obs.attrs['sensor'] = "MODIS, SSM/I, SSMIS"
            obs.attrs['obs_name'] = obs_name + '_' + version
            obs.attrs.update(ds.attrs)

            # Rename lon and lat for the regrid
            obs = obs.rename({'longitude': 'lon', 'latitude': 'lat'})

            # Resamble data per month (from per day)
            obs = obs.resample(
                time='1MS').mean(
                'time',
                skipna='False',
                keep_attrs=True)
            u.check_period_size(period, obs, ds, frequency='monthly')

        else:
            raise ValueError(
                f"Invalid obs_name argument: '{obs_name}'. "
                 "Valid names are: 'NOAA-CDR-v1'."
            )

    #################
    # Precipitation #
    #################
    elif var in ['pr', 'precip']:

        # APHRODITE: http://aphrodite.st.hirosaki-u.ac.jp/download/data/search/
        # http://aphrodite.st.hirosaki-u.ac.jp/download/ V1101 et V1101EX_R1
        # domain MA
        if obs_name == 'APHRO_MA':
            if version not in ['V1101']:
                raise ValueError(
                    f"Invalid version argument: '{version}'. "
                     "Valid version are: 'v01r01'."
                )

            # Select machine
            if machine in ['CICLAD']:

                path = '/data/mlalande/APHRODITE/' \
                    'APHRO_MA_050deg_' + version + '.*.nc'

                path_ext = '/data/mlalande/APHRODITE/' \
                    'APHRO_MA_050deg_' + version + '_EXR1.*.nc'

            else:
                raise ValueError(
                    f"Invalid machine argument: '{machine}'. "
                     "Valid names are: 'CICLAD'."
                )

            # Get raw data
            print('Get observation: ' + obs_name + '\n' + path + '\n')
            ds_1 = xr.open_mfdataset(path)

            print('Get observation: ' + obs_name + '\n' + path_ext + '\n')
            ds_2 = xr.open_mfdataset(path_ext)

            # Combine the 2 dataset
            ds_1 = ds_1.rename({'longitude': 'lon', 'latitude': 'lat'})
            ds = xr.combine_nested([ds_1, ds_2], concat_dim='time')

            u.check_first_last_year(period, ds)

            # Get the precip variable on the seleted period
            obs = ds.precip.sel(time=period)
            # obs.attrs['units'] = 'mm/day'
            obs.attrs['obs_name'] = obs_name + '_' + version
            obs.attrs.update(ds_1.attrs)
            obs.attrs.update(ds_2.attrs)

            # Resamble data per month (from per day)
            obs = obs \
                .resample(time='1MS') \
                .mean('time', skipna='False', keep_attrs=True)

            u.check_period_size(period, obs, ds, frequency='monthly')
        else:
            raise ValueError(
                f"Invalid obs_name argument: '{obs_name}'. "
                 "Valid names are: 'APHRODITE'."
            )

    ################################
    # Near-Surface Air Temperature #
    ################################
    elif var in ['tas', 't2m', 'tmp']:

        # CRU: https://crudata.uea.ac.uk/cru/data/hrg/
        if obs_name in ['CRU_TS']:

            if version not in ['4.00', '4.04']:
                raise ValueError(
                    f"Invalid version argument: '{version}'. "
                     "Valid version are: '4.00', '4.04'."
                )

            # Select machine
            if machine in ['CICLAD']:

                if version == '4.00':
                    path = '/bdd/cru/cru_ts_4.00/data/tmp/' \
                        'cru_ts4.00.1901.2015.tmp.dat.nc'

                elif version == '4.04':
                    path = '/data/mlalande/CRU/tmp/' \
                        'cru_ts4.04.1901.2019.tmp.dat.nc'
            else:
                raise ValueError(
                    f"Invalid machine argument: '{machine}'. "
                     "Valid names are: 'CICLAD'."
                )

            # Get raw data
            print('Get observation: ' + obs_name + '\n' + path + '\n')
            ds = xr.open_dataset(path)
            u.check_first_last_year(period, ds)

            # Select period
            obs = ds.sel(time=period).tmp
            u.check_period_size(period, obs, ds, frequency='monthly')

            obs.attrs['units'] = '°C'
            obs.attrs['obs_name'] = obs_name + '_' + version
            obs.attrs.update(ds.attrs)

        else:
            raise ValueError(
                f"Invalid obs_name argument: '{obs_name}'. "
                 "Valid names are: 'CRU'."
            )
            
    ###################
    # Air Temperature #
    ###################
    elif var in ['ta']:

        # ERA-Interim: https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era-interim
        if obs_name in ['ERAI']:

            if version not in ['']:
                raise ValueError(
                    f"Invalid version argument: '{version}'. "
                     "Valid version are: ''."
                )

            # Select machine
            if machine in ['CICLAD']:

                if version == '':
                    path = '/bdd/ERAI/NETCDF/GLOBAL_075/1xmonthly/AN_PL/*/' \
                        'ta.*.apmei.GLOBAL_075.nc'
                    path_ps = '/data/mlalande/ERAI/sp/sp_ERAI_*.nc'

            else:
                raise ValueError(
                    f"Invalid machine argument: '{machine}'. "
                     "Valid names are: 'CICLAD'."
                )
                
            # Get raw data
            print('Get observation: ' + obs_name + '\n' + path + '\n')
            ds = xr.open_mfdataset(path, combine='by_coords')
            ds_ps = xr.open_mfdataset(path_ps, combine='by_coords')
            ds_ps = ds_ps.rename({'longitude': 'lon', 'latitude': 'lat'})
            u.check_first_last_year(period, ds)

            # Select period
            obs = ds.sel(time=period).ta.sortby('lat') - 273.15
            obs_ps = ds_ps.sel(time=period).sp.sortby('lat')
            u.check_period_size(period, obs, ds, frequency='monthly')

            # Mask vertical values > ps and convert units
            obs = obs.where(obs.level <= obs_ps/100)
            
            obs.attrs['units'] = '°C'
            obs.attrs['obs_name'] = obs_name
            obs.attrs.update(ds.attrs)

        else:
            raise ValueError(
                f"Invalid obs_name argument: '{obs_name}'. "
                 "Valid names are: 'CRU'."
            )
            
            
    #########
    # Error #
    #########
    else:
        raise ValueError(
            f"""Invalid var argument: '{var}'. Valid names are:
                - 'snc', 'frac_snow'
                - 'tas', 't2m', 'tmp'
                - 'pr'
            """
        )

    ##########
    # Regrid #
    ##########
    if regrid is not None:

        # Chekc if data is global and/or periodic or not
        obs_names_not_global = ['NH_SCE_CDR', 'MEaSUREs', 'APHRO_MA']
        if obs_name in obs_names_not_global:
            globe = False
        else:
            globe = True

        obs_names_not_periodic = ['NH_SCE_CDR', 'APHRO_MA']
        if obs_name in obs_names_not_periodic:
            periodic = False
        else:
            periodic = True
        
        # Horizontal regrid
        obs = u.regrid(
            obs,
            regrid,
            'bilinear',
            globe=globe,
            periodic=periodic,
            reuse_weights=True)
        
        # Vertical regrid for 3D ATM data
        if var in ['ta']:
            obs = obs.interp(level=(regrid.level.values), method='linear')

    return obs
