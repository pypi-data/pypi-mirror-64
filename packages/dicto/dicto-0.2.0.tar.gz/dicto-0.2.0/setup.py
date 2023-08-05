# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dicto']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3,<6.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'dicto',
    'version': '0.2.0',
    'description': '',
    'long_description': '# dicto\nA dict-like object that enables access of its elements as regular fields. Dicto\'s main feature is delivering an elegant experience while using configuration files/objects. \n\n### Example\nYou can create a Dicto from any `dict`: \n\n```python\nimport dicto\n\nparams = dicto.Dict({"learning_rate": 0.001, "batch_size": 32 })\n\noptimizer = Adam(params.learning_rate)\n```\n\nDicto parses through arbitrary nested structures of `dicts`, `list`, `tuple`, and `set`: \n\n```python\nimport dicto\n\nparams = dicto.Dict({\n    "points":[\n        {\n            "x": 1,\n            "y": 2\n        },\n        {\n            "x": 3,\n            "y": 4\n        }\n    ]\n})\n\nprint(params.points[0].x) # 1\n```\n`dicto` can load `json`, `yaml`, and `xml` formats directly, for example, given this `YAML` file\n```yaml\n# params.yml\nlearning_rate: 0.001\nbatch_size: 32\n```\n\nyou can load it like this:\n\n```python\nimport dicto\n\nparams = dicto.load("params.yml")\noptimizer = Adam(params.learning_rate)\n```\n\n## Installation\n```bash\npip install dicto\n```\n\n## License\nMIT License',
    'author': 'Cristian Garcia',
    'author_email': 'cgarcia.e88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cgarciae.github.io/dicto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
