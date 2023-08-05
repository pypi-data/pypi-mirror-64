# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webcomix',
 'webcomix.scrapy',
 'webcomix.scrapy.download',
 'webcomix.scrapy.download.tests',
 'webcomix.scrapy.tests',
 'webcomix.scrapy.verification',
 'webcomix.tests',
 'webcomix.tests.fake_websites']

package_data = \
{'': ['*'],
 'webcomix.tests.fake_websites': ['one_webpage/*',
                                  'one_webpage_searchable/*',
                                  'three_webpages/*',
                                  'three_webpages_alt_text/*',
                                  'three_webpages_classes/*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'scrapy-splash>=0.7.2,<0.8.0',
 'scrapy>=2.0.1,<3.0.0',
 'tqdm>=4.43.0,<5.0.0']

entry_points = \
{'console_scripts': ['webcomix = webcomix.cli:cli']}

setup_kwargs = {
    'name': 'webcomix',
    'version': '3.2.2',
    'description': 'Webcomic downloader',
    'long_description': None,
    'author': 'Jean-Christophe Pelletier',
    'author_email': 'pelletierj97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
