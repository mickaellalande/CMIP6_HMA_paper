#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autopep8: https://pypi.org/project/autopep8/
# Check with http://pep8online.com/

import numpy as np
import xarray as xr
import calendar as cld

# =============================================================================
# Compute monthly weighted data
# =============================================================================
# http://xarray.pydata.org/en/stable/examples/monthly-means.html
dpm = {'noleap': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       '365_day': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'standard': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'gregorian': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'proleptic_gregorian':
       [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'all_leap': [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       '366_day': [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       '360_day': [0, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]}


def leap_year(year, calendar='standard'):
    """Determine if year is a leap year"""
    leap = False
    if ((calendar in ['standard', 'gregorian',
                      'proleptic_gregorian', 'julian']) and
            (year % 4 == 0)):
        leap = True
        if ((calendar == 'proleptic_gregorian') and
            (year % 100 == 0) and
                (year % 400 != 0)):
            leap = False
        elif ((calendar in ['standard', 'gregorian']) and
              (year % 100 == 0) and (year % 400 != 0) and
              (year < 1583)):
            leap = False
    return leap


def get_dpm(time, calendar='standard'):
    """
    Return a array of days per month corresponding to the months provided in
    `months`.
    """
    month_length = np.zeros(len(time), dtype=np.int)

    if calendar not in [
        'noleap', '365_day', 'standard', 'gregorian', 'proleptic_gregorian',
        'all_leap', '366_day', '360_day'
    ]:
        raise ValueError(
            f"""Invalid calendar argument: '{calendar}'. Valid values are:
                - 'noleap'   : [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                - '365_day'  : [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                - 'standard' : [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                - 'gregorian': [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                - 'proleptic_gregorian':
                               [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                - 'all_leap' : [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                - '366_day'  : [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                - '360_day'  : [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
            """
        )

    cal_days = dpm[calendar]

    for i, (month, year) in enumerate(zip(time.month, time.year)):
        month_length[i] = cal_days[month]
        if leap_year(year, calendar=calendar) and month == 2:
            month_length[i] += 1
    return month_length


# Custom seasonal climatology (on monthly data set, include just month)
def clim(ds, calendar='standard', season='annual', skipna=False):
    """
        Compute the climatology from monthly data by taking into account the
        number of days in each month. For seasonal climatology, compute all the
        months without removing any data (e.g. for 'DJF' it will take into
        account the first D and last JF). The time dimension needs to be named
        'time'.

        Parameters
        ----------
        ds : xarray.core.dataarray.DataArray, xarray.core.dataset.Dataset
            Monthly data to process.

        calendar : str, optional
            Calendar type. Default is 'standard'. Options are:

            - 'noleap'   : [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            - '365_day'  : [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            - 'standard' : [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            - 'gregorian': [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            - 'proleptic_gregorian':
                           [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            - 'all_leap' : [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            - '366_day'  : [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            - '360_day'  : [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]

        season : int, str, optional
            Season on wchich to compute the climatology. Default is 'annual'.
            Options are:

            - 'annual'
            - single month: int (ex: 1 for January, 2 for February, etc.)
            - any character string (ex: 'DJF', 'JJAS', etc.)

        skipna : bool, optional
            Whether to skip missing values when aggregating. Default to False
            (does not skip NaNs values).


        Returns
        -------
        clim : xarray.core.dataarray.DataArray, xarray.core.dataset.Dataset
            Weighted climatology.

        Example
        -------
        >>> import xarray as xr
        >>> import sys
        >>> sys.path.insert(1, '/home/mlalande/notebooks/utils')
        >>> import utils as u
        >>>
        >>> da = xr.open_dataarray(...)
        >>> clim = u.clim(da, season='annual', calendar='360_day')

    """

    # Get month lenght
    month_length = xr.DataArray(
        get_dpm(ds.time.to_index(), calendar=calendar),
        coords=[ds.time],
        name='month_length'
    )

    # Annual case
    if season in ['annual', 'Annual']:
        weights = month_length / month_length.sum()
        np.testing.assert_allclose(weights.sum().values, np.ones(1))
        with xr.set_options(keep_attrs=True):
            clim = (ds * weights) \
                .sum(dim='time', skipna=skipna) \
                .assign_coords(season=season)

    # Season case:
    # - single month: int (ex: 1 for January, 2 for February, etc.)
    # - following months: str (ex: 'DJF', 'JJAS', etc.)
    else:
        month = ds['time.month']

        if isinstance(season, int):
            season_sel = (month == season)
        elif isinstance(season, str) and len(season) > 1:
            season_str = 'JFMAMJJASONDJFMAMJJASOND'

            month_start = season_str.index(season) + 1
            month_end = month_start + len(season) - 1

            if month_end > 12:
                month_end -= 12
                season_sel = (month >= month_start) | (month <= month_end)
            else:
                season_sel = (month >= month_start) & (month <= month_end)

        else:
            raise ValueError(
                f"""Invalid season argument: '{season}'. Valid values are:
                - 'annual'"
                - single month: int (ex: 1 for January, 2 for February, etc.)
                - any character string (ex: 'DJF', 'JJAS', etc.)")
                """
            )

        seasonal_data = ds.sel(time=season_sel)
        weights = month_length \
            .sel(time=season_sel) / month_length.astype(float) \
            .sel(time=season_sel) \
            .sum()

        np.testing.assert_allclose(weights.sum().values, np.ones(1))

        with xr.set_options(keep_attrs=True):
            clim = (seasonal_data * weights) \
                .sum(dim='time', skipna=skipna) \
                .assign_coords(season=season)

    # Add period attribute
    clim.attrs['period'] = str(
        ds[0]['time.year'].values) + '-' + str(ds[-1]['time.year'].values)

    return clim


# Yearly mean (on monthly data set)
def year_mean(da, calendar='standard', season='annual', skipna=False):
    # season = 'DJF' can be string
    # season = 1 or int for a single month

    month_length = xr.DataArray(
        get_dpm(
            da.time.to_index(),
            calendar=calendar),
        coords=[
            da.time],
        name='month_length')

    # Deal with custom season (string or int for single month)
    month = da['time.month']

    if isinstance(season, int):
        season_sel = (month == season)
        with xr.set_options(keep_attrs=True):
            season_mean = da.sel(time=season_sel)

    elif isinstance(season, str) and len(season) > 1:

        if season in ['annual', 'Annual']:
            normalize = month_length.astype(float).groupby('time.year').sum()
            weights = month_length.groupby('time.year') / normalize
            np.testing.assert_allclose(
                weights.groupby('time.year').sum().values, np.ones(
                    normalize.year.size))
            with xr.set_options(keep_attrs=True):
                season_mean = (da * weights) \
                    .groupby('time.year') \
                    .sum(dim='time', skipna=skipna)

        else:
            season_str = 'JFMAMJJASONDJFMAMJJASOND'

            month_start = season_str.index(season) + 1
            month_end = month_start + len(season) - 1

            if month_end > 12:
                # Remove one year
                # (.isel(time=slice(month_end,-(12-month_start+1)))) to have
                # continious months
                # The month/year label is from the starting month

                # Checked with cdo: !cdo yearmonmean -selmon,10,11,12\
                # -shifttime,-2mo in.nc out.nc
                # -> slight differences, is CDO do not take the right month
                # weights when shifted?
                # -> or do I use the wrong weights?
                # https://code.mpimet.mpg.de/boards/1/topics/826
                #
                # !cdo yearmean -selmon,10,11,12 -shifttime,-2mo in.nc out.nc
                # Same results with the calendar=360_day
                #
                # Try with cdo season selection?

                # https://pandas.pydata.org/pandas-docs/stable/user_guide/\
                # timeseries.html#dateoffset-objects

                month_end -= 12
                season_sel = (month >= month_start) | (month <= month_end)

                seasonal_data = da.sel(time=season_sel).isel(
                    time=slice(month_end, -(12 - month_start + 1)))

                seasonal_month_length = month_length.astype(float)\
                    .sel(time=season_sel)\
                    .isel(time=slice(month_end, -(12 - month_start + 1)))

                weights = xr.DataArray(
                    [
                        value / seasonal_month_length.resample(
                            time='AS-' + cld.month_abbr[month_start].upper()
                        ).sum().values[i // len(season)]
                        for i, value in enumerate(seasonal_month_length.values)
                    ],
                    coords=[
                        month_length.sel(time=season_sel).isel(
                            time=slice(month_end, -(12 - month_start + 1))
                        ).time
                    ],
                    name='weights'
                )

                sum_weights = weights.resample(
                    time='AS-' + cld.month_abbr[month_start].upper()).sum()

                np.testing.assert_allclose(
                    sum_weights.values, np.ones(
                        sum_weights.size))

                with xr.set_options(keep_attrs=True):
                    season_mean = (seasonal_data * weights) \
                        .resample(time='AS-' + cld.month_abbr[month_start].upper())  \
                        .sum('time', skipna=skipna)

                # To keep same format as the version bellow (be aware that the
                # year label will be from the first month)
                season_mean = season_mean.assign_coords(
                    {"time": season_mean['time.year']})
                season_mean = season_mean.rename({'time': 'year'})

            else:
                # Checked with CDO (!cdo yearmonmean -selmonth,'' in.nc out.nc)
                season_sel = (month >= month_start) & (month <= month_end)
                seasonal_data = da.sel(time=season_sel)
                normalize = month_length.astype(float).sel(
                    time=season_sel).groupby('time.year').sum()
                weights = month_length.sel(
                    time=season_sel).groupby('time.year') / normalize
                np.testing.assert_allclose(
                    weights.groupby('time.year').sum().values, np.ones(
                        normalize.size))
                with xr.set_options(keep_attrs=True):
                    season_mean = (seasonal_data * weights) \
                        .groupby('time.year') \
                        .sum('time', skipna=skipna)

    else:
        raise ValueError(
            'The season is not valid (string or int for single month)')

    return season_mean


# Annual cycle (on monthly data set)
def annual_cycle(ds, calendar='standard', skipna=False):
    month_length = xr.DataArray(
        get_dpm(
            ds.time.to_index(),
            calendar=calendar),
        coords=[
            ds.time],
        name='month_length')
    weights = month_length.groupby(
        'time.month') / month_length.astype(float).groupby('time.month').sum()

    np.testing.assert_allclose(weights.groupby(
        'time.month').sum().values, np.ones(12))

    with xr.set_options(keep_attrs=True):
        return (ds * weights) \
            .groupby('time.month') \
            .sum(dim='time', skipna=skipna)
