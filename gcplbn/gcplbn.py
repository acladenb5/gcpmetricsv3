"""Main application."""
# import os
import sys
import argparse

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

def main():
    """Main routine."""
    return 0


if __name__ == "__main__":
    sys.exit(main())
