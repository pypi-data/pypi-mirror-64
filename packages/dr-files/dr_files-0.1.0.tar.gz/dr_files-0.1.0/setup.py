# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dr_files', 'dr_files.pb']

package_data = \
{'': ['*']}

install_requires = \
['nptdms>=0.22.0,<0.23.0',
 'numpy>=1.18.2,<2.0.0',
 'protobuf>=3.11.3,<4.0.0',
 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'dr-files',
    'version': '0.1.0',
    'description': 'Read and convert Mechbase files (.dr) to known file formats',
    'long_description': None,
    'author': 'Antonis Kalipetis',
    'author_email': 'akalipetis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
