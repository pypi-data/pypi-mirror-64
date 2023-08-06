# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfjeeves',
 'tfjeeves.callbacks',
 'tfjeeves.datasets',
 'tfjeeves.evaluation',
 'tfjeeves.models',
 'tfjeeves.models.classification',
 'tfjeeves.models.regression',
 'tfjeeves.tests',
 'tfjeeves.utils']

package_data = \
{'': ['*']}

install_requires = \
['attrdict>=2.0.1,<3.0.0',
 'boto3>=1.10.44,<2.0.0',
 'boto>=2.49.0,<3.0.0',
 'click>=7.0,<8.0',
 'hyperdash>=0.15.3,<0.16.0',
 'loguru>=0.4.0,<0.5.0',
 'pandas>=1.0.0,<2.0.0',
 'pillow>=6.2.1,<7.0.0',
 'py3nvml>=0.2.5,<0.3.0',
 'tensorflow-estimator==2.1.0',
 'tensorflow==2.1.0',
 'tqdm>=4.41.1,<5.0.0']

entry_points = \
{'console_scripts': ['fix = scripts:fix', 'train = train:run']}

setup_kwargs = {
    'name': 'tfjeeves',
    'version': '0.2.4',
    'description': 'Utilities to help train models with tensorflow2 and keras',
    'long_description': '# tfjeeves\n\n`poetry run python train.py --config=configs/cifar10.py --data=assets/cifar10`\n\nhttps://flynn.gg/blog/software-best-practices-python-2019/\n',
    'author': 'Soumendra Dhanee',
    'author_email': 'soumendra@gmail.com',
    'maintainer': 'Soumendra Dhanee',
    'maintainer_email': 'soumendra@gmail.com',
    'url': 'https://github.com/soumendra/tfjeeves',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.7.6',
}


setup(**setup_kwargs)
