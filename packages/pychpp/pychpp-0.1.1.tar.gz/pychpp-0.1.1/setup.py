# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pychpp']

package_data = \
{'': ['*']}

install_requires = \
['rauth>=0.7.3,<0.8.0']

setup_kwargs = {
    'name': 'pychpp',
    'version': '0.1.1',
    'description': 'framework created to use the API provided by the online game Hattrick',
    'long_description': "# pyCHPP\n\npyCHPP is a python framework created to use the API provided by the online game Hattrick (www.hattrick.org).\n\n## Installation\n\npyCHPP can be installed using pip :\n\n    pip install pychpp\n\n## Usage\n\n### First connection\n    from pychpp import CHPP\n    \n    # Set consumer_key and consumer_secret provided for your app by Hattrick\n    consumer_key = ''\n    consumer_secret = ''\n    \n    # Initialize CHPP object\n    chpp = CHPP(consumer_key, consumer_secret)\n    \n    # Get url, request_token and request_token_secret to request API access\n    # You can set callback_url and scope\n    auth = chpp.get_auth(callback_url='www.mycallbackurl.com', scope='')\n    \n    # auth['url'] contains the url to which the user can grant the application\n    # access to the Hattrick API\n    # Once the user has entered their credentials,\n    # a code is returned by Hattrick (directly or to the given callback url)\n    \n    # Get access token from Hattrick\n    # access_token['key'] and access_token['secret'] have to be stored\n    # in order to be used later by the app\n    access_token = chpp.get_access_token(\n                        request_token=auth['request_token'],\n                        request_token_secret=auth['request_token_secret'],\n                        code=code,\n                        )\n\n### Further connections\n    # Once you have obtained access_token for a user\n    # You can use it to call Hattrick API\n    chpp = CHPP(consumer_key,\n                consumer_secret,\n                access_token['key'],\n                access_token['secret'],\n                )\n    \n    # Now you can use chpp methods to get datas from Hattrick API\n    # For example :\n    user = chpp.get_current_user()\n\n## License\npyCHPP is licensed under the Apache License 2.0.",
    'author': 'Pierre Gobin',
    'author_email': 'contact@pierregobin.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://framagit.org/Pierre86/pychpp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
