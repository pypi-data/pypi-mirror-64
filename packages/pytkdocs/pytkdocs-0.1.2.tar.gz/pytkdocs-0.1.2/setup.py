# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytkdocs', 'pytkdocs.parsers']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pytkdocs = pytkdocs.cli:main']}

setup_kwargs = {
    'name': 'pytkdocs',
    'version': '0.1.2',
    'description': 'Load Python objects documentation.',
    'long_description': '# pytkdocs\n[![pipeline status](https://gitlab.com/pawamoy/pytkdocs/badges/master/pipeline.svg)](https://gitlab.com/pawamoy/pytkdocs/pipelines)\n[![coverage report](https://gitlab.com/pawamoy/pytkdocs/badges/master/coverage.svg)](https://gitlab.com/pawamoy/pytkdocs/commits/master)\n[![documentation](https://img.shields.io/badge/docs-latest-green.svg?style=flat)](https://pawamoy.github.io/pytkdocs)\n[![pypi version](https://img.shields.io/pypi/v/pytkdocs.svg)](https://pypi.org/project/pytkdocs/)\n\nLoad Python objects documentation.\n\n## Requirements\n`pytkdocs` requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.8\n\n# make it available globally\npyenv global system 3.6.8\n```\n</details>\n\n## Installation\nWith `pip`:\n```bash\npython3.6 -m pip install pytkdocs\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.6 -m pip install --user pipx\n\npipx install --python python3.6 pytkdocs\n```\n\n## Usage\n\n`pytkdocs` accepts JSON on standard input and writes JSON on standard output.\n\nInput format:\n\n```json\n{\n  "global_config": {},\n  "objects": [\n    {\n      "path": "my_module.my_class",\n      "config": {}\n    }\n  ]\n}\n```\n\n## Configuration\n\nFor now, the only configuration option available is `filters`,\nwhich allows you to select objects based on their name.\nIt is a list of regular expressions.\nIf the expression starts with an exclamation mark,\nit will filter out objects matching it (the exclamation mark is removed before evaluation).\nYou shouldn\'t need a literal `!` at the beginning of a regex\n(as it\'s not a valid character for Python objects names),\nbut if you ever need one, you can add it in brackets: `[!].*`.\n\nEvery regular expression is performed against every name.\nIt allows fine-grained filtering. Example:\n\n- `!^_`: filter out every object whose name starts with `_` (private/protected)\n- `^__`: but still select those who start with two `_` (class-private)\n- `!^__.*__$`: except those who also end with two `_` (specials)\n\nYou can obviously make use of your regex-fu\nto reduce the number of regular expressions and make it more efficient.\n\n',
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pawamoy/pytkdocs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
