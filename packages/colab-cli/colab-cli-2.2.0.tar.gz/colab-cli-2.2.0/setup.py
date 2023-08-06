# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colab_cli', 'colab_cli.utilities']

package_data = \
{'': ['*']}

install_requires = \
['Send2Trash>=1.5.0,<2.0.0',
 'colorama>=0.4.3,<0.5.0',
 'gitpython>=3.1.0,<4.0.0',
 'pydrive>=1.3.1,<2.0.0',
 'typer[all]>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['colab-cli = colab_cli.main:app']}

setup_kwargs = {
    'name': 'colab-cli',
    'version': '2.2.0',
    'description': 'Experience better workflow with google colab, local jupyter notebooks and git',
    'long_description': "# Welcome to colab-cli 👋\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://choosealicense.com/licenses/mit/)\n[![Twitter: aks2899](https://img.shields.io/twitter/follow/aks2899.svg?style=social)](https://twitter.com/aks2899)\n\n> Experience better workflow with google colab, local jupyter notebooks and git\n\n### ✨ [Demo](https://github.com/Akshay090/colab-cli/demo)\n\n## Install\n\n```sh\npython -m pip install colab-cli or python3.7 -m pip install colab-cli\n```\n## Set-up\n\nSTEP-1: \n \n Get your client_secrets.json, [instructions given here](https://pythonhosted.org/PyDrive/quickstart.html),\nonly follow till the part where you have client_secrets.json in a local directory\n\nSTEP-2: \n\n Go to the local directory with client_secrets.json\n  ```sh\n  colab-cli set-config client_secrets.json\n  ```\nSTEP-3:\n \nNow we need to set the google account user id, goto your browser and see how many google logins you have,\n the count start from zero\n \n for eg. I have 3 login and I use the second one for coding work, so my user id is 1\n  ```sh\n  colab-cli set-auth-user 1\n  ```\n \n🙌 Now You're all set to go\n## Usage\n\n```sh\ncolab-cli --help\n```\n* List local ipynb\n```sh\ncolab-cli list-nb\n``` \n* Open local ipynb file in google colab for first time and remote copy for subsequent time\n```sh\ncolab-cli open-nb lesson1-pets.ipynb\n``` \n* Now you have made some changes to ipynb in colab, get the modified file locally by\n```sh\ncolab-cli pull-nb lesson1-pets.ipynb\n``` \n* Made some changes to ipynb locally, push it to drive\n```sh\ncolab-cli push-nb lesson1-pets.ipynb\n``` \n\n## Author\n\n👤 **Akshay Ashok**\n\n* Twitter: [@aks2899](https://twitter.com/aks2899)\n* Github: [@Akshay090](https://github.com/Akshay090)\n* LinkedIn: [@akshay-a](https://linkedin.com/in/akshay-a)\n\n## 🤝 Contributing\n\nContributions, issues and feature requests are welcome!\n\nFeel free to check [issues page](https://github.com/Akshay090/colab-cli/issues). You can also take a look at the [contributing guide](https://github.com/Akshay090/colab-cli/contributing.md).\n\n## Show your support\n\nGive a 🌟 if this project helped you!\n\n## 📝 License\n\nCopyright © 2020 [Akshay Ashok](https://github.com/Akshay090).\n\nThis project is [MIT](https://choosealicense.com/licenses/mit/) licensed.\n\n***\n_This README was generated with ❤ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_",
    'author': 'Akshay Ashok',
    'author_email': 'aks28id@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
