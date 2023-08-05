# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbfcapi']

package_data = \
{'': ['*']}

extras_require = \
{'api': ['aiohttp[speedups]>=3.6,<4.0'],
 'apis': ['requests>=2.23,<3.0'],
 'app': ['aiohttp[speedups]>=3.6,<4.0',
         'beautifulsoup4>=4.8,<5.0',
         'fastapi>=0.52,<0.53',
         'pyhumps>=1.3.1,<2.0.0',
         'uvicorn>=0.11,<0.12'],
 'client': ['aiohttp[speedups]>=3.6,<4.0'],
 'clients': ['requests>=2.23,<3.0'],
 'lib': ['aiohttp[speedups]>=3.6,<4.0', 'beautifulsoup4>=4.8,<5.0'],
 'libs': ['beautifulsoup4>=4.8,<5.0', 'requests>=2.23,<3.0']}

setup_kwargs = {
    'name': 'bbfcapi',
    'version': '2.0.0',
    'description': 'API service, library and parser for BBFC',
    'long_description': '# BBFC API\n\n![PyPI](https://img.shields.io/pypi/v/bbfcapi)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bbfcapi)\n![PyPI - License](https://img.shields.io/pypi/l/bbfcapi)\n![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/fustra/bbfcapi)\n\nWeb API and Python library for [BBFC](https://bbfc.co.uk/).\n\n## Public REST API\n\n![Mozilla HTTP Observatory Grade](https://img.shields.io/mozilla-observatory/grade-score/bbfcapi.fustra.co.uk?publish)\n![Security Headers](https://img.shields.io/security-headers?url=https%3A%2F%2Fbbfcapi.fustra.co.uk%2Fhealthz)\n<a href="https://uptime.statuscake.com/?TestID=SgEZQ2v2KF" title="bbfcapi uptime report">\n    <img src="https://app.statuscake.com/button/index.php?Track=K7juwHfXel&Days=7&Design=6"/>\n</a>\n\n* Hosted @ <https://bbfcapi.fustra.co.uk>\n* Documentation @ <https://bbfcapi.fustra.co.uk/redoc>\n* Alternative documentation @ <https://bbfcapi.fustra.co.uk/docs>\n\nTry it now:\n\n```console\n$ curl "https://bbfcapi.fustra.co.uk?title=interstellar&year=2014"\n{"title":"INTERSTELLAR","year":2014,"ageRating":"12"}\n```\n\nUse the Python client:\n\n```console\n$ pip install bbfcapi[apis]\n```\n\n```py\n>>> from bbfcapi.apis import top_search_result\n>>> top_search_result("interstellar", 2014)\nFilm(title=\'INTERSTELLAR\', year=2014, age_rating=<AgeRating.AGE_12: \'12\'>)\n```\n\n## Project Overview\n\nThe project is divided into:\n\n* "I want to self-host the REST API demoed above"\n    * BBFCAPI - Python REST Web API\n    * `pip install bbfcapi[app]`\n* "I want a Python library to talk to the REST API as demoed above"\n    * Python client for BBFCAPI\n    * `pip install bbfcapi[api]` (async variant)\n    * `pip install bbfcapi[apis]` (sync variant)\n* "I want a Python library to talk to the BBFC website"\n    * Python library for the BBFC website\n    * `pip install bbfcapi[lib]` (async variant)\n    * `pip install bbfcapi[libs]` (sync variant)\n* "I want to download the raw HTML web pages from BBFC"\n    * Python network client for the BBFC website\n    * `pip install bbfcapi[client]` (async variant)\n    * `pip install bbfcapi[clients]` (sync variant)\n* "I want to parse the downloaded web pages from BBFC"\n    * Python HMTL parser for the BBFC web pages\n    * `pip install bbfcapi`\n\nSync versions use the `requests` library, while async variants use `aiohttp`.\n\n## High-Level REST Web API\n\nInstall `pip install bbfcapi[app]`.\n\nTo use the REST API to query BBFC, first run the web server:\n\n```console\n$ uvicorn bbfcapi.app:app\n```\n\nThen, to query the API using the Python library *synchronously*:\n\n```py\nfrom bbfcapi.apis import top_search_result\ntop_search_result("interstellar", 2014, base_url="http://127.0.0.1:8000")\n```\n\nOr, to query the API using the Python library *asynchronously*:\n\n```py\nfrom bbfcapi.api import top_search_result\nprint(await top_search_result("interstellar", 2014, base_url="http://127.0.0.1:8000"))\n```\n\n```py\nimport asyncio\nfrom bbfcapi.api import top_search_result\nprint(asyncio.run(top_search_result("interstellar", 2014, base_url="http://127.0.0.1:8000")))\n```\n\nOr, to query the API using `curl`:\n\n```console\n$ curl "127.0.0.1:8000?title=interstellar&year=2014"\n{"title":"INTERSTELLAR","year":2014,"age_rating":"12"}\n```\n\nOr, to query the API from another web page:\n\n```js\nasync function call()\n{\n    const response = await fetch(\'http://127.0.0.1:8000/?title=interstellar&year=2014\');\n    const responseJson = await response.json();\n    console.log(JSON.stringify(responseJson));\n}\ncall();\n```\n\nAdditional notes:\n\n* HTTP 404 Not Found is returned when there is no film found.\n* Browse documentation @ <http://127.0.0.1:8000/redoc>.\n* Or, browse documentation @ <http://127.0.0.1:8000/docs>.\n* Samples on hosting this web application are available in the repository\'s [/docs](/docs) folder.\n\n## High-Level Python Library\n\nTo use the library to get results from BBFC *synchronously*:\n\n```py\nfrom bbfcapi.lib import top_search_result\nprint(top_search_result(title="interstellar", year=2014))\n```\n\nTo use the library to get results from BBFC *asynchronously*:\n\n```py\nfrom bbfcapi.lib import top_search_result\nprint(await top_search_result(title="interstellar", year=2014))\n```\n\n```py\nimport asyncio\nfrom bbfcapi.lib import top_search_result\nprint(asyncio.run(top_search_result(title="interstellar", year=2014)))\n```\n\n## Low-Level BBFC Network Client & Parser\n\nTo use the library to get raw HTML pages from BBFC *synchronously*:\n\n```console\n$ pip install bbfcapi[clients]`\n```\n\n```py\nfrom bbfcapi.clients import search\nprint(search(title="interstellar", year=2014))\n```\n\nTo use the library to get raw HTML pages from BBFC *asynchronously*:\n\n```console\n$ pip install bbfcapi[client]`\n```\n\n```py\nfrom bbfcapi.client import search\nprint(await search(title="interstellar", year=2014))\n```\n\n```py\nimport asyncio\nfrom bbfcapi.client import search\nprint(asyncio.run(search(title="interstellar", year=2014)))\n```\n\nTo use the library to parse raw HTML pages from BBFC:\n\n```console\n$ pip install bbfcapi`\n```\n\n```py\nfrom bbfcapi import parser\nprint(parser.parse_top_search_result(b"<BBFC search page byte-string>"))\n```\n\n## Development\n\n1. `poetry install` to set up the virtualenv (one-off)\n2. `poetry run uvicorn bbfcapi.apiweb:app --reload` to run the web server\n3. `make fix`, `make check`, and `make test` before committing\n\nThere is also `make test-live` which will run live integration tests against\nthe BBFC website.\n\n### Contributing\n\nPull requests are welcome :)\n\n### Publishing\n\nThis application is published on PyPi.\n\n1. Ensure you have configured the PyPi repository with Poetry (one-off)\n2. Run `make release` to execute the check-list\n\nTo publish to the test repository:\n\n1. Ensure you have configured the Test PyPi repository with Poetry (one-off)\n2. `poetry publish --build -r testpypi` to upload to the test repository\n\n## Changelog\n\n### v2.0.0 - 2020-03-22\n\n- Add Python client library for the BBFCAPI REST Web API\n- Use camelCasing for JSON fields in the web API\n- Reorganise entire package\n\n### v1.0.1 - 2020-01-19\n\n- Fix parsing 12A age ratings\n\n### v1.0.0 - 2020-01-19\n\n- First release of bbfcapi\n',
    'author': 'QasimK',
    'author_email': 'noreply@QasimK.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Fustra/bbfcapi/',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
