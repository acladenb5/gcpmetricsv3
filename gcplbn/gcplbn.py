"""Main application."""
import os
import sys
import argparse
import yaml

# pylint: disable-msg=line-too-long
# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=too-many-locals
# pylint: disable-msg=broad-except
# pylint: disable-msg=too-many-branches
# pylint: disable-msg=protected-access
# pylint: disable-msg=too-many-statements
# pylint: disable-msg=duplicate-code


PARSER = argparse.ArgumentParser(
    description="Get metrics from GCP",
    formatter_class=argparse.RawDescriptionHelpFormatter
)

PARSER.add_argument("--version", default=None, action='store_true', help='Print gcpmetics version and exit.')
PARSER.add_argument('--project', help='Project ID.', metavar='ID')
PARSER.add_argument('--service', help='Cloud service to check', metavar='SVC')


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

    if args_dict['service']:
        service = args_dict['service']
    else:
        service = ''

    metrics_list = yaml.load(open('metrics_list.yaml'))
    if service:
        print('metrics list for {}:'.format(service))
        print(metrics_list[service])
    else:
        print('metrics list:')
        for key in metrics_list:
            print(key)
            print(metrics_list[key])
    return 0


if __name__ == "__main__":
    sys.exit(main())
