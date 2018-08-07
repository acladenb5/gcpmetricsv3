"""Main application."""
import os
import sys
# import time
import argparse
import pprint
from google.cloud import monitoring_v3
# from google.cloud.monitoring_v3 import types as v3types
from google.cloud.monitoring_v3 import query
# from google.cloud.monitoring_v3 import enums
from google.oauth2 import service_account
# from google.cloud.monitoring_v3 import query

# pylint: disable-msg=line-too-long
# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=too-many-locals
# pylint: disable-msg=broad-except


PARSER = argparse.ArgumentParser(
    description='Google Cloud Monitoring API Command Line\nWebsite: https://github.com/acladenb5/gcpmetricsv3',
    formatter_class=argparse.RawDescriptionHelpFormatter
)

PARSER.add_argument('--version', default=None, action='store_true', help='Print gcpmetics version and exit.')
PARSER.add_argument('--init-config', help='Location of configuration files.', metavar='DIR')
# PARSER.add_argument('--config', help='Local configuration *.yaml file to be used.', metavar='FILE')
PARSER.add_argument('--keyfile', help='Goolge Cloud Platform service account key file.', metavar='FILE')
PARSER.add_argument('--preset', help='Preset ID, like http_response_5xx_sum, etc.', metavar='ID')
PARSER.add_argument('--project', help='Project ID.', metavar='ID')
PARSER.add_argument('--list-resources', default=None, action='store_true', help='List monitored resource descriptors and exit.')
PARSER.add_argument('--list-metrics', default=None, action='store_true', help='List available metric descriptors and exit.')
PARSER.add_argument('--query', default=None, action='store_true', help='Run the time series query.')
PARSER.add_argument('--service', help='Service ID.', metavar='ID')
PARSER.add_argument('--metric', help='Metric ID as defined by Google Monitoring API.', metavar='ID')
PARSER.add_argument('--infinite', default=None, action='store_true', help='Calculate time delta since the dawn of time.')
PARSER.add_argument('--days', default=0, help='Days from now to calculate the query start date.', metavar='INT')
PARSER.add_argument('--hours', default=0, help='Hours from now to calculate the query start date.', metavar='INT')
PARSER.add_argument('--minutes', default=0, help='Minutes from now to calculate the query start date.', metavar='INT')
PARSER.add_argument('--resource-filter', default=None, help='Filter of resources in the var:val[,var:val] format.', metavar='S')
PARSER.add_argument('--metric-filter', default=None, help='Filter of metrics in the var:val[,var:val] format.', metavar='S')
PARSER.add_argument('--align', default=None, help='Alignment of data ALIGN_NONE, ALIGN_SUM. etc.', metavar='A')
PARSER.add_argument('--reduce', default=None, help='Reduce of data REDUCE_NONE, REDUCE_SUM, etc.', metavar='R')
PARSER.add_argument('--reduce-grouping', default=None, help='Reduce grouping in the var1[,var2] format.', metavar='R')
PARSER.add_argument('--iloc00', default=None, action='store_true', help='Print value from the table index [0:0] only.')


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


def list_resource_descriptors(client, project):
    """List the resource descriptors."""
    print('Monitored resource descriptors:')
    index = 0
    for descriptor in client.list_monitored_resource_descriptors(project):
        index += 1
        print('Resource descriptor #{}'.format(index))
        print(format(pprint.pformat(descriptor)))
    return 0


def list_metric_descriptors(client, project):
    """List the metrics."""
    print('Defined metric descriptors:')
    index = 0
    for descriptor in client.list_metric_descriptors(project):
        index += 1
        print('Metric descriptor #{}'.format(index))
        print(format(pprint.pformat(descriptor)))
        print()
    return 0


def perform_query(client, project, metric_id, days, hours, minutes, resource_filter, metric_filter, align, reduce, grouping, iloc00):
    """Perform a query."""
    print('----------')
    print(client, project, metric_id, days, hours, minutes, resource_filter, metric_filter, align, reduce, grouping, iloc00)
    print('----------')
    if (days + hours + minutes) == 0:
        error('No time interval specified. Please use --infinite or --days, --hours, --minutes')
    if not metric_id:
        error('Metric ID is required for query, please use --metric')

    # interval = monitoring_v3.types.TimeInterval
    # interval = v3types.duration_pb2
    # now = time.time()
    # interval.end_time.seconds = int(now)
    # interval.end_time.nanos = int((now - interval.end_time.seconds) * 10**9)
    # interval.start_time.seconds = int(now - 60)
    # interval.start_time.nanos = interval.end_time.nanos
    req = query.Query(client, project, metric_type=metric_id, end_time=None, days=days, hours=hours, minutes=minutes)
    try:
        dataframe = req.as_dataframe()
        print(dataframe)
    except Exception as exc:
        print(type(exc))
        print(exc)
        print('Permission denied or Metric does not exist: {}'.format(metric_id))
        exit(-1)
    return 0


def process(keyfile, project_id, list_resources, list_metrics, request, metric_id, days, hours, minutes,
            resource_filter, metric_filter, align, reduce, reduce_grouping, iloc00):
    """Process the request."""

    if not project_id:
        error('--project not specified')

    if not keyfile:
        client = monitoring_v3.MetricServiceClient()
    else:
        credentials = service_account.Credentials.from_service_account_file(keyfile)
        client = monitoring_v3.MetricServiceClient(credentials=credentials)

    project = client.project_path(project_id)

    if list_resources:
        list_resource_descriptors(client, project)

    elif list_metrics:
        list_metric_descriptors(client, project)

    elif request:
        perform_query(client, project, metric_id, days, hours, minutes,
                      resource_filter, metric_filter, align, reduce, reduce_grouping, iloc00)

    else:
        error('No operation specified. Please choose one of --list-resources, --list-metrics, --query')


def process_filter(_filter):
    """Process the filters."""
    if not _filter:
        return None
    _filter = _filter.split(',')
    _ret = {}
    for res in _filter:
        key, value = res.split(':')
        _ret[key] = value
    return _ret


def main():
    """Main routine."""
    args_dict = vars(PARSER.parse_args())

    if args_dict['version']:
        print(version())
        return 0

    # data re-formatting for simpler use going forward
    resource_filter = process_filter(args_dict['resource_filter'])
    metric_filter = process_filter(args_dict['metric_filter'])

    process(
        args_dict['keyfile'],
        # args_dict['config'],
        args_dict['project'],
        args_dict['list_resources'],
        args_dict['list_metrics'],
        args_dict['query'],
        args_dict['metric'],
        int(args_dict['days']),
        int(args_dict['hours']),
        int(args_dict['minutes']),
        resource_filter,
        metric_filter,
        args_dict['align'],
        args_dict['reduce'],
        args_dict['reduce_grouping'],
        args_dict['iloc00']
    )
    return 0


if __name__ == '__main__':
    sys.exit(main())
