#!/bin/bash

export VENV_DIR="/home/zabbix/GCP-Monitoring/gcpmonitenv"
export GCP_METRICS_DIR="/home/zabbix/GCP-Monitoring"

OUT=$(mktemp /tmp/output.XXXXXXXXXX) || { echo "1"; exit 1; }

# ----- DO NOT EDIT BELOW THIS LINE ----- #
source ${VENV_DIR}/bin/activate
cd ${GCP_METRICS_DIR}
python gcplbn/gcplbn.py $* > $OUT
zabbix_sender -z localhost -i $OUT 2>&1 >/dev/null 
if [ "$?" -ne "0" ] ; then
	echo 1
else
	echo 0
fi
rm $OUT
