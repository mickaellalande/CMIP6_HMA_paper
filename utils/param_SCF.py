#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autopep8: https://pypi.org/project/autopep8/
# Check with http://pep8online.com/

# Parameterization SCF


import numpy as np


def scf(param, SWE, rho_snow=100, sigma_topo=0, SWE_max=200):
    """
        Function computing the Snow Cover Fraction (SCF) from the Snow Water
        Equivalent (SWE) from different parameterizations.

        Parameters
        ----------
        param : str
            Parameterization name. Options are:

            - 'NY07': Niu and Yang, 2007
        https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2007JD008674
        
            - 'NY07_STD': custom version of NY07
            
            - 'SL12': Swenson and Lawrence, 2012
        https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2012JD018178
        
            - 'R01': Roesch et al., 2001
        https://link.springer.com/article/10.1007/s003820100153

        SWE : float, array
            Snow Water Equivalent value(s) [mm or kg/m2].

        rho_snow : float, array, optional
            Density of the snow value(s) [kg/m3]. Default is 100 kg/m3.
            
        sigma_topo : float, array, optional
            Standard deviation of the topography [m]. Default is 0 m.
        
        SWE_max : float, array, optional
            Maximum Snow Water Equivalent value(s) [mm or kg/m2]. Default is
            200 km/m2.

        Returns
        -------
        scf : float, array
            Value(s) of SCF.

        Example
        -------
        >>> import sys
        >>> sys.path.insert(1, '/home/mlalande/notebooks/utils')
        >>> import utils as u
        >>> import numpy as np
        >>>
        >>> SWE = np.aragen(0, 150, 1)
        >>> SCF = u.scf(param='NY07', SWE=SWE, rho_snow=300)
    """

    rho_water = 997  # density of water [kg/m3]

    if param == 'NY07':
        #####################
        # Orchidée constant #
        #####################
        z_0g = 0.01  # ground roughness length [m]
        rho_new = 50  # density of the new snow [kg/m3]
        m = 1  # empirical constant

        scf = np.tanh(
            (SWE) / (2.5 * z_0g * rho_snow * (rho_snow / rho_new)**m)
        )
        
    elif param == 'NY07_STD':
        #####################
        # Orchidée constant #
        #####################
        z_0g = 0.01  # ground roughness length [m]
        rho_new = 50  # density of the new snow [kg/m3]
        m = 1  # empirical constant

        scf = np.tanh(
            (SWE) / (2.5 * z_0g * rho_snow * (rho_snow / rho_new)**m * 
                     (1 + sigma_topo / 200) )
        )
        
    elif param == 'SL12':
        epsilon = 1e-6
#         epsilon = 10
#         N_melt = 200 / (sigma_topo + epsilon)
#         N_melt = 200 / (sigma_topo + epsilon)
        N_melt = 200 / np.max([30, sigma_topo])
        
        scf = 1 - ( 1 / np.pi * np.arccos( 2 * SWE / SWE_max - 1 ) )**N_melt
        
    elif param == 'R01':
        epsilon = 1e-6        
        scf = 0.95 * np.tanh(100 * SWE) * np.sqrt(
            ( SWE ) / ( SWE + epsilon + 0.15 * sigma_topo )
        )
        
    else:
        raise ValueError(
            f"Invalid parameterization argument: '{param}'. "
            "Valid names are: 'NY07', 'NY07_STD', 'SL12', 'R01'."
        )

    return scf
