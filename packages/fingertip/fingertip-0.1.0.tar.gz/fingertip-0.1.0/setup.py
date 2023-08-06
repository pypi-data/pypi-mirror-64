# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fingertip',
 'fingertip.plugins',
 'fingertip.plugins.backend',
 'fingertip.plugins.os',
 'fingertip.plugins.self_test',
 'fingertip.util']

package_data = \
{'': ['*']}

install_requires = \
['CacheControl>=0.12.6,<0.13.0',
 'GitPython>=3.1.0,<4.0.0',
 'cloudpickle>=1.3.0,<2.0.0',
 'colorlog>=4.1.0,<5.0.0',
 'fasteners>=0.15,<0.16',
 'lockfile>=0.12.2,<0.13.0',
 'paramiko>=2.7.1,<3.0.0',
 'pexpect>=4.8.0,<5.0.0',
 'pyxdg>=0.26,<0.27',
 'requests-mock>=1.7.0,<2.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['fingertip = fingertip.main:main']}

setup_kwargs = {
    'name': 'fingertip',
    'version': '0.1.0',
    'description': 'Control VMs, containers and other machines with Python, leverage live snapshots',
    'long_description': None,
    'author': 'Alexander Sosedkin',
    'author_email': 'asosedki@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
