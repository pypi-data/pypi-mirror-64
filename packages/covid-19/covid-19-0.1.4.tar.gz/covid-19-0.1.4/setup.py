# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covid_19']

package_data = \
{'': ['*']}

install_requires = \
['hug>=2.6.1,<3.0.0', 'pandas>=1.0.3,<2.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['covid = covid_19.api:__hug__.cli',
                     'covid-serve = covid_19.api:__hug__.http.serve']}

setup_kwargs = {
    'name': 'covid-19',
    'version': '0.1.4',
    'description': 'An API around the https://github.com/CSSEGISandData/COVID-19 dataset',
    'long_description': "# COVID-19 API\n\n![](https://github.com/knowsuchagency/covid-19/workflows/black/badge.svg)\n![](https://github.com/knowsuchagency/covid-19/workflows/unit%20tests/badge.svg)\n\nThis API is a wrapper around Johns Hopkins' https://github.com/CSSEGISandData/COVID-19 dataset.\n\nPlease abide by their terms of use with respect to how you use their data via this API.\n\n## Installation\n\nThe recommended method of installation is through [pipx].\n```bash\npipx install covid-19\n```\nHowever, covid-19 can also be pip-installed as normal.\n```bash\npip install covid-19\n```\n\n## Usage\n\nThis package installs a command-line tool, `covid`\n\nThis tool lets you programmatically access John Hopkins' dataset in the terminal\nbut also lets you host a REST API for the data on your machine via the `serve` subcommand\ni.e. `covid serve`\n\n## Docker\n\nThis package can also be run as a docker image.\n\n```bash\ndocker run knowsuchagency/covid-19 --help\n```\n\n[pipx]: https://github.com/pipxproject/pipx\n",
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
