#!/bin/bash

VENV_DIR="/PATH/TO/VENV"
GCP_METRICS_DIR="/PATH/TO/REPOSITORY_CLONE"

# ----- DO NOT EDIT BELOW THIS LINE ----- #
source ${VENV_DIR}/bin/activate
cd ${GCP_METRICS_DIR}/GCP-Monitoring
python gcplbn/gcplbn.py $*
