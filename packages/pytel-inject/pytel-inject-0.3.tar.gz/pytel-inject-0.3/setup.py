# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytel']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytel-inject',
    'version': '0.3',
    'description': 'Injection of dependencies for python 3',
    'long_description': "A bag of objects for Python\n===========================\n\n.. image:: https://img.shields.io/pypi/v/pytel-inject.svg?style=flat\n    :target: https://pypi.org/project/pytel-inject/\n\n.. image:: https://travis-ci.com/mattesilver/pytel.svg\n  :target: https://travis-ci.com/mattesilver/pytel\n\n.. image:: https://codecov.io/gh/mattesilver/pytel/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/mattesilver/pytel\n\nFor when your object graph is too big\n\n.. code-block:: python\n\n    class A:\n        def __init__(self, b: B):\n            self.b = b\n\n    class B:\n        pass\n\n    svc = {\n        'a': A,\n        'b': B,\n    }\n    context = Pytel(PytelContext(svc))\n    assert context.a.b == context.b\n\nSee `usage <https://github.com/mattesilver/pytel/blob/master/tests/pytel/test_usage.py>`_ for more cases\n",
    'author': 'Rafal Krupinski',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mattesilver/pytel',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
