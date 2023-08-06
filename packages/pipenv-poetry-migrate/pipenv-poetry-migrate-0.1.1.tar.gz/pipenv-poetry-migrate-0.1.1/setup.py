# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipenv_poetry_migrate']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.5.11,<0.6.0']

entry_points = \
{'console_scripts': ['pipenv-poetry-migrate = pipenv_poetry_migrate.cli:main']}

setup_kwargs = {
    'name': 'pipenv-poetry-migrate',
    'version': '0.1.1',
    'description': 'simple migration script, migrate pipenv to poetry',
    'long_description': '# pipenv-poetry-migrate\n\nThis is simple migration script, migrate pipenv to poetry.\n\n## Usage\n\n    $ pipenv-poetry-migrate -f Pipfile -t pyproject.toml\n\n## Example\n\nThis is an example of a Pipfile to be migrated.\n\n```toml\n[[source]]\nurl = "https://pypi.python.org/simple"\nverify_ssl = true\nname = "pypi"\n\n[packages]\nrequests = "*"\n\n[dev-packages]\npytest = "^5.2"\n```\n\nMigrate the above file to the following pyproject.toml.\n\n```toml\n[tool.poetry]\nname = "migration-sample"\nversion = "0.1.0"\ndescription = ""\nauthors = ["Yoshiyuki HINO <yhinoz@gmail.com>"]\n\n[tool.poetry.dependencies]\npython = "^3.7"\n\n[tool.poetry.dev-dependencies]\n\n[build-system]\nrequires = ["poetry>=0.12"]\nbuild-backend = "poetry.masonry.api"\n```\n\nBy executing this script, pyproject.toml is rewritten as follows.\n\n```toml\n[tool.poetry]\nname = "migration-sample"\nversion = "0.1.0"\ndescription = ""\nauthors = ["Yoshiyuki HINO <yhinoz@gmail.com>"]\n\n[tool.poetry.dependencies]\npython = "^3.7"\nrequests = "*"\n\n[tool.poetry.dev-dependencies]\npytest = "^5.2"\n\n[build-system]\nrequires = ["poetry>=0.12"]\nbuild-backend = "poetry.masonry.api"\n```',
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
