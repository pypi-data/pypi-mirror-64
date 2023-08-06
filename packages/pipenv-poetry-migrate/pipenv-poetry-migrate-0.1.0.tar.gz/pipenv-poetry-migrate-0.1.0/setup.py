# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipenv_poetry_migrate']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.5.11,<0.6.0']

entry_points = \
{'console_scripts': ['pipenv-poetry-migrate = pipenv_poetry_migrate.cli::main']}

setup_kwargs = {
    'name': 'pipenv-poetry-migrate',
    'version': '0.1.0',
    'description': 'super simple migration script, from pipenv to poetry',
    'long_description': '# pipenv-poetry-migrate\n\nThis is super simple migration script, migrate pipenv to poetry.\n\n## Usage\n\n    $ pipenv-poetry-migrate -f Pipfile -t pyproject.toml\n\n',
    'author': 'Yoshiyuki HINO',
    'author_email': 'yhinoz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yhino/pipenv-poetry-migrate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
