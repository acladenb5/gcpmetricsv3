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


PARSER = argparse.ArgumentParser(
    description="Get metrics from GCP",
    formatter_class=argparse.RawDescriptionHelpFormatter
)

PARSER.add_argument("--version", default=None, action='store_true', help='Print gcpmetics version and exit.')


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
    
    metrics_file = open('metrics_list.yaml', 'r')
    # print(metrics_file)
    metrics_list = yaml.load_all(metrics_file)
    print('metrics list:')
    for key in metrics_list:
        print(key['compute'])
    # print(metrics_list)
    metrics_file.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
