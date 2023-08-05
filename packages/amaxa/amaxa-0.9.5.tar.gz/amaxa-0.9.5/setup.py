# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amaxa', 'amaxa.loader']

package_data = \
{'': ['*']}

install_requires = \
['cerberus>=1.3.2,<2.0.0',
 'cryptography>=2.8,<3.0',
 'pyjwt>=1.7.1,<2.0.0',
 'pyyaml>=5.3,<6.0',
 'requests[security]>=2.23.0,<3.0.0',
 'salesforce_bulk>=2.1.0,<3.0.0',
 'simple_salesforce>=0.75.3,<0.76.0']

entry_points = \
{'console_scripts': ['amaxa = amaxa.__main__:main']}

setup_kwargs = {
    'name': 'amaxa',
    'version': '0.9.5',
    'description': 'Load and extract data from multiple Salesforce objects in a single operation, preserving links and network structure.',
    'long_description': 'Amaxa - a multi-object ETL tool for Salesforce\n==============================================\n\nIntroduction\n------------\n\nAmaxa is a new data loader and ETL (extract-transform-load) tool for Salesforce, designed to support the extraction and loading of complex networks of records in a single operation. For example, an Amaxa operation can extract a designated set of Accounts, their associated Contacts and Opportunities, their Opportunity Contact Roles, and associated Campaigns, and then load all of that data into another Salesforce org while preserving the connections between the records.\n\nAmaxa is designed to replace complex, error-prone workflows that manipulate data exports with spreadsheet functions like ``VLOOKUP()`` to maintain object relationships.\n\nAmaxa is free and open source software, distributed under the BSD License. Amaxa is by `David Reed <https://ktema.org>`_, (c) 2019-2020.\n\nDocumentation for Amaxa is available on `ReadTheDocs <https://amaxa.readthedocs.io>`_. The project is developed on `GitHub <https://github.com/davidmreed/amaxa>`_.\n\nWhat Does Amaxa Mean?\n---------------------\n\n`ἄμαξα <http://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.04.0058%3Aentry%3Da\\)%2Fmaca>`_ is the Ancient Greek word for a wagon.\n',
    'author': 'David Reed',
    'author_email': 'david@ktema.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidmreed/amaxa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
