"""Main application."""
import os
import sys
# import time
import argparse
from google.cloud import monitoring_v3
# from google.cloud.monitoring_v3 import query

# pylint: disable-msg=line-too-long
# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=too-many-locals


PARSER = argparse.ArgumentParser(
    description='Google Cloud Monitoring API Command Line\nWebsite: https://github.com/acladenb5/gcpmetricsv3',
    formatter_class=argparse.RawDescriptionHelpFormatter
)

PARSER.add_argument('--version', default=None, action='store_true', help='Print gcpmetics version and exit.')
PARSER.add_argument('--init-config', help='Location of configuration files.', metavar='DIR')
PARSER.add_argument('--config', help='Local configuration *.yaml file to be used.', metavar='FILE')
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


def list_resource_descriptors(client):
    """List the resource descriptors."""
    print(client)
    return 0


def list_metric_descriptors(client):
    """List the metrics."""
    print(client)
    return 0


def perform_query(client, metric_id, days, hours, minutes, resource_filter, metric_filter, align, reduce, grouping, iloc00):
    """Perform a query."""
    print(client, metric_id, days, hours, minutes, resource_filter, metric_filter, align, reduce, grouping, iloc00)
    return 0


def process(project_id, list_resources, list_metrics, query, metric_id, days, hours, minutes,
            resource_filter, metric_filter, align, reduce, reduce_grouping, iloc00):
    """Process the request."""

    if not project_id:
        error('--project not specified')

    client = monitoring_v3.MetricServiceClient()
    client.project_path(project_id)

    if list_resources:
        list_resource_descriptors(client)

    elif list_metrics:
        list_metric_descriptors(client)

    elif query:
        perform_query(client, metric_id, days, hours, minutes,
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
