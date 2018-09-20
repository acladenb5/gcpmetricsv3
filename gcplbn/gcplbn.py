"""Main application."""
import os
import sys
import datetime
import argparse
import json
import yaml
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import query
from google.oauth2 import service_account

# pylint: disable-msg=line-too-long
# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=too-many-locals
# pylint: disable-msg=broad-except
# pylint: disable-msg=too-many-branches
# pylint: disable-msg=protected-access
# pylint: disable-msg=too-many-statements
# pylint: disable-msg=duplicate-code
# pylint: disable-msg=invalid-name
# pylint: disable-msg=bare-except


PARSER = argparse.ArgumentParser(
    description="Get metrics from GCP",
    formatter_class=argparse.RawDescriptionHelpFormatter
)

PARSER.add_argument("--version", default=None, action='store_true', help='Print gcpmetics version and exit.')
PARSER.add_argument('--keydir', help='Directory where keyfiles are stores (no trailing "/")', metavar='KEYDIR', required=True)
PARSER.add_argument('--keyfile', help='Goolge Cloud Platform service account key file.', metavar='KEYFILE', required=True)
PARSER.add_argument('--project', help='Project ID.', metavar='PROJECT_ID', required=True)
PARSER.add_argument('--service', help='Cloud service to check', metavar='SERVICE', required=True)
# PARSER.add_argument('--privatekeyid', help='Private key ID', metavar='PKID')
# PARSER.add_argument('--privatekey', help='Private key content', metavar='PKC')
# PARSER.add_argument('--clientid', help='Client ID', metavar='CID')
# PARSER.add_argument('--serviceaccount', help='Service account for the project', metavar='SVCACC')
PARSER.add_argument('--lbnref', help='LBNREF to query', metavar='LBNREF', required=True)
# PARSER.add_argument('--hostname', help='Host', metavar='HOST')

# KEYSRCDIR = '/etc/gcpmonitoring/keysfiles'


def error(message):
    """Display an error message and exit."""
    sys.stderr.write('error: {}'.format(message))
    print()
    print()
    PARSER.print_help()
    sys.exit(1)


def version():
    """Print version."""
    _path = os.path.split(os.path.abspath(__file__))[0]
    _file = os.path.join(_path, './VERSION')
    fversion = open(_file, 'r')
    ver = fversion.read()
    fversion.close()
    return ver.strip()


def perform_query(client, project, metric_id, minutes, lbnref):
    """Perform a query."""
    if minutes == 0:
        error('No time interval specified. Please specify the number of minutes')

    req = query.Query(client, project, metric_type=metric_id, end_time=None, days=0, hours=0, minutes=minutes)

    filt = req._filter
    filt = str(filt) + ' AND metadata.user_labels.lbnref="' + lbnref + '"'
    req._filter = filt

    delta = datetime.timedelta(days=0, hours=0, minutes=minutes)
    seconds = int(delta.total_seconds())
    req = req.align('ALIGN_MEAN', seconds=seconds)

    try:
        dataframe = req.as_dataframe()
    except Exception:
        return json.dumps({'error': 'problem aligning'})

    return dataframe.unstack(level=0).to_json(orient='table')


def main():
    """Main routine."""
    args_dict = vars(PARSER.parse_args())

    if args_dict['version']:
        print(version())
        return 0

    if not args_dict['lbnref']:
        error('--lbnref not specified')
    else:
        lbnref = args_dict['lbnref']

    # if not args_dict['hostname']:
    #     error('--hostname not specified')
    # else:
    #     host = args_dict['hostname']

    if not args_dict['keydir']:
        error('--keydir not specified')
    else:
        keydir = args_dict['keydir']
        if not os.path.isdir(keydir):
            error('--keydir must be an existing directory')

    if not args_dict['keyfile']:
        error('--keyfile not specified')
    else:
        keyfile = keydir + '/' + args_dict['keyfile']
        if not os.path.isfile(keyfile):
            error('--keyfile does not exist')

    if not args_dict['project']:
        error('--project not specified')

    if not args_dict['service']:
        error('--service not specified')

    project_id = args_dict['project']
    keyfile_name = 'keyfiles/' + project_id + '.json'

    # if not args_dict['privatekeyid']:
    #     error('--privatekeyid not specified')

    # if not args_dict['privatekey']:
    #     error('--privatekey not specified')

    # if not args_dict['clientid']:
    #     error('--clientid not specified')

    # if args_dict['serviceaccount']:
    #     svc_account = args_dict['serviceaccount']
    # else:
    #     svc_account = 'lbn-monitoring'

    # private_key_id = args_dict['privatekeyid']
    # private_key = args_dict['privatekey']
    # private_key = private_key.replace('\\n', '\n')
    # client_email = svc_account + '@' + project_id + '.iam.gserviceaccount.com'
    # client_x509_cert_url = 'https://www.googleapis.com/robot/v1/metadata/x509/' + svc_account + '%40' + project_id + '.iam.gserviceaccount.com'
    # client_id = args_dict['clientid']

    # KEYFILE = {'type': 'service_account',
    #            'project_id': project_id,
    #            'private_key_id': private_key_id,
    #            'private_key': private_key,
    #            'client_email': client_email,
    #            'client_id': client_id,
    #            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    #            'token_uri': 'https://oauth2.googleapis.com/token',
    #            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
    #            'client_x509_cert_url': client_x509_cert_url}

    # with open(keyfile_name, 'w') as fp:
    #     json.dump(KEYFILE, fp)
    #     fp.close()

    # credentials = service_account.Credentials.from_service_account_file(keyfile_name)
    credentials = service_account.Credentials.from_service_account_file(keyfile)
    client = monitoring_v3.MetricServiceClient(credentials=credentials)

    service = args_dict['service']

    metrics_list = yaml.load(open('metrics_list.yaml'))

    if service not in metrics_list:
        print('ERROR: service "{}" is not in the services list'.format(service))
        return 1

    arr_metrics = []
    exp_metrics = dict()

    for metric in metrics_list[service]:
        metr = metric.split('/')
        family = metr[0]
        metri = '/'.join(metr[1:])
        # ret_msg = lbnref + ' - ' + family + '[' + metri + '] '
        ret_msg = '- ' + family + '[' + metri + '] '
        arrkeysdict = perform_query(client, project_id, metric, 5, lbnref)
        exp_metrics['metric'] = metric
        exp_metrics['data'] = json.loads(arrkeysdict)
        try:
            ret_msg += str(exp_metrics['data']['data'][0]['values'])
        except:
            ret_msg += 'ERROR READING METRIC'
        arr_metrics.append(exp_metrics)
        print(ret_msg)

    # print(json.dumps(arr_metrics))
    return 0


if __name__ == "__main__":
    sys.exit(main())
