# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wcf', 'wcf.records']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wcf',
    'version': '0.5.5',
    'description': 'A library for transforming wcf-binary data from and to xml',
    'long_description': '# python-wcfbin [![Build Status](https://travis-ci.com/caiyunapp/python-wcfbin.svg?branch=master)](https://travis-ci.com/caiyunapp/python-wcfbin)\n\nA python library for converting between WCF binary xml and plain xml.\n\nA more complete documentation could be found in the doc directory (build with sphinx).\n\n## Install\n\n```sh\n# Install from GitHub\npip install git+https://github.com/caiyunapp/python-wcfbin.git@0.5.4#egg=wcf-binary-parser\n\n# Install from PyPi\npip install wcf\n```\n\n## About\n\n* [contributors](https://github.com/caiyunapp/python-wcfbin/graphs/contributors)\n',
    'author': 'BlueC0re',
    'author_email': 'coding@bluec0re.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/caiyunapp/python-wcfbin',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
