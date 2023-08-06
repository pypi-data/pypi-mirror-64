# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pslib']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'pslib',
    'version': '0.0.4',
    'description': 'A python library for interacting with Pokémon Showdown',
    'long_description': '# pslib\n\n[![Build Status](https://travis-ci.com/vberlier/pslib.svg?branch=master)](https://travis-ci.com/vberlier/pslib)\n[![PyPI](https://img.shields.io/pypi/v/pslib.svg)](https://pypi.org/project/pslib/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pslib.svg)](https://pypi.org/project/pslib/)\n\n> A python library for interacting with Pokémon Showdown.\n\n**🚧 Work in progress 🚧**\n\n```python\nimport asyncio\nimport pslib\n\nasync def join_battles(client):\n    while True:\n        for battle in await client.query_battles():\n            await battle.join()\n\nasync def display_logs(client):\n    async for message in client.listen(pslib.WinMessage, all_rooms=True):\n        print(message.room.logs)\n        await message.room.leave()\n\nasync def main():\n    async with pslib.connect() as client:\n        await asyncio.gather(join_battles(client), display_logs(client))\n\nasyncio.run(main())\n```\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install pslib\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/pslib/blob/master/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/pslib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
