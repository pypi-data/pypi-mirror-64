# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyopenuv']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'asynctest>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'pyopenuv',
    'version': '1.1.0',
    'description': 'A simple Python API data from openuv.io',
    'long_description': '# ☀️  pyopenuv: A simple Python API for data from openuv.io\n\n[![CI](https://github.com/bachya/pyopenuv/workflows/CI/badge.svg)](https://github.com/bachya/pyopenuv/actions)\n[![PyPi](https://img.shields.io/pypi/v/pyopenuv.svg)](https://pypi.python.org/pypi/pyopenuv)\n[![Version](https://img.shields.io/pypi/pyversions/pyopenuv.svg)](https://pypi.python.org/pypi/pyopenuv)\n[![License](https://img.shields.io/pypi/l/pyopenuv.svg)](https://github.com/bachya/pyopenuv/blob/master/LICENSE)\n[![Code Coverage](https://codecov.io/gh/bachya/pyopenuv/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/pyopenuv)\n[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/pyopenuv/maintainability)\n[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)\n\n`pyopenuv` is a simple Python library for retrieving UV-related information from\n[openuv.io](https://openuv.io/). It supports both sync and async use cases.\n\n- [Installation](#installation)\n- [Python Versions](#python-versions)\n- [API Key](#api-key)\n- [Usage](#usage)\n  * [Sync (Normal) Usage](#sync--normal--usage)\n  * [Async Usage](#async-usage)\n- [Contributing](#contributing)\n\n# Installation\n\n```python\npip install pyopenuv\n```\n\n# Python Versions\n\n`pyopenuv` is currently supported on:\n\n* Python 3.6\n* Python 3.7\n* Python 3.8 \n# API Key\n\nYou can get an API key from\n[the OpenUV console](https://www.openuv.io/console).\n\n# Usage\n\n## Sync (Normal) Usage\n\n```python\nfrom pyopenuv import Client\nfrom pyopenuv.errors import OpenUvError\n\nAPI_KEY = "<OPENUV_API_KEY>"\nLATITUDE = 39.7974509\nLONGITUDE = -104.8887227\nALTITUDE = 1609.3\n\n\nclient = Client(API_KEY, LATITUDE, LONGITUDE, altitude=ALTITUDE)\n\ntry:\n    # Get current UV info:\n    print(client.uv_index())\n\n    # Get forecasted UV info:\n    print(client.uv_forecast())\n\n    # Get UV protection window:\n    print(client.uv_protection_window())\nexcept OpenUvError as err:\n    print(f"There was an error: {err}")\n```\n\n## Async Usage\n\nTo use the library in an `asyncio`-friendly way, simply pass the `use_async` parameter when\ncreating a client. From there, the same methods can be used, but now as coroutines:\n\n```python\nimport asyncio\n\nfrom pyopenuv import Client\nfrom pyopenuv.errors import OpenUvError\n\nAPI_KEY = "<OPENUV_API_KEY>"\nLATITUDE = 39.7974509\nLONGITUDE = -104.8887227\nALTITUDE = 1609.3\n\n\nasync def main():\n    client = Client(API_KEY, LATITUDE, LONGITUDE, altitude=ALTITUDE, use_async=True)\n\n    try:\n        # Get current UV info:\n        print(await client.uv_index())\n\n        # Get forecasted UV info:\n        print(await client.uv_forecast())\n\n        # Get UV protection window:\n        print(await client.uv_protection_window())\n    except OpenUvError as err:\n        print(f"There was an error: {err}")\n\n\nasyncio.get_event_loop().run_until_complete(main())\n```\n\nBy default, the `asyncio`-friendly method creates a new connection to OpenUV with each\ncoroutine; this means that you won\'t get much in the way of runtime speed savings over\nthe normal, sync API. If you are calling a large number of coroutines (or merely want to\nsqueeze out every second of runtime savings possible), an\n[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection\npooling:\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\nfrom pyopenuv import Client\nfrom pyopenuv.errors import OpenUvError\n\nAPI_KEY = "<OPENUV_API_KEY>"\nLATITUDE = 39.7974509\nLONGITUDE = -104.8887227\nALTITUDE = 1609.3\n\n\nasync def main():\n    async with ClientSession() as session:\n        client = Client(\n            API_KEY,\n            LATITUDE,\n            LONGITUDE,\n            altitude=ALTITUDE,\n            session=session,\n            use_async=True,\n        )\n\n        try:\n            # Get current UV info:\n            print(await client.uv_index())\n\n            # Get forecasted UV info:\n            print(await client.uv_forecast())\n\n            # Get UV protection window:\n            print(await client.uv_protection_window())\n        except OpenUvError as err:\n            print(f"There was an error: {err}")\n\n\nasyncio.get_event_loop().run_until_complete(main())\n```\n\nCheck out the `[examples/`](https://github.com/bachya/pyopenuv/tree/dev/examples)\ndirectory for more info.\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/bachya/pyopenuv/issues)\n  or [initiate a discussion on one](https://github.com/bachya/pyopenuv/issues/new).\n2. [Fork the repository](https://github.com/bachya/pyopenuv/fork).\n3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`\n4. (_optional, but highly recommended_) Enter the virtual environment: `source ./venv/bin/activate`\n5. Install the dev environment: `script/setup`\n6. Code your new feature or bug fix.\n7. Write tests that cover your new functionality.\n8. Run tests and ensure 100% code coverage: `script/test`\n9. Update `README.md` with any new documentation.\n10. Add yourself to `AUTHORS.md`.\n11. Submit a pull request!\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bachya/pyopenuv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
