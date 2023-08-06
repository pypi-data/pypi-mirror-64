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
    'version': '0.1.1',
    'description': 'A reverse-parser as a Hypotheses strategy: generate examples from an EBNF grammar',
    'long_description': 'Hypothesis-Grammar\n==================\n\n[![Build Status](https://travis-ci.org/anentropic/hypothesis-grammar.svg?branch=master)](https://travis-ci.org/anentropic/hypothesis-grammar)\n[![Latest PyPI version](https://badge.fury.io/py/hypothesis-grammar.svg)](https://pypi.python.org/pypi/hypothesis-grammar/)\n\n![Python 3.7](https://img.shields.io/badge/Python%203.7--brightgreen.svg)\n![Python 3.8](https://img.shields.io/badge/Python%203.8--brightgreen.svg)  \n\n(pre-alpha... the stuff I\'ve tried all works, not well tested yet though)\n\n## What is it?\n\nHypothesis-Grammar is a "reverse parser" - given a grammar it will generate examples of that grammar.\n\nIt is implemented as a [Hypothesis](https://hypothesis.readthedocs.io/) strategy.\n\n(If you are looking to generate text from a grammar for purposes other than testing with Hypothesis then this lib can still be useful, but I stongly recommend looking at the [tools provided with NLTK](http://www.nltk.org/howto/generate.html) instead.)\n\n## Usage\n\nSo, how does this look?\n\nFirst you need a grammar. Our grammar format is based on that used by the [Lark parser](https://lark-parser.readthedocs.io/en/latest/grammar/) library.  You can see our grammar-parsing grammar [here](hypothesis_grammar/grammar.lark). More details of our grammar format [below](#grammar-details).\n\nHere is an example of using Hypothesis-Grammar:\n\n```python\nfrom hypothesis_grammar import strategy_from_grammar\n\nst = strategy_from_grammar(\n    grammar="""\n        DET: "the" | "a"\n        N: "man" | "park" | "dog"\n        P: "in" | "with"\n\n        s: np vp\n        np: DET N\n        pp: P np\n        vp: "slept" | "saw" np | "walked" pp\n    """,\n    start="s",\n)\n\nst.example()\n# [\'a\', \'dog\', \'saw\', \'the\', \'man\']\n\nst.example()\n# [\'a\', \'park\', \'saw\', \'a\', \'man\']\n\nst.example()\n# [\'the\', \'man\', \'slept\']\n```\n\nor as a test...\n\n```python\nfrom hypothesis import given\nfrom hypothesis_grammar import strategy_from_grammar\n\n\n@given(\n    strategy_from_grammar(\n        grammar="""\n            DET: "the" | "a"\n            N: "man" | "park" | "dog"\n            P: "in" | "with"\n\n            s: np vp\n            np: DET N\n            pp: P np\n            vp: "slept" | "saw" np | "walked" pp\n        """,\n        start="s",\n    )\n)\ndef test_grammar(example):\n    nouns = {"man", "park", "dog"}\n    assert any(noun in example for noun in nouns)\n```\n\nThe grammar is taken from an example in the NLTK docs and converted into our "simplified Lark" format.\n\n`start="s"` tells the parser that the start rule is `s`.\n\nAs you can see, we have produced a Hypothesis strategy which is able to generate examples which match the grammar (in this case, short sentences which sometimes makes sense).\n\nThe output will always be a flat list of token strings. If you want a sentence you can just `" ".join(example)`.\n\nBut the grammar doesn\'t have to describe text, it might represent a sequence of actions for example. In that case you might want to convert your result tokens into object instances, which could be done via a lookup table.\n\n(But if you\'re generating action sequences for tests then probably you should check out Hypothesis\' [stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html) features first)\n\n## Grammar details\n\n- Whitespace is ignored\n- \'Terminals\' must be named all-caps (terminals only reference literals, not other rules), e.g. `DET`\n- \'Rules\' must be named all-lowercase, e.g. `np`\n- LHS (name) and RHS are separated by `:` \n- String literals must be quoted with double-quotes e.g. `"man"`\n- You can also use regex literals, they are delimited with forward-slash, e.g. `/the[a-z]{0,2}/`. Content for the regex token is generated using Hypothesis\' [`from_regex`](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.from_regex) strategy, with `fullmatch=True`.\n- Adjacent tokens are concatenated, i.e. `DET N` means a `DET` followed by a `N`.\n- `|` is alternation, so `"in" | "with"` means one-of `"in"` or `"with"`\n- `?` means optional, i.e. `"in"?` means `"in"` is expected zero-or-one time.\n- `*` i.e. `"in"*` means `"in"` is expected zero-or-many times.\n- `+` i.e. `"in"+` means `"in"` is expected one-or-many times.\n- `~ <num>` means exactly-&lt;num&gt; times.\n- `~ <min>..<max>` is a range, expected between-&lt;min&gt;-and-&lt;max&gt; times.\n- `(` and `)` are for grouping, the group can be quantified using any of the modifiers above.\n',
    'author': 'Anentropic',
    'author_email': 'ego@anentropic.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anentropic/hypothesis-grammar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
