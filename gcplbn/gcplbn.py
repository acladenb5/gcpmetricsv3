"""Main application."""
import os
import sys
# import datetime
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


PARSER = argparse.ArgumentParser(
    description="Get metrics from GCP",
    formatter_class=argparse.RawDescriptionHelpFormatter
)

PARSER.add_argument("--version", default=None, action='store_true', help='Print gcpmetics version and exit.')
PARSER.add_argument('--keyfile', help='Goolge Cloud Platform service account key file.', metavar='FILE')
PARSER.add_argument('--project', help='Project ID.', metavar='ID')
PARSER.add_argument('--service', help='Cloud service to check', metavar='SVC')
PARSER.add_argument('--privatekeyid', help='Private key ID', metavar='PKID')
PARSER.add_argument('--privatekey', help='Private key content', metavar='PKC')
PARSER.add_argument('--clientid', help='Client ID', metavar='CID')
PARSER.add_argument('--serviceaccount', help='Service account for the project', metavar='SVCACC')


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


def perform_query(client, project, metric_id, minutes):
    """Perform a query."""
    if minutes == 0:
        error('No time interval specified. Please specify the number of minutes')

    req = query.Query(client, project, metric_type=metric_id, end_time=None, days=0, hours=0, minutes=minutes)

    dataframe = req.as_dataframe()
    # print(dataframe)
    # print(dataframe.values)

    dflen = len(dataframe)
    print('dflen={}'.format(dflen))
    print('number of cols: {}'.format(dataframe.shape[1]))
    # tmp = dataframe.shape[1]
    print(dataframe.keys().levels[0][0])
    print(dataframe.keys().levels[1][0])
    print(dataframe.keys().levels[2][0])
    print(dataframe.keys().levels[3][0])

    print(dataframe.keys().levels[0][0])
    print(dataframe.keys().levels[1][0])
    print(dataframe.keys().levels[2][1])
    print(dataframe.keys().levels[3][1])

    dictret = dict()
    if dflen:
        # counter = 0
        for cnt in range(dflen):
            counter = 0
            print(cnt)
            print('-----')
            for name in dataframe.keys().names:
                try:
                    # print(dataframe.keys().levels[counter][cnt])
                    counter += 1
                    print(counter)
                except IndexError:
                    continue
            print('-----')
        exit(0)
        for name in dataframe.keys().names:
            dictret[name] = dataframe.keys().levels[counter][0]
            counter += 1

        mydict = dataframe.to_dict('record')
        # stuff = list(mydict[0].keys())
        # stufflen = len(stuff) -1

        dictret['metric'] = metric_id
        dictret['val'] = list(mydict[0].values())[0]
    else:
        dictret = {'metric': metric_id, 'val': 'Empty result'}

    print(dictret)
    return 0


def main():
    """Main routine."""
    args_dict = vars(PARSER.parse_args())

    if args_dict['version']:
        print(version())
        return 0

    if not args_dict['project']:
        error('--project not specified')

    if not args_dict['service']:
        error('--service not specified')

    project_id = args_dict['project']
    keyfile_name = 'keyfiles/' + project_id + '.json'

    # if not os.path.isfile(keyfile_name):
    if not args_dict['privatekeyid']:
        error('--privatekeyid not specified')

    if not args_dict['privatekey']:
        error('--privatekey not specified')

    if not args_dict['clientid']:
        error('--clientid not specified')

    if args_dict['serviceaccount']:
        svc_account = args_dict['serviceaccount']
    else:
        svc_account = 'lbn-monitoring'

    private_key_id = args_dict['privatekeyid']
    private_key = args_dict['privatekey']
    private_key = private_key.replace('\\n', '\n')
    client_email = svc_account + '@' + project_id + '.iam.gserviceaccount.com'
    client_x509_cert_url = 'https://www.googleapis.com/robot/v1/metadata/x509/' + svc_account + '%40' + project_id + '.iam.gserviceaccount.com'
    client_id = args_dict['clientid']

    KEYFILE = {'type': 'service_account',
               'project_id': project_id,
               'private_key_id': private_key_id,
               'private_key': private_key,
               'client_email': client_email,
               'client_id': client_id,
               'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
               'token_uri': 'https://oauth2.googleapis.com/token',
               'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
               'client_x509_cert_url': client_x509_cert_url}

    with open(keyfile_name, 'w') as fp:
        json.dump(KEYFILE, fp)
        fp.close()

    credentials = service_account.Credentials.from_service_account_file(keyfile_name)
    client = monitoring_v3.MetricServiceClient(credentials=credentials)

    # print(client)

    service = args_dict['service']

    metrics_list = yaml.load(open('metrics_list.yaml'))

    if service not in metrics_list:
        print('ERROR: service "{}" is not in the services list'.format(service))
        return 1

    # print('metrics list for "{}":'.format(service))
    # print(metrics_list[service])
    for metric in metrics_list[service]:
        # print('- {}'.format(metric))
        perform_query(client, project_id, metric, 5)

    return 0


if __name__ == "__main__":
    sys.exit(main())
