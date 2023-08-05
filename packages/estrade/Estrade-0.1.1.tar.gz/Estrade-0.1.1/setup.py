# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['estrade',
 'estrade.indicators',
 'estrade.indicators.candle_set',
 'estrade.mixins',
 'estrade.reporting',
 'estrade.utils']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.15.5,<0.16.0',
 'pyYAML>=5.3,<6.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2019.3,<2020.0',
 'requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'estrade',
    'version': '0.1.1',
    'description': 'Build, Backtest and Go Live your own trading bots',
    'long_description': '# Estrade\n\n[![Build Status](https://travis-ci.com/cimourdain/estrade.svg?branch=master)](https://travis-ci.com/cimourdain/estrade)\n[![Documentation Status](https://readthedocs.org/projects/estrade/badge/?version=latest)](https://estrade.readthedocs.io/en/latest/?badge=latest)\n[![pypi](https://badgen.net/pypi/v/estrade)](https://pypi.org/project/estrade/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![black](https://badgen.net/badge/code%20style/black/000)](https://github.com/ambv/black)\n\n# Estrade: Trading bot manager\n\nEstrade is a python library that allows you to easily backtest and run stock trading strategies.\n\nEstrade focus on providing tools so you mainly focus on your strategy definition.\n\n>  **WARNING**: Estrade is still in an alpha state of developpement and very unmature. Do not use it for other purposes than testing.\n\n## Features\n\n- Estrade provides a **market environnement**, so you do not have to worry about\n   - Trades result calculation\n   - Candle Graph building\n   - Indicators calculation\n- Estrade allows you to define your strategies based on market events (new tick received, new candle created)\n- Estrade allows you to create your own data providers to generate ticks data and manage trades (open/close)\n- Estrade allows you to create your own indicators\n- Estrade allows you to create your own reporting\n\n\n## What Estrade does NOT provides\n\n- **Data**: You have to define your own data provider (live or static)\n- **Strategies**: Although some very basic (and useless) strategies are provided as examples in samples, Estrate does not provide any financially relevant strategy.\n\n## Documentation\n\n[Documentation](https://estrade.readthedocs.io/)\n\n\n',
    'author': 'Gabriel Oger',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/estrade/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
