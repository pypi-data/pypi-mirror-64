# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gigaleaf', 'gigaleaf.linkedfiles']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['gigaleaf_askpass = gigaleaf.askpass']}

setup_kwargs = {
    'name': 'gigaleaf',
    'version': '0.0.1',
    'description': 'An opinionated package for integrating Gigantum and Overleaf Projects',
    'long_description': '# gigaleaf\n[![CircleCI](https://circleci.com/gh/gigantum/gigaleaf/tree/master.svg?style=svg)](https://circleci.com/gh/gigantum/gigaleaf/tree/master)\n\nAn opinionated library to link Gigantum Projects to Overleaf Projects. This tool automatically manages git repositories\nto link the outputs from a Gigantum Project to an Overleaf Project, letting you build a completely reproducible \nworkflow from analysis to publication.\n\n**NOTE: This library is an early alpha proof of concept and subject to change!**\n\n\n### Installation\ngigaleaf may be installed using pip.\n\n```bash\npip install gigaleaf\n```\n\n### Usage\n\ngigaleaf is currently designed to working inside Jupyter Notebooks running in Gigantum and API is pretty simple\n\nThe general workflow is:\n\n* Create an Overleaf Project\n  \n* Get the git share URL from Overleaf\n  * Click on "Git" under the sync options\n    \n    ![Git Share Link](./imgs/git_link.png)\n    \n  * Copy the URL only (not the entire git command) from the modal that is shown\n    \n    ![Git Share Link](./imgs/git_link_modal.png)\n\n* Create an instance of gigaleaf\n\n  ```python\n  from gigaleaf import Gigaleaf\n  \n  gl = Gigaleaf()\n  ```\n  \n  This will start the configuration process where you enter the Overleaf URL along with\n  the email and password you use to log into Overleaf. These will be stored in a file locally that is "untracked" in \n  Gigantum and therefore will not sync or be shared. Other users will be prompted for _their_ Overleaf credentials if\n  they run your notebook.\n  \n* Link an image file\n\n  ```python\n  gl.link_image(\'output/fig1.png\')\n  ```\n  \n  Here, you pass the relative path in Gigantum to the image file you want to link. Any time this file changes and you\n  sync, it will automatically be updated in your Overleaf project! **You only need to call this once per file that you \n  wish to track.**\n  \n* Sync Projects\n\n  ```python\n  gl.sync()\n  ```\n  \n  This will pull changes from Overleaf, apply all gigaleaf managed changes, and then push back to Overleaf. Once files\n  are linked, you typically will only be calling `.sync()`.\n\n### Advanced Usage\n\ngigaleaf also provides Latex subfiles that you can use into your Overleaf Project that make adding and updating content\nfrom Gigantum trivial. \n\nTo take full advantage of this, the `link_image()` method has additional optional arguments:\n\n* caption: A caption that will be added to the image. If omitted, not caption is inserted.\n* label: A label to add to the figure for referencing inside your Overleaf document\n* width: A string to set width of the image. The default is "0.5\\\\textwidth"\n* alignment: A string to set the position of the image using the `adjustbox` package. The default is \'center\'\n\nTo use the subfiles generated you need to make a few modifications to your `main.tex` preamble. You may need to modify\nthis depending on your exact project configuration:\n\n```latex\n% gigaleaf setup\n\\usepackage[export]{adjustbox} % Needed if linking image files\n\\usepackage{graphicx} % Needed if linking image files\n\\graphicspath{{gigantum/data/}{../data/}} % Needed if linking image files\n\\usepackage{csvsimple} % Needed if linking csv files\n\\usepackage{subfiles} % Best loaded last in the preamble\n% gigaleaf setup\n```\n\nOnce configured, you can simply import the subfiles as they are created in your project. They will be named in a way\nthat matches the files they are linked to:\n\n```latex\n\\subfile{gigantum/subfiles/fig1_png}\n```\n\nIn this example, this subfile would render the image `fig1.png` that we linked above.\n\n\n### Contributing\n\nThis project is packaged using [poetry](https://python-poetry.org/). To develop, install packages with:\n\n```bash\npoetry install\n```\n\nWhen working, be sure to sign-off all of your commits.\n',
    'author': 'Dean Kleissas',
    'author_email': 'dean@gigantum.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gigantum/gigaleaf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
