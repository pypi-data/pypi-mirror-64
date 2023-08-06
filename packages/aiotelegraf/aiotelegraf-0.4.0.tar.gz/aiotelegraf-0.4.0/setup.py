# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiotelegraf']

package_data = \
{'': ['*']}

install_requires = \
['pytelegraf>=0.3.3']

setup_kwargs = {
    'name': 'aiotelegraf',
    'version': '0.4.0',
    'description': 'AsyncIO Python client for sending metrics to Telegraf',
    'long_description': "# aiotelegraf\n\n[![Build Status](https://github.com/Gr1N/aiotelegraf/workflows/default/badge.svg)](https://github.com/Gr1N/aiotelegraf/actions?query=workflow%3Adefault) [![codecov](https://codecov.io/gh/Gr1N/aiotelegraf/branch/master/graph/badge.svg)](https://codecov.io/gh/Gr1N/aiotelegraf) ![PyPI](https://img.shields.io/pypi/v/aiotelegraf.svg?label=pypi%20version) ![PyPI - Downloads](https://img.shields.io/pypi/dm/aiotelegraf.svg?label=pypi%20downloads) ![GitHub](https://img.shields.io/github/license/Gr1N/aiotelegraf.svg)\n\nAn asyncio-base client for sending metrics to [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/).\n\nImplementation based on [pytelegraf](https://github.com/paksu/pytelegraf) package.\n\n## Installation\n\n```shell\n$ pip install aiotelegraf\n```\n\n## Usage\n\n```python\nimport asyncio\nimport aiotelegraf\n\n\nasync def main():\n    client = aiotelegraf.Client(\n        host='0.0.0.0',\n        port=8089,\n        tags={\n            'my_global_tag_1': 'value_1',\n            'my_global_tag_2': 'value_2',\n        }\n    )\n    await client.connect()\n\n    client.metric('my_metric_1', 'value_1', tags={\n        'my_tag_1': 'value_1',\n    })\n    await client.close()\n\n\nasyncio.run(main())\n```\n\n## Contributing\n\nTo work on the `aiotelegraf` codebase, you'll want to clone the project locally and install the required dependencies via [poetry](https://python-poetry.org):\n\n```sh\n$ git clone git@github.com:Gr1N/aiotelegraf.git\n$ make install\n```\n\nTo run tests and linters use command below:\n\n```sh\n$ make lint && make test\n```\n\nIf you want to run only tests or linters you can explicitly specify which test environment you want to run, e.g.:\n\n```sh\n$ make lint-black\n```\n\n## License\n\n`aiotelegraf` is licensed under the MIT license. See the license file for details.\n",
    'author': 'Nikita Grishko',
    'author_email': 'gr1n@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Gr1N/aiotelegraf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
