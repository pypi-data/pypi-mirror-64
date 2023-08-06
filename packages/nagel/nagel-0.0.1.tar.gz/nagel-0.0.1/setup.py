# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nagel']
install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'nagel',
    'version': '0.0.1',
    'description': 'Straightforward pastebin software.',
    'long_description': 'nagel\n#####\n\n.. image:: https://travis-ci.org/supakeen/nagel.svg?branch=master\n    :target: https://travis-ci.org/supakeen/nagel\n\n.. image:: https://readthedocs.org/projects/nagel/badge/?version=latest\n    :target: https://nagel.readthedocs.io/en/latest/\n\n.. image:: https://nagel.readthedocs.io/en/latest/_static/license.svg\n    :target: https://github.com/supakeen/nagel/blob/master/LICENSE\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n.. image:: https://img.shields.io/pypi/v/nagel\n    :target: https://pypi.org/project/nagel\n\n.. image:: https://codecov.io/gh/supakeen/nagel/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/supakeen/nagel\n\nAbout\n=====\n\n``nagel`` is a Python library to interface with the pinnwand_ pastebin\nsoftware. By default ``nagel`` uses bpaste_ but you can override the\ninstance used.\n\nPrerequisites\n=============\n* Python >= 3.6\n* requests\n\nLicense\n=======\n``nagel`` is distributed under the MIT license. See `LICENSE`\nfor details.\n\n.. _bpaste: https://bpaste.net/\n.. _project page: https://github.com/supakeen/nagel\n.. _documentation: https://nagel.readthedocs.io/en/latest/\n.. _pinnwand: https://supakeen.com/project/pinnwand\n',
    'author': 'supakeen',
    'author_email': 'cmdr@supakeen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/supakeen/nagel',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
