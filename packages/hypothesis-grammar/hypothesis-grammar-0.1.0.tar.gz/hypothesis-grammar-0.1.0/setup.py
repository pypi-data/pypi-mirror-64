# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypothesis_grammar']

package_data = \
{'': ['*']}

install_requires = \
['hypothesis>=5.8.0,<6.0.0',
 'inject>=4.1.1,<5.0.0',
 'lark-parser>=0.8.5,<0.9.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'hypothesis-grammar',
    'version': '0.1.0',
    'description': 'A reverse-parser as a Hypotheses strategy: generate examples from an EBNF grammar',
    'long_description': None,
    'author': 'Anentropic',
    'author_email': 'ego@anentropic.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
