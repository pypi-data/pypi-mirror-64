# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsfind']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.11.9,<2.0.0',
 'ccaaws>=0.4.6,<0.5.0',
 'ccalogging>=0.3.3,<0.4.0',
 'ccautils>=0.4.2,<0.5.0',
 'chaim>=0.8.0,<0.9.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['ifind = awsfind.find:awsFindInstances']}

setup_kwargs = {
    'name': 'awsfind',
    'version': '0.4.0',
    'description': 'searches across all accounts and regions known to chaim for the item(s)',
    'long_description': "# awsfind\n\nsearches across all accounts and regions known to chaim for the instance(s)\n\nYou should be able to obtain `CrossAccountReadOnly` chaim credentials for\nevery account.\n\nThe script will obtain chaim `rro` permissions for each account in turn,\ndeleting them when it has finished with that account, and then, using a\nthread per region query the AWS API for each specific instance mentioned\non the command line.\n\nOnce all instances have been found the script stops and displays the\nresults.\n\nShould the script need to visit every account it will take approx. 13\nminutes to do so.\n\n## install\n\nClone this repository, and enter the dir\n\n```\ngit clone https://github.com/ConnectedHomes/awsfind.git\ncd awsfind\n```\n\nIf you don't currently use `poetry` get it with\n\n```\npip[3] install poetry --user\n```\n\nOptional: If you intend to develop this script install the dependencies\n\n```\npoetry install\n```\n\nOptional: the script can be run from the development environment with\n\n```\npoetry run ifind\n```\n\nInstall the script to the users local python installation\n\n```\npoetry build\nvers=$(poetry version|sed 's/ /-/')\npip[3] install dist/${vers}*whl --user\n```\n\nYou should now have a script `ifind` in your python user directories\n\n```\n$ which ifind\n/home/chris/.local/bin/ifind\n\n$ ifind -h\nifind 0.3.0\n ifind - AWS Instance Finder\n\nSearches across all accounts and regions for instances using chaim credentials\n\nsearch accounts in alphabetical order\n    ifind <instance-id> <instance-id> ... <instance-id>\n\nto search accounts in random order (maybe quicker)\n    ifind -r <instance-id> <instance-id> ... <instance-id>\n\n\n```\n\nYou can now add your `.local/bin` directory to your PATH if you haven't\nalready.\n\n## Usage\n\nYou can run directly from this repository with `poetry run ifind` or\ninstall it as above\n\n```\n$ ifind <instance-id> <instance-id> ... <instance-id>\n```\n\nThe above command will search through all accounts in alphabetical order,\nsearching all regions for the instance ids.\n\nIf you want to search accounts in a random order (which maybe quicker)\nthen add `-r` to the command\n\n```\n$ ifind -r i-0b7ff13d0219b8b58 i-014c4b3c01153aef8\n```\n\n\nIt displays it's current progress\n\n\n```\n$ ifind i-0b7ff13d0219b8b58 i-014c4b3c01153aef8 i-09d8cfbb5fc425d26 i-0b42d2ae0db8cf231\nifind 0.3.0\nSearching 119 accounts in 16 regions for 4 instances\n\n\n  7/119 1/4    biqlite-qa-uk\n```\n\ni.e. looking in the 7th of 119 accounts for the last remaining instance\nid, having found 3 others.\n\nOnce it has found all the instances it stops, displaying the results\n\n```\nAccount                       Region    Name                          Instance ID\n------------------------------------------------------------------------------------------\nbiqlite-dev-uk                eu-west-1 UNNAMED                       i-0b7ff13d0219b8b58\nbiqlite-dev-uk                eu-west-1 UNNAMED                       i-014c4b3c01153aef8\nbiqlite-firmware              eu-west-1 simplicity                    i-09d8cfbb5fc425d26\nbiqlite-qa-uk                 eu-west-1 UNNAMED                       i-0b42d2ae0db8cf231\n\nsearch took 59s\n```\n",
    'author': 'ccdale',
    'author_email': 'chris.allison@hivehome.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
