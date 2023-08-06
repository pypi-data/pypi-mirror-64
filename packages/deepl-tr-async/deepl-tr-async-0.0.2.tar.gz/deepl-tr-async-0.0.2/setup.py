# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepl_tr_async']

package_data = \
{'': ['*']}

install_requires = \
['absl-py>=0.9.0,<0.10.0',
 'environs>=7.3.1,<8.0.0',
 'flake8>=3.7.9,<4.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'linetimer>=0.1.4,<0.2.0',
 'logzero>=1.5.0,<2.0.0',
 'polyglot>=16.7.4,<17.0.0',
 'pycld2>=0.41,<0.42',
 'pyicu>=2.4.3,<3.0.0',
 'pyinstaller>=3.6,<4.0',
 'pyperclip>=1.7.0,<2.0.0',
 'pyppeteer>=0.0.25,<0.0.26',
 'pyquery>=1.4.1,<2.0.0',
 'pytest-cov>=2.8.1,<3.0.0',
 'python-dotenv>=0.12.0,<0.13.0',
 'tqdm>=4.43.0,<5.0.0']

entry_points = \
{'console_scripts': ['deepl-tr = deepl_tr_async.__main__:main']}

setup_kwargs = {
    'name': 'deepl-tr-async',
    'version': '0.0.2',
    'description': 'deepl translate for free, based no pyppeteer',
    'long_description': '# deepl-tr-async ![build](https://github.com/ffreemt/deepl-tr-async/workflows/build/badge.svg)[![codecov](https://codecov.io/gh/ffreemt/deepl-tr-async/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/deepl-tr-async)\ndeepl translate for free with async and proxy support, based on pyppeteer\n\n### Installation\nNot available yet\n```pip install deepl-tr-async```\n\nValidate installation\n```\npython -c "import deepl_tr_async; print(deepl_tr_async.__version__)"\n# 0.0.1 or other version info\n```\n\n### Usage\n\n```\nimport asyncio\nfrom deepl_tr_async import deepl_tr_async\n\nasyncio.get_event_loop().run_until_complete(deep_tr_async(\'test this and that\'))\n# \'测试这个和那个\'\n```\n\n## Extra installation for Windows 10\n\nDownload and install the pyicu and pycld2 whl packages for your OS version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu and https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2\n\n### Acknowledgments\n\n* Thanks to everyone whose code was used\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffremt/deepl-tr-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
