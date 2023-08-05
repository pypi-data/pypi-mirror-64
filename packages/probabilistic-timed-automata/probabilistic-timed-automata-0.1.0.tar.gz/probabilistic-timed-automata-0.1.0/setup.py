# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pta', 'pta.examples']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0', 'portion>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'probabilistic-timed-automata',
    'version': '0.1.0',
    'description': 'Probabilistic Timed Automata library for Python',
    'long_description': 'Probabilistic Timed Automata\n============================\n\nPython library for building and simulating probabilistic timed automata.\n\n.. image:: https://travis-ci.com/anand-bala/probabilistic-timed-automata.svg?branch=master\n  :target: https://travis-ci.com/anand-bala/probabilistic-timed-automata\n\n.. image:: https://codecov.io/gh/anand-bala/probabilistic-timed-automata/branch/master/graph/badge.svg?token=9JIV7X4YEQ\n  :target: https://codecov.io/gh/anand-bala/probabilistic-timed-automata\n\n.. image:: https://badge.fury.io/py/probabilistic-timed-automata.svg\n  :target: https://badge.fury.io/py/probabilistic-timed-automata\n\n.. image:: https://img.shields.io/badge/docs-link-brightgreen\n  :target: https://anand-bala.github.io/probabilistic-timed-automata\n\nInstallation\n------------\n\nTo install using `pip` just use:\n\n.. code-block:: shell\n\n    $ pip install probabilistic-timed-automata\n\n\nFor developers, since this project uses `poetry <https://python-poetry.org/>`_\nfor building/dependency management, please install that (and familiarize\nyourself with it). Then, you can run:\n\n.. code-block:: shell\n\n    $ poetry install\n\n\nUsage\n-----\n\n\n\n',
    'author': 'Anand Balakrishnan',
    'author_email': 'anandbala1597@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anand-bala/probabilistic-timed-automata.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
