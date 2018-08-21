"""Main application."""
import os
import sys
import argparse
import json
import yaml
# from google.cloud import monitoring_v3
# from google.oauth2 import service_account

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


def main():
    """Main routine."""
    args_dict = vars(PARSER.parse_args())

    if args_dict['version']:
        print(version())
        return 0

    if not args_dict['project']:
        error('--project not specified')

    if not args_dict['privatekeyid']:
        error('--privatekeyid not specified')

    if not args_dict['privatekey']:
        error('--privatekey not specified')

    if not args_dict['clientid']:
        error('--clientid not specified')

    project_id = args_dict['project']
    private_key_id = args_dict['privatekeyid']
    private_key = args_dict['privatekey']
    private_key = private_key.replace('\\n', '\n')
    client_email = 'lbn-monitoring@' + project_id + '.iam.gserviceaccount.com'
    client_x509_cert_url = 'https://www.googleapis.com/robot/v1/metadata/x509/lbn-monitoring%40' + project_id + '.iam.gserviceaccount.com'
    client_id = args_dict['clientid']
    keyfile_name = 'keyfiles/' + project_id + '.json'

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

    print('keyfile:\n{}'.format(KEYFILE))

    with open(keyfile_name, 'w') as fp:
        json.dump(KEYFILE, fp)

    # if not args_dict['keyfile']:
    #     client = monitoring_v3.MetricServiceClient()
    # else:
    #     credentials = service_account.Credentials.from_service_account_file(args_dict['keyfile'])
    #     client = monitoring_v3.MetricServiceClient(credentials=credentials)

    if args_dict['service']:
        service = args_dict['service']
    else:
        service = ''

    metrics_list = yaml.load(open('metrics_list.yaml'))
    if service:
        print('metrics list for "{}":'.format(service))
        # print(metrics_list[service])
        for metric in metrics_list[service]:
            print('- {}'.format(metric))
    else:
        print('metrics list:')
        for key in metrics_list:
            print(key)
            # print(metrics_list[key])
            for metric in metrics_list[key]:
                print('- {}'.format(metric))
    return 0


if __name__ == "__main__":
    sys.exit(main())
