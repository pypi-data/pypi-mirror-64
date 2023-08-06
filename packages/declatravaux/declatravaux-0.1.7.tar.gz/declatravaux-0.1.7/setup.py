# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['declatravaux']

package_data = \
{'': ['*'], 'declatravaux': ['ui/*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0', 'PyQt5==5.14', 'keyring>=21.2.0,<22.0.0']

setup_kwargs = {
    'name': 'declatravaux',
    'version': '0.1.7',
    'description': 'Utilitaire de transmission de déclarations issues de la plateforme http://www.reseaux-et-canalisations.ineris.fr/',
    'long_description': None,
    'author': 'Pierre Gobin',
    'author_email': 'contact@pierregobin.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
