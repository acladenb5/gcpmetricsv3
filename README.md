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

4. Set the variables in the wrapper script and copy it to the directory of your chosing.

VENV_DIR is the path to the virtualenv you created in step 1
GCP_METRICS_DIR is the path where you cloned the git repository

Example:
```
VENV_DIR="/opt/venvs/gcpmonitenv"
GCP_METRICS_DIR="/opt/scripts/python"
```

## Usage


