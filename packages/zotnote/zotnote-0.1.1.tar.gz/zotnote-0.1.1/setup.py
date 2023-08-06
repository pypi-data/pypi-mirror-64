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
    'version': '0.1.1',
    'description': 'Streamlining reading notes with Zotero',
    'long_description': '# ZotNote\n\n> A helper tool that automatises your reading notes with Zotero.\n\nVision: A literature review suite that connects to Zotero/Better-Bibtex. Writing and accessing reading notes plus some basic qualitative text analytics based on the written notes.\n\n## Current features\n\n- Very simple installation via pip\n- Clean (very basic) CLI\n- Connects to local Zotero and Better Bibtex databases to retrieve metadata\n- Supports custom [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templates for reading notes\n\n*Planned features*\n\n- Annotation of reading notes with special tags/keywords\n  - Analytics based on these tags and keywords + content\n- Retrieval of tags/keywords from Zotero\n  - Enrich the reading notes with more metadata from Zotero\n- Simple reports about progress of literature review \n- (*dreaming*) Automatically export collection of notes as an annotated bibliography.\n\n## Getting started\n\n### Requirements\n\nI have currently only used the script on my own Linux machine.\n\n- Python 3.6 (I am currently using f-strings)\n- [Zotero Standalone](https://www.zotero.org/)\n- [Better Bibtex plugin](https://github.com/retorquere/zotero-better-bibtex)\n\n### Installation\n\nThe recommended way to install ZotNote is using [pipx](https://pipxproject.github.io/pipx/).\n\n```bash\npipx install zotnote\n```\n\nPipx cleanly install the package in an isolated environment (clean uninstalls!) and automagically exposes the cli-endpoints globally on your system.\n\nHowever, you can also simply use pip.\n\n```bash\npip install zotnote\n```\n\n## Usage\n\n### Configuration\n\nAfter installation you should be able to simply run `zotnote` and be prompted to a quick interactive configuration.\n\nZotNote currently asks you for:\n\n- A name which is used in all reading notes.\n- Path to your Zotero installation\n- A folder to store your reading notes\n\n### Creating your own notes\n\n`zotnote new [citekey]` should be all you need to start creating your notes. The script will retrieve all required metadata from Zotero and populate the template stored in your notes folder and create a new reading note.\n\n## Developers\n\nThe project is being developed with [Poetry](https://python-poetry.org/) as a dependency manager.\n\nMore instructions will follow soon!\n\n## Authors\n\nWritten by Asura Enkhbayar while he was quarantined.',
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
