# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xpath']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xpath-expressions',
    'version': '1.0.2',
    'description': 'Treat XPath expressions as Python objects ',
    'long_description': '# XPath-expressions\n\n![https://travis-ci.org/orf/xpath-expressions](https://travis-ci.org/orf/xpath-expressions.svg?branch=master)\n![https://pypi.org/project/xpath-expressions/](https://badge.fury.io/py/xpath-expressions.svg)\n\n\nThis is a small, lightweight Python 3.5+ library to aide in the manipulations of\nxpath expressions. It allows you to manipulate them as Python objects with\nPython expressions and operators.\n\n### Install\n\n`pip install xpath-expressions`\n\n\n### Quickstart\n\n```python\nfrom xpath import Expression, Attribute\n\nroot_node = Expression(\'/root\')\nprint(root_node.children)                 # /root/*\nprint(root_node.name)                     # name(/root)\nprint(root_node.attributes[1])            # /root/@*[1]\nprint(root_node / \'abc\' / \'def\')          # /root/abc/def\n\n# Filtering expressions:\nprint(root_node.text == \'abc\')            # /root/text()=\'abc\'\n\nexpr = Attribute(\'abc\') == \'def\'\nprint(expr)                               # @abc=\'def\'\nprint(root_node.children[expr])           # /root/*[@abc=\'def\']\n\n# The library handles quoting for you:\nexpr = Attribute(\'abc\') == "def\'"\nfiltered2 = root_node.children[expr]      # /root/*[@abc="def\'"]\n\n# You can use xpath functions:\nfrom xpath import func\n# Pass arguments like usual\nexpr = func.string_length(root_node.name)\nprint(expr)                               # string-length(name(/root/))\n\n# And treat those as normal expressions\nprint(expr == 5)                          # string-length(name(/root/)) == 5\n\n# The library normalizes python reserved names:\nprint(func.or_())                         # or()\n\n# Use custom namespaces\nfrom xpath import Functions\nns_functions = Functions(\'my-ns:\')\nprint(ns_functions.something())           # my-ns:something()\n```\n',
    'author': 'orf',
    'author_email': 'tom@tomforb.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/orf/xpath-expressions',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>3.5',
}


setup(**setup_kwargs)
