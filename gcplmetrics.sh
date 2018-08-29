#!/bin/bash

VENV_DIR="</PATH/TO/VENV>"
GCP_METRICS_DIR="</PATH/TO/REPOSITORY_CLONE>"

source ${VENV_DIR}/bin/activate
python ${GCP_METRICS_PATH}/GCP-Monitoring/gcplbn/gcplbn.py $*
