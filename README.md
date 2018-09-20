# GCP Metrics

## Setup

1. Create a python virtualenv and activate it

```bash
virtualenv -p python3 gcpmonitenv
source gcpmonitenv/bin/activate
```

2. Clone the repository

```bash
git clone https://git.lbn.fr/cloud-gcp/GCP-Monitoring.git
```

3. Install the dependencies

```bash
cd GCP-Monitoring
pip install -r requirements.txt
```

4. Copy it to the directory of your chosing set the variables in the wrapper (gcplmetrics.sh) script and .

```bash
cp gcplmetrics.sh /usr/local/zabbix/scripts
```

Then edit this copy and set the variables.

VENV_DIR is the path to the virtualenv you created in step 1
GCP_METRICS_DIR is the path where you cloned the git repository

Example:
```
VENV_DIR="/opt/venvs/gcpmonitenv"
GCP_METRICS_DIR="/opt/scripts/python"
```

## Usage

```
gcpmetrics.sh --keydir KEYDIR --keyfile KEYFILE --project PROJECT_ID --service SERVICE --lbnref LBNREF
```

Example:
```
/opt/zabbix/gcp/gcpmonitoring.sh --keydir /opt/zabbix/gcp/keys --keyfile lbn-labo.json --project lbn-labo --service cloudsql
```
