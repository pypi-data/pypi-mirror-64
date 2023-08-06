# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eqversion']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'snakypy>=0.3.4,<0.4.0', 'tomlkit>=0.5.11,<0.6.0']

entry_points = \
{'console_scripts': ['eqversion = eqversion.eqversion:main']}

setup_kwargs = {
    'name': 'eqversion',
    'version': '0.1.3',
    'description': 'EQversion maintains the pyproject.toml and __init__.py (from the main package) versions in the same way.',
    'long_description': 'EQVersion\n=========\n\nThe purpose of **EQVersion** is to remove the change redundancy in the project version in two places, in the **pyproject.toml** and in the **__init__.py** of the main package. **EQVersion** is especially for those who work with `Poetry`_.\n\n\nUsing:\n------\n\nIn a project using `Poetry`_ and an active virtual environment, add **EQVersion** as a development dependency:\n\n.. code-block:: shell\n\n    $ poetry add eqversion --dev\n\n\nNow simply run the command below for the versions to be matched:\n\n.. code-block:: shell\n\n    $ eqversion\n\n**Specifying a package:**\n\nBy default, **EQVersion** takes the name of the main package via **pyproject.toml**, in the key **name**, but it may happen that the name of the main package is not the same as in **pyproject.toml**. If this happens, the **--package** option should be used to specify the main package:\n\n.. code-block:: shell\n\n    $ eqversion --package=<PACKAGE MAIN NAME>\n\nUsing with tests:\n\nYou must call **EQVersion** before performing your tests.\n\nExample of `tox.ini` file:\n\n.. code-block:: ini\n\n    [tox]\n    isolated_build = True\n    \n    [testenv]\n    setenv =\n        PYTHONPATH = {toxinidir}\n    deps =\n        poetry\n    commands =\n        pip install --upgrade pip\n        poetry install\n        poetry run eqversion\n    ;   Or use the named option:\n    ;   poetry run eqversion --package=<PACKAGE MAIN NAME>\n        poetry run pytest --basetemp={envtmpdir}\n\nLinks\n-----\n\n* Authors: https://github.com/snakypy/eqversion/blob/master/AUTHORS.rst\n* Code: https://github.com/snakypy/eqversion\n* Documentation: https://github.com/snakypy/eqversion/blob/master/README.rst\n* Releases: https://pypi.org/project/eqversion/#history\n* Issue tracker: https://github.com/snakypy/eqversion/issues\n\nDonation\n--------\n\nIf you liked my work, buy me a coffee <3\n\n.. image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif\n    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YBK2HEEYG8V5W&source\n\nLicense\n-------\n\nThe gem is available as open source under the terms of the `MIT License`_ ©\n\n\n.. _MIT License: https://github.com/snakypy/zshpower/blob/master/LICENSE\n.. _Poetry: https://python-poetry.org/\n',
    'author': 'William C. Canin',
    'author_email': 'william.costa.canin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/snakypy/eqversion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
