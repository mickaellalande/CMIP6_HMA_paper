# Environments

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

- For installing on HPC: https://github.com/mickaellalande/MC-Toolkit/tree/master/conda_environment_xarray_xesmf_proplot
- My xarray environment: https://github.com/mickaellalande/MC-Toolkit/tree/master/conda_environment_xarray_xesmf_proplot/xarray


```bash
conda env list

conda create --name myenv
conda create --name myclone --clone myenv

conda list --explicit > spec-file.txt
conda create --name myenv --file spec-file.txt


conda env export > environment.yml
conda env export --from-history > environment.yml
conda env create -f environment.yml
```

Small bash script to save environment from one environment folder: `sh ../save_env.sh my_env`

---

## PhD environments

- ~~phd_v2~~ (20/07/2020 work -> phd updated version for xarray -> html and proplot -> shading, made on CICLAD)
    - bug with the last version of Matplotlib 3.3 (https://github.com/lukelbd/proplot/issues/210)
- work_v1 (made the 24/06/2020 on Jean-Zay)
- **work** (made on CICLAD -> didn't work on Jean-Zay?)

## CICLAD environments

- **ciclad_v0** (28/07/2020 updated version of my work environment + jupyter-lab + intake)

**Installation**:
```bash
conda create -n ciclad_v0
conda activate ciclad_v0

# Need to install first esmpy separatly (https://github.com/JiaweiZhuang/xESMF/issues/47#issuecomment-582421822)
conda install esmpy
conda install xesmf dask

# Need matplotlib<=3.2 for Proplot (https://github.com/lukelbd/proplot/issues/210)
# Need nodejs>=10.0 for installing dask extension in jupyter-lab
# xarray and other packages already installed with dask previously
conda install jupyter jupyterlab "nodejs>=10.0" psutil netcdf4 proplot cartopy "matplotlib<=3.2" intake-esm python-graphviz

# Fot testing xESMF
pip install pytest  
pytest -v --pyargs xesmf  #all need to pass

# Launch jupyter-lab on your own port (xxxx)
jupyter lab --port xxxx --ip 0.0.0.0 --no-browser

# SSH tunel on your own terminal (with the port + the CICLAD node)
ssh -L xxxx:cicladxx:xxxx login@ciclad2.ipsl.jussieu.fr

# Problem with dask extension
404 GET /dask/clusters?1595927028221 (172.20.3.252) 4.28ms referer=http://127.0.0.1:7227/lab

# New tunel for dask
ssh -L 8787:cicladxx:8787 login@ciclad2.ipsl.jussieu.fr

```
---
## Proplot environments
- proplot_v0.6.4 (20/07/2020 for testing bar bug)

## Xarray environments
- xarray_v0.16.0 (21/07/2020 for testing time.encoding bug)

## ScipyConf environments
- scipyconf2020 (21/07/2020 for [SciPyConf 2020 tutorials](https://www.scipy2020.scipy.org/tutorial-information) + [videos](https://www.youtube.com/playlist?list=PLYx7XA2nY5Gde-6QO98KUJ9iL_WW4rgYf))

## Intake-esm
- 