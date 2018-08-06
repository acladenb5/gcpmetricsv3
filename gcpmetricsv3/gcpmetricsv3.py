"""Main application."""
# import os
import sys
# import time
import argparse
# from google.cloud import monitoring_v3
# from google.cloud.monitoring_v3 import query

# pylint: disable-msg=line-too-long

PARSER = argparse.ArgumentParser(
    description='Google Cloud Monitoring API Command Line',
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
