#!/bin/bash

# Save conda environments with different methods
# https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

conda list --explicit > $1.txt
conda env export > $1.yml
conda env export --from-history > $1_fh.yml