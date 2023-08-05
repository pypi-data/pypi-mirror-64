# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linestickerdl']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'click>=7.1.1,<8.0.0',
 'parsel>=1.5.2,<2.0.0',
 'questionary>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['line-sticker-dl = linestickerdl.cli:main']}

setup_kwargs = {
    'name': 'line-sticker-dl',
    'version': '1.0.0',
    'description': 'line sticker downloader',
    'long_description': '# line-sticker-dl\n\nCommand Line Downloader for stickers of popular messaging application [LINE].\n\ne.g. \nhttps://store.line.me/stickershop/product/9044256/en\n\n\n# Usage\n\n```shell\nUsage: line-sticker-dl [OPTIONS] [IDS_OR_URLS]...\n\n  Line sticker downloader cli application\n\nOptions:\n  -o, --output DIRECTORY  save sticker files to directory\n  -s, --search TEXT       search_stickers for stickers by a query\n  -x, --speed INTEGER     concurrent request limit, higher speeds might cause\n                          bans  [default: 10]\n\n  --help                  Show this message and exit.\n```\n\n![demo](demo.svg)\n\nThe application can either download straight from urls or shop ids:\n\n```\nhttps://store.line.me/stickershop/product/9044256/en\n# shop id in this case being:\n9044256\n```\n\nor can search sticker shop via query:\n\n```shell\n$ line-sticker-dl --search bugcat                                                                                     \n? Select stickers:  (Use arrow keys to move, <space> to select, <a> to toggle, <i> to invert)                         \n » ○ BugCat-Capoo Cute and useful\n   ○ BugCat Capoo & Tutu - move move\n   ○ Bugcat-Capoo is on the Move! Vol. 2\n   ○ BugCat Capoo & Tutu-love and eat\n   ○ BugCat-Capoo\n```\n\nOutput urls to stdout or if `-o`/`--output` flag is given download sticker files to given directory.\n\n\n# Install\n\nCan be installed via pip:\n\n```shell\n$ pip install --user line-sticker-dl\n```\n\nor built from source:\n\n```shell script\n$ git clone https://github.com/Granitosaurus/line-sticker-dl\n$ cd line-sticker-dl\n$ pip install .\n```\n\n[LINE]: https://store.line.me\n',
    'author': 'granitosaurus',
    'author_email': 'tinarg@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/granitosaurus/line-sticker-dl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
