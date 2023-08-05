# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neural_semigroups']

package_data = \
{'': ['*'],
 'neural_semigroups': ['.mypy_cache/3.7/*',
                       '.mypy_cache/3.7/collections/*',
                       '.mypy_cache/3.7/importlib/*',
                       '.mypy_cache/3.7/neural_semigroups/*',
                       '.mypy_cache/3.7/numpy/*',
                       '.mypy_cache/3.7/numpy/core/*',
                       '.mypy_cache/3.7/os/*',
                       '.mypy_cache/3.8/*',
                       '.mypy_cache/3.8/collections/*',
                       '.mypy_cache/3.8/ctypes/*',
                       '.mypy_cache/3.8/email/*',
                       '.mypy_cache/3.8/email/mime/*',
                       '.mypy_cache/3.8/google/*',
                       '.mypy_cache/3.8/google/protobuf/*',
                       '.mypy_cache/3.8/html/*',
                       '.mypy_cache/3.8/http/*',
                       '.mypy_cache/3.8/importlib/*',
                       '.mypy_cache/3.8/json/*',
                       '.mypy_cache/3.8/logging/*',
                       '.mypy_cache/3.8/neural_semigroups/*',
                       '.mypy_cache/3.8/numpy/*',
                       '.mypy_cache/3.8/numpy/core/*',
                       '.mypy_cache/3.8/os/*',
                       '.mypy_cache/3.8/six/*',
                       '.mypy_cache/3.8/six/moves/*',
                       '.mypy_cache/3.8/six/moves/urllib/*',
                       '.mypy_cache/3.8/tkinter/*',
                       '.mypy_cache/3.8/torch/*',
                       '.mypy_cache/3.8/torch/autograd/*',
                       '.mypy_cache/3.8/torch/cuda/*',
                       '.mypy_cache/3.8/torch/nn/*',
                       '.mypy_cache/3.8/torch/nn/modules/*',
                       '.mypy_cache/3.8/torch/nn/parallel/*',
                       '.mypy_cache/3.8/torch/nn/utils/*',
                       '.mypy_cache/3.8/torch/optim/*',
                       '.mypy_cache/3.8/torch/utils/*',
                       '.mypy_cache/3.8/torch/utils/data/*',
                       '.mypy_cache/3.8/torch/utils/tensorboard/*',
                       '.mypy_cache/3.8/unittest/*',
                       '.mypy_cache/3.8/urllib/*',
                       '.pytest_cache/*',
                       '.pytest_cache/v/cache/*']}

install_requires = \
['numpy==1.18.1',
 'pandas==1.0.2',
 'pytorch-ignite==0.3.0',
 'sphinx_rtd_theme==0.4.3',
 'tensorboard==2.1.1',
 'torch==1.4.0',
 'tqdm==4.43.0']

setup_kwargs = {
    'name': 'neural-semigroups',
    'version': '0.2.0',
    'description': 'Neural networks powered research of semigroups',
    'long_description': None,
    'author': 'Boris Shminke',
    'author_email': 'boris@shminke.ml',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inpefess/neural-semigroups',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
