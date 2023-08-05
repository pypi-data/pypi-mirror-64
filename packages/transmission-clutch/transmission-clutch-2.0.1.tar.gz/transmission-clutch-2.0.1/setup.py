# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clutch',
 'clutch.method',
 'clutch.method.convert',
 'clutch.method.convert.argument',
 'clutch.method.convert.response',
 'clutch.method.group',
 'clutch.method.typing',
 'clutch.method.typing.session',
 'clutch.method.typing.torrent',
 'clutch.network',
 'clutch.network.rpc']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'transmission-clutch',
    'version': '2.0.1',
    'description': 'An RPC client library for the Transmission BitTorrent client',
    'long_description': 'Clutch\n--------\n\n.. image:: https://readthedocs.org/projects/clutch/badge/?version=latest\n    :target: https://clutch.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://img.shields.io/pypi/v/transmission-clutch.svg?style=flat-square\n    :target: https://pypi.org/project/transmission-clutch\n\n.. image:: https://img.shields.io/pypi/pyversions/transmission-clutch.svg?style=flat-square\n    :target: https://pypi.org/project/transmission-clutch\n\n.. image:: https://img.shields.io/badge/license-BSD-blue.svg?style=flat-square\n    :target: https://en.wikipedia.org/wiki/BSD_License\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\nQuick start\n===========\n\nInstall the package:\n\n::\n\n$ pip install transmission-clutch\n\nRunning the client is as easy as:\n\n::\n\n>>> from clutch.client import Client\n>>> client = Client(address="http://localhost:9091/transmission")\n\nIf you find the client isn\'t connecting, make sure you\'re entering the address correctly. Reference `urllib.parse.urlparse`_ for parsing rules.\n\n.. _urllib.parse.urlparse: https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse\n\nRPC methods are separated into groups: torrent, session, queue and misc.\n\nMethods are called by first specifying a group:\n\n::\n\n>>> client.torrent.add(...)\n',
    'author': 'mhadam',
    'author_email': 'michael@hadam.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
