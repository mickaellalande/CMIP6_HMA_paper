#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autopep8: https://pypi.org/project/autopep8/
# Check with http://pep8online.com/


# =============================================================================
# Select model on CICLAD
# =============================================================================
def get_model_infos(name, var):
    if name in ['ACCESS-CM2']:
        institude = 'CSIRO-ARCCSS'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = 'proleptic_gregorian'

    elif name in ['ACCESS-ESM1-5']:
        institude = 'CSIRO'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = 'proleptic_gregorian'

    elif name in ['AWI-CM-1-1-MR']:
        institude = 'AWI'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = 'proleptic_gregorian'

    elif name in ['BCC-CSM2-MR', 'BCC-ESM1']:
        institude = 'BCC'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = '365_day'

    elif name in ['CAMS-CSM1-0']:
        institude = 'CAMS'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = '365_day'

    elif name in ['CAS-ESM2-0']:
        institude = 'CAS'
        grid = 'gn'
        member = 'r4i1p1f1'  # other members not present for pr
        calendar = '365_day'

    elif name in ['CESM2', 'CESM2-FV2', 'CESM2-WACCM', 'CESM2-WACCM-FV2']:
        institude = 'NCAR'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = 'noleap'

    elif name in ['CIESM']:
        institude = 'THU'
        grid = 'gr'
        member = 'r1i1p1f1'
        calendar = '365_day'

    elif name in ['CNRM-CM6-1', 'CNRM-CM6-1-HR', 'CNRM-ESM2-1']:
        institude = 'CNRM-CERFACS'
        grid = 'gr'
        member = 'r1i1p1f2'
        calendar = 'gregorian'

    elif name in ['CanESM5', 'CanESM5-CanOE']:
        institude = 'CCCma'
        grid = 'gn'
        member = 'r3i1p2f1'
        calendar = '365_day'

    elif name in ['E3SM-1-0', 'E3SM-1-1', 'E3SM-1-1-ECA']:
        institude = 'E3SM-Project'
        grid = 'gr'
        member = 'r1i1p1f1'
        calendar = 'noleap'

    elif name in ['EC-Earth3', 'EC-Earth3-Veg', 'EC-Earth3-Veg-LR']:
        institude = 'EC-Earth-Consortium'
        grid = 'gr'
        if name in ['EC-Earth3']:
            member = 'r2i1p1f1'
        else:
            member = 'r1i1p1f1'
        calendar = 'proleptic_gregorian'

    elif name in ['FGOALS-f3-L', 'FGOALS-g3']:
        institude = 'CAS'
        grid = 'gr'
        if var in ['snc', 'pr']:
            grid = 'gn'
        if var == 'prsn' and name in ['FGOALS-g3']:
            grid = 'gn'
        member = 'r1i1p1f1'
        calendar = '365_day'

    elif name in ['FIO-ESM-2-0']:
        institude = 'FIO-QLNM'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = '365_day'

    elif name in ['GFDL-CM4', 'GFDL-ESM4']:
        institude = 'NOAA-GFDL'
        grid = 'gr1'
        member = 'r1i1p1f1'
        calendar = 'noleap'

    elif name in ['GISS-E2-1-G', 'GISS-E2-1-G-CC', 'GISS-E2-1-H']:
        institude = 'NASA-GISS'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = '365_day'

    elif name in ['HadGEM3-GC31-LL', 'HadGEM3-GC31-MM']:
        institude = 'MOHC'
        grid = 'gn'
        member = 'r1i1p1f3'
        calendar = '360_day'

    elif name in ['INM-CM4-8', 'INM-CM5-0']:
        institude = 'INM'
        grid = 'gr1'
        member = 'r1i1p1f1'
        calendar = '365_day'

    elif name in ['IPSL-CM6A-LR']:
        institude = 'IPSL'
        grid = 'gr'
        member = 'r1i1p1f1'
        calendar = 'gregorian'

    elif name in ['KACE-1-0-G']:
        institude = 'NIMS-KMA'
        grid = 'gr'
        member = 'r1i1p1f1'
        calendar = '360_day'

    elif name in ['MCM-UA-1-0']:
        institude = 'UA'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = 'noleap'

    elif name in ['MIROC-ES2L', 'MIROC6']:
        institude = 'MIROC'
        grid = 'gn'
        if name == 'MIROC6':
            member = 'r1i1p1f1'
        else:
            member = 'r1i1p1f2'
        calendar = 'gregorian'

    elif name in ['MPI-ESM-1-2-HAM']:
        institude = 'HAMMOZ-Consortium'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = 'proleptic_gregorian'

    elif name in ['MPI-ESM1-2-HR', 'MPI-ESM1-2-LR']:
        institude = 'MPI-M'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = 'proleptic_gregorian'

    elif name in ['MRI-ESM2-0']:
        institude = 'MRI'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = 'proleptic_gregorian'

    elif name in ['NESM3']:
        institude = 'NUIST'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = 'standard'

    elif name in ['NorCPM1', 'NorESM2-LM', 'NorESM2-MM']:
        institude = 'NCC'
        grid = 'gn'
        member = 'r2i1p1f1'
        calendar = 'noleap'

    elif name in ['SAM0-UNICON']:
        institude = 'SNU'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = 'noleap'

    elif name in ['TaiESM1']:
        institude = 'AS-RCEC'
        grid = 'gn'
        member = 'r1i1p1f1'
        calendar = 'noleap'

    elif name in ['UKESM1-0-LL']:
        institude = 'MOHC'  # 'NIMS-KMA'
        grid = 'gn'
        member = 'r1i1p1f2'
        calendar = '360_day'

    else:
        raise NameError('The model ' + name + ' is not defined')

    return institude, grid, member, calendar

# This is already a sublist from climaf (tas, snc, pr)


def get_model_names():
    model_list = [
        'BCC-CSM2-MR',
        'BCC-ESM1',
        'CAS-ESM2-0',
        'CESM2',
        'CESM2-FV2',
        'CESM2-WACCM',
        'CESM2-WACCM-FV2',
        #       'CIESM', # Precip too low
        'CNRM-CM6-1',
        'CNRM-CM6-1-HR',
        'CNRM-ESM2-1',
        'CanESM5',
#         'CanESM5-CanOE', # too close from CanESM5
        #       'EC-Earth3', # Missing some years
        #       'EC-Earth3-Veg', # Missing some years
        #       'EC-Earth3-Veg-LR', # Missing some years
        #       'FGOALS-f3-L', # Missing pr
        'GFDL-CM4',
        'GISS-E2-1-G',
        #       'GISS-E2-1-G-CC', # Missing some years for snc
        'GISS-E2-1-H',
        'HadGEM3-GC31-LL',
        'HadGEM3-GC31-MM',
        'IPSL-CM6A-LR',
        'MIROC-ES2L',
        'MIROC6',
        #       'MPI-ESM-1-2-HAM', # Missing some years for snc
        'MPI-ESM1-2-HR',
        'MPI-ESM1-2-LR',
        'MRI-ESM2-0',
        #       'NorCPM1', # Missing latitudes
        'NorESM2-LM',
        #       'NorESM2-MM', # Missing some years for snc
        'SAM0-UNICON',
        'TaiESM1',
        'UKESM1-0-LL'
    ]

    return model_list


def get_model_names_projections():
    model_list = [
        'BCC-CSM2-MR',
        #       'BCC-ESM1',
        #       'CAS-ESM2-0',
#         'CESM2', # plus disponble...
        #       'CESM2-FV2',
        #       'CESM2-WACCM', # /bdd/CMIP6/ScenarioMIP/NCAR/CESM2-WACCM/\
        # ssp585/r1i1p1f1/Amon/pr/gn/latest/ missing years
        #       'CESM2-WACCM-FV2',
        'CNRM-CM6-1',
        'CNRM-CM6-1-HR',
        'CNRM-ESM2-1',
        'CanESM5',
#         'CanESM5-CanOE', # Too similar to CanESM5
        #       'GFDL-CM4',
        #       'GISS-E2-1-G',
        #       'GISS-E2-1-H',
        #       'HadGEM3-GC31-LL', # missing ssp370
        #       'HadGEM3-GC31-MM',
        'IPSL-CM6A-LR',
        'MIROC-ES2L',
        'MIROC6',
        #       'MPI-ESM1-2-HR',
        #       'MPI-ESM1-2-LR', # /bdd/CMIP6/ScenarioMIP/MPI-M/MPI-ESM1-2-LR\
        # /ssp126/r1i1p1f1/Amon/pr/gn/latest/ missing years
        'MRI-ESM2-0',
        #       'NorESM2-LM',
        #       'SAM0-UNICON',
        #       'TaiESM1',
        'UKESM1-0-LL'
    ]

    return model_list
