# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['risc']

package_data = \
{'': ['*'],
 'risc': ['.mypy_cache/3.8/*',
          '.mypy_cache/3.8/collections/*',
          '.mypy_cache/3.8/email/*',
          '.mypy_cache/3.8/http/*',
          '.mypy_cache/3.8/importlib/*',
          '.mypy_cache/3.8/logging/*',
          '.mypy_cache/3.8/os/*',
          '.mypy_cache/3.8/requests/*',
          '.mypy_cache/3.8/requests/packages/*',
          '.mypy_cache/3.8/requests/packages/urllib3/*',
          '.mypy_cache/3.8/requests/packages/urllib3/packages/*',
          '.mypy_cache/3.8/requests/packages/urllib3/packages/ssl_match_hostname/*',
          '.mypy_cache/3.8/requests/packages/urllib3/util/*',
          '.mypy_cache/3.8/risc/*',
          '.mypy_cache/3.8/urllib/*']}

entry_points = \
{'console_scripts': ['risc = risc.main:main']}

setup_kwargs = {
    'name': 'risc',
    'version': '0.2.0',
    'description': 'Python client and CLI for RISC',
    'long_description': '# risc-python\n\nPython client and CLI for [RISC](https://riscnetworks.com/)\n\n[![PyPI](https://img.shields.io/pypi/v/risc) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/risc)](https://pypi.org/project/risc/) [![PyPi Publish](https://github.com/2ndWatch/risc-python/workflows/PyPi%20Publish/badge.svg)](https://2ndwatch.github.io/risc-python/) [![Documenation](https://github.com/2ndWatch/risc-python/workflows/Github%20Pages/badge.svg)](https://2ndwatch.github.io/risc-python/)\n\n## Requirements\n\n[Python 3.6+](https://www.python.org/downloads/)\n\n## Installation & Usage\n\n```sh\npyenv install 3.7\npip(env) install risc\n```\n',
    'author': 'Mark Beacom',
    'author_email': 'mbeacom@2ndwatch.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/2ndWatch/risc-python',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
