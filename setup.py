"""Setup."""
from setuptools import setup

#  pylint: disable-msg=invalid-name


config = {
    'description': 'Rewrite of gcpmetrics for monitoring_v3',
    'author': 'A. Claden',
    'author_email': 'acladen@purplespark.org',
    'version': '0.0.1-alpha',
    'install_requires': [
        'flake8',
        'pylint',
        'google-cloud-monitoring',
        'PyYAML',
        'pandas'
    ],
    'scripts': 'gcpmetricsv3',
    'name': 'gcpmetricsv3',
    'packages': ['gcpmetricsv3'],
    'package_dir': {
        'gcpmetricsv3': 'gcpmetricsv3'
    },
    'entry_points': {
        'console_scripts': [
            'gcpmetricsv3=gcpmetricsv3.run:main'
        ]
    }
}

setup(**config)
