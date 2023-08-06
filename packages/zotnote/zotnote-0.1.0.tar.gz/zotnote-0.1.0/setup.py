# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zotnote']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'jinja2>=2.11.1,<3.0.0',
 'python-dotenv>=0.12.0,<0.13.0',
 'tomlkit>=0.5.11,<0.6.0',
 'xdg>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['zotnote = zotnote.__main__:main']}

setup_kwargs = {
    'name': 'zotnote',
    'version': '0.1.0',
    'description': 'Streamlining reading notes with Zotero',
    'long_description': '# ZotNote\n\nA helper tool that automatises reading note management with Zotero.\n\n## Features\n\n- Connects to local Zotero and Better Bibtex databases to retrieve metadata\n- Supports custom templates for reading notes\n- CLI interface to populate templates and create reading note skeletons\n\n*Planned features*\n\n- Basic annotations\n- Retrieval of tags/keywords from Zotero\n- Text analysis of reading notes\n- Export as annotated bibliography\n\n## Getting started\n\n### Requirements\n\nI have currently only used the script on my own Linux machine.\n\n- Python 3.6 (I am currently using f-strings)\n- [Zotero Standalone](https://www.zotero.org/)\n- [Better Bibtex plugin](https://github.com/retorquere/zotero-better-bibtex)\n\n### Installation\n\nJust copy the script found in `src` to a folder on your machine. Make sure to add the folder to your PATH and make the file executable.\n\n## Usage\n\n### Configuration\n\nThe script contains a few variables that you have to rename to according to your own file system.\n\n```bash\nNOTES = "/path/to/reading/notes"\nZOTERO = "/path/to/zotero"\n\nAUTHOR = "Your Name"\n```\n\nMake sure to copy `templates/template.txt` to your NOTES folder.\n\n## Creating your own notes\n\n`new_zotnote.py citekey` should be all you need to start creating your notes. The script will retrieve all required metadata from Zotero and populate the template stored in your notes folder and create a new reading note.',
    'author': 'Asura Enkhbayar',
    'author_email': 'asura.enkhbayar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bubblbu/zotnote',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
