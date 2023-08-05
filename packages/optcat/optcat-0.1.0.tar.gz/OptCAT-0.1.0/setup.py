# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optcat']

package_data = \
{'': ['*']}

install_requires = \
['catboost>=0.22,<0.23',
 'optuna>=1.2.0,<2.0.0',
 'pandas>=1.0.2,<2.0.0',
 'scikit-learn>=0.22.2,<0.23.0']

setup_kwargs = {
    'name': 'optcat',
    'version': '0.1.0',
    'description': 'OptCAT (= Optuna + CatBoost) provides a scikit-learn compatible estimator that tunes hyperparameters in CatBoost with Optuna.',
    'long_description': '# OptCAT\n\n<p align="center">\n<a href="https://github.com/wakamezake/OptCAT/actions"><img alt="Actions Status" src="https://github.com/wakamezake/OptCAT/workflows/Python package/badge.svg"></a>\n<a href="https://github.com/wakamezake/OptCAT/master/LICENSE"><img alt="License: MIT" src="http://img.shields.io/badge/license-MIT-blue.svg"></a>\n</p>\n\nOptCAT (= [Optuna][1] + [CatBoost][2]) provides a scikit-learn compatible estimator that tunes hyperparameters in CatBoost with Optuna.\n\nThis Repository is very influenced by [Y-oHr-N/OptGBM](https://github.com/Y-oHr-N/OptGBM).\n\n## Examples\n\n```python:classification.py\nfrom optcat.core import CatBoostClassifier\nfrom sklearn import datasets\n\nparams = {\n        "bootstrap_type": "Bayesian",\n        "loss_function": "Logloss",\n        "iterations": 100\n    }\n\nmodel = CatBoostClassifier(params=params, n_trials=5)\ndata, target = datasets.load_breast_cancer(return_X_y=True)\nmodel.fit(X=data, y=target)\n```\n\n## Installation\n\n```\npip install git+https://github.com/wakamezake/OptCAT.git\n```\n\n## Testing\n\n```\npoetry run pytest\n```\n\n\n[1]: https://optuna.org/\n[2]: https://catboost.ai/\n',
    'author': 'wakame1367',
    'author_email': 'hotwater1367@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wakamezake/OptCAT',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
