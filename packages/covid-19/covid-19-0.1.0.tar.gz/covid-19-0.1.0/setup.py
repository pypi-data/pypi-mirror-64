# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covid_19']

package_data = \
{'': ['*']}

install_requires = \
['hug>=2.6.1,<3.0.0', 'pandas>=1.0.3,<2.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['corona = covid_19.api:__hug__.cli',
                     'corona-serve = covid_19.api:__hug__.http.serve']}

setup_kwargs = {
    'name': 'covid-19',
    'version': '0.1.0',
    'description': 'An API around the https://github.com/CSSEGISandData/COVID-19 dataset',
    'long_description': None,
    'author': 'Stephan Fitzpatrick',
    'author_email': 'knowsuchagency@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
