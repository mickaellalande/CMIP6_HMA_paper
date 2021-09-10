# Climate change in the High Mountain Asia in CMIP6

This repository gathers the code used to make the analyses of the paper published in Earth System Dynamics (ESD):

>Lalande, M., Ménégoz, M., Krinner, G., Naegeli, K., and Wunderle, S.: Climate change in the High Mountain Asia in CMIP6, Earth Syst. Dynam. Discuss. [preprint], https://doi.org/10.5194/esd-2021-43, in review, 2021.

## Abstract
Climate change over High Mountain Asia (HMA, including the Tibetan Plateau) is investigated over the period 1979–2014 and in future projections following the four shared socioeconomic pathways SSP1-2.6, SSP2-4.5, SSP3-7.0 and SSP5-8.5. The skill of 26 CMIP6 models is estimated for near-surface air temperature, snow cover extent and total precipitation, and 10 of them are used to describe their projections until 2100. Similarly to previous CMIP models, this new generation of GCMs shows a mean cold bias over this area reaching −1.9 [−8.2 to 2.9] °C (90 % confidence interval) in comparison with the CRU observational dataset, associated with a snow cover mean overestimation of 12 [−13 to 43] %, corresponding to a relative bias of 52 [−53 to 183] % in comparison with the NOAA CDR satellite dataset. The temperature and snow cover model biases are more pronounced in winter. Simulated precipitation rates are overestimated by 1.5 [0.3 to 2.9] mm day−1, corresponding to a relative bias of 143 [31 to 281] %, but this might be an apparent bias caused by the undercatch of solid precipitation in the APHRODITE observational reference. For most models, the cold surface bias is associated with an overestimation of snow cover extent, but this relationship does not hold for all models, suggesting that the processes of the origin of the biases can differ from one model to another one. A significant correlation between snow cover bias and surface elevation is found, and to a lesser extent between temperature bias and surface elevation, highlighting the model weaknesses at high elevation. The models performing the best for temperature are not necessarily the most skillful for the other variables, and there is no clear relationship between model resolution and model skill. This highlights the need for a better understanding of the physical processes driving the climate in this complex topographic area, as well as for further parameterization developments adapted to such areas. A dependency of the simulated past trends to the model biases is found for some variables and seasons, however, some highly biased models fall within the range of observed trends suggesting that model bias is not a robust criterion to discard models in trend analysis. The HMA median warming simulated over 2081–2100 with respect to 1995–2014 ranges from 1.9 [1.2 to 2.7] °C for SSP1-2.6 to 6.5 [4.9 to 9.0] °C for SSP5-8.5. This general warming is associated with a relative median snow cover extent decrease from −9.4 [−16.4 to −5.0] % to −32.2 [−49.1 to −25.0] % and a relative median precipitation increase from 8.5 [4.8 to 18.2] % to 24.9 [14.4 to 48.1] % by the end of the century in these respective scenarios. The warming is 11 % higher over HMA than over the other Northern Hemisphere continental surfaces excluding the Arctic area. Seasonal temperature, snow cover and precipitation changes over HMA show a linear relationship with the Global Surface Air Temperature (GSAT), except for summer snow cover that shows a slower decrease at strong levels of GSAT.

## Code

All analyses were done on the CICLAD server (CLIMERI-France infrastructure: http://climeri-france.fr/). The scripts are therefore not directly reproducible. To retrieve CMIP6 data, you can use, for example, the ESGF portal (https://esgf-node.llnl.gov/search/cmip6/) or [Intake](https://intake-esm.readthedocs.io/en/latest/user-guide/cmip6-tutorial.html) (see example: [intake.ipynb](intake.ipynb)). The paths will of course have to be adapted. I use some personal functions that you can find in the [utils](utils) folder. The environment used is the `phd_v3` of the [envs](envs/phd) folder. To see the detailed history, you can refer to my personal repository: https://github.com/mickaellalande/PhD/tree/master/CICLAD/Himalaya/CMIP6_HMA_paper.

The number of the Figures does not necessarily correspond to the number in the article. Here are the notebooks corresponding to the Figures in the article :

- Figure 1: [fig1_topo-clim.ipynb](fig1_topo-clim.ipynb)

[<img src="img/fig1_topo-cllim_1979-2014.jpg" alt="Figure 1" width="300"/>](fig1_topo-clim.ipynb)


- Figure 2: [fig5_annual-cycles.ipynb](fig5_annual-cycles.ipynb)

[<img src="img/fig5_ac_all_1979-2014.jpg" alt="Figure 2" width="300"/>](fig5_annual-cycles.ipynb)


- Figure 3, B1, B2: [fig2_tas-bias.ipynb](fig2_tas-bias.ipynb), [figS1_snc-bias.ipynb](figS1_snc-bias.ipynb), [figS2_pr-bias.ipynb](figS2_pr-bias.ipynb)

[<img src="img/fig2_Annual_clim_bias_tas_1979-2014.jpg" alt="Figure 3" width="300"/>](fig2_tas-bias.ipynb)
[<img src="img/fig2_Annual_clim_bias_snc_1979-2014.jpg" alt="Figure B1" width="300"/>](figS1_snc-bias.ipynb)
[<img src="img/fig2_Annual_clim_bias_pr_1979-2014.jpg" alt="Figure B2" width="300"/>](figS2_pr-bias.ipynb)


- Figure 4, C1, C2, C3: [fig3_s3_correlations.ipynb](fig3_s3_correlations.ipynb), [fig3_s3_correlations-zones.ipynb](fig3_s3_correlations-zones.ipynb)

[<img src="img/fig3_correlations_1979-2014.jpg" alt="Figure 4" width="300"/>](fig3_s3_correlations.ipynb)
[<img src="img/figS3_correlations_GPCP_1979-2014.jpg" alt="Figure C1" width="300"/>](fig3_s3_correlations.ipynb)

[<img src="img/fig3_seasonal_correlations_HK_1979-2014.jpg" alt="Figure C2" width="300"/>](fig3_s3_correlations-zones.ipynb)
[<img src="img/fig3_seasonal_correlations_TP_1979-2014.jpg" alt="Figure C3" width="300"/>](fig3_s3_correlations-zones.ipynb)


- Figure 5: [fig4_metrics.ipynb](fig4_metrics.ipynb)

[<img src="img/fig4_metrics_Annual_1979-2014.jpg" alt="Figure 5" width="300"/>](fig4_metrics.ipynb)


- Figure 6: [fig_taylor_diagram-PCC.ipynb](fig_taylor_diagram-PCC.ipynb)

[<img src="img/fig_taylor_diagram_Annual_PCC_1979-2014.jpg" alt="Figure 6" width="300"/>](fig_taylor_diagram-PCC.ipynb)


- Figure 7, D1, D2, D3, 8: [fig6-7_S4-6_seasonal-trends.ipynb](fig6-7_S4-6_seasonal-trends.ipynb)

[<img src="img/fig6_seasonal-trends_1979-2014_v2_80.jpg" alt="Figure 7" width="300"/>](fig6-7_S4-6_seasonal-trends.ipynb)
[<img src="img/figS4_tas_obs_seasonal-trends_1979-2014_v2_80.jpg" alt="Figure D1" width="300"/>](fig6-7_S4-6_seasonal-trends.ipynb)

[<img src="img/figS5_snc_obs_seasonal-trends_1979-2014_v2_80.jpg" alt="Figure D2" width="300"/>](fig6-7_S4-6_seasonal-trends.ipynb)
[<img src="img/figS6_pr_obs_seasonal-trends_1979-2014_v2_80.jpg" alt="Figure D3" width="300"/>](fig6-7_S4-6_seasonal-trends.ipynb)

[<img src="img/fig7_trends-vs-bias_1979-2014_v2.jpg" alt="Figure 8" width="300"/>](fig6-7_S4-6_seasonal-trends.ipynb)


- Figure 9: [fig8_projections.ipynb](fig8_projections.ipynb)

[<img src="img/fig8_HMA_annual_projections_v1.jpg" alt="Figure 9" width="300"/>](fig8_projections.ipynb)


- Figure 10: [fig9_spatial_projections.ipynb](fig9_spatial_projections.ipynb)

[<img src="img/fig9_spatial-projections_seasonal.jpg" alt="Figure 10" width="300"/>](fig9_spatial_projections.ipynb)


- Figure 11: [fig10_global_vs_HMA.ipynb](fig10_global_vs_HMA.ipynb)

[<img src="img/fig10_HMA-vs-global.jpg" alt="Figure 11" width="300"/>](fig10_global_vs_HMA.ipynb)


## Data availability
- CMIP6: https://esgf-node.llnl.gov/search/cmip6/
- CRU TS (Climatic Research Unit gridded Time Series) version 4.00: http://doi.org/10/gbr3nj
- NOAA Climate Data Record (CDR) of Northern Hemisphere (NH) Snow Cover Extent (SCE), Version 1: https://doi.org/10.7289/V5N014G9
- ESA CCI snow product: https://catalogue.ceda.ac.uk/uuid/5484dc1392bc43c1ace73ba38a22ac56 (the cloud gap filter used in this study can be provided upon request)
- APHRODITE V1101 (1951-2007) and V1101EX_R1 (2007-2015) domain Monsoon Asia (MA) at a 0.5° resolution: http://aphrodite.st.hirosaki-u.ac.jp/download/
- Global Precipitation Climatology Project (GPCP) Climate Data Record (CDR), Version 2.3 (Monthly): https://doi.org/10.7289/V56971M6
- Global Multi-resolution Terrain Elevation Data 2010 (GMTED2010): https://www.temis.nl/data/gmted2010/index.php
- GLDAS Land/Sea Mask Dataset at 1°: https://ldas.gsfc.nasa.gov/gldas/vegetation-class-mask
- ERA-Interim: https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era-interim  
- ERA5: https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5
