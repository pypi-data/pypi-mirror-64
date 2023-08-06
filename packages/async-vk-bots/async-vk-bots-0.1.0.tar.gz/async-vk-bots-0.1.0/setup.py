# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['async_vk_bots']

package_data = \
{'': ['*'], 'async_vk_bots': ['api/*', 'ext/*']}

install_requires = \
['aiohttp>=3.5,<4.0']

setup_kwargs = {
    'name': 'async-vk-bots',
    'version': '0.1.0',
    'description': 'Library for creating asynchronous vk bots',
    'long_description': None,
    'author': 'mihett05',
    'author_email': 'mihett05@yandex.ru',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
