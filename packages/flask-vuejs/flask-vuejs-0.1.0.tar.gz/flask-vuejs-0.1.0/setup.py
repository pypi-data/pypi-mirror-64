# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_vuejs']

package_data = \
{'': ['*'], 'flask_vuejs': ['static/*', 'static/core/*', 'templates/vue/*']}

install_requires = \
['flask-assets>=2.0,<3.0', 'flask>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'flask-vuejs',
    'version': '0.1.0',
    'description': 'Connect Flask With VueJS Framework',
    'long_description': '# Install\n\nFor install the package run:\n\n```\n$ pip install flask-vuejs\n```\n\n# Using\n\nImport the Vue class in bootstrap flask file, see:\n\n```ptyhon\nfrom flask_vuejs import Vue\n```\n\n## Register extension\n```ptyhon\nVue(app)\n```\n\n## With Factory\n```ptyhon\nvue = Vue()\n\ndef create_app():\n    app = Flask(__name__)\n    vue.init_app(app)\n```\n\n## Configuration\n\nYou can set the component directory, by default it uses \'static/components\' folder, but, it can be easily changed.\n\n```ptyhon\ndef create_app():\n    app.config["FLASK_VUE_COMPONENT_DIRECTORY"] = "vuecomponent"\n```\nRemember, if you changed component directory, you\'ll should be rename this directory on \'static\' folder application\n\n## [JInja Template]\n\nYou can see how its works [here](https://github.com/pacotei/flask-vuejs/tree/master/sample_app)',
    'author': 'Marcus Pereira',
    'author_email': 'oi@pacotei.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
