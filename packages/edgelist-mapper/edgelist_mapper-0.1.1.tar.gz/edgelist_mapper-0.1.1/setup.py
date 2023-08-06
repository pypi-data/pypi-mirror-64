# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['edgelist_mapper', 'edgelist_mapper.bin', 'tests', 'tests.bin']

package_data = \
{'': ['*'], 'tests': ['.fixtures/cities-s1/*']}

setup_kwargs = {
    'name': 'edgelist-mapper',
    'version': '0.1.1',
    'description': 'Maps nodes and edges of a multi-relational graph to integer',
    'long_description': '<h1 align="center">\n  <b>edgelist-mapper</b>\n</h1>\n<p align="center">\n  <!-- Build -->\n  <a href="https://github.com/simonepri/edgelist-mapper/actions?query=workflow%3Abuild">\n    <img src="https://github.com/simonepri/edgelist-mapper/workflows/build/badge.svg?branch=master" alt="Build status" />\n  </a>\n  <br />\n  <!-- Code style -->\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style" />\n  </a>\n  <!-- Linter -->\n  <a href="https://github.com/PyCQA/pylint">\n    <img src="https://img.shields.io/badge/linter-pylint-ce963f.svg" alt="Linter" />\n  </a>\n  <!-- Test runner -->\n  <a href="https://github.com/pytest-dev/pytest">\n    <img src="https://img.shields.io/badge/test%20runner-pytest-449bd6.svg" alt="Test runner" />\n  </a>\n  <!-- Build tool -->\n  <a href="https://github.com/python-poetry/poetry">\n    <img src="https://img.shields.io/badge/build%20system-poetry-4e5dc8.svg" alt="Build tool" />\n  </a>\n  <br />\n  <!-- License -->\n  <a href="https://github.com/simonepri/edgelist-mapper/tree/master/license">\n    <img src="https://img.shields.io/github/license/simonepri/edgelist-mapper.svg" alt="Project license" />\n  </a>\n</p>\n<p align="center">\n  📊 Maps nodes and edges of a multi-relational graph to integer\n</p>\n\n\n## Synopsis\n\nedgelist-mapper is a simple tool that reads an edge-list file representing a graph and maps each node and relation to integer.\nThe mapping assigned is such that entities and relations that appear more frequently in the graph are mapped to smaller numerical values.\n\nThis tool is particularly useful to pre-process some of the publicly available knowledge graph datasets that are often used for the machine learning task of [relation prediction][repo:NLP-progress->relation_prediction.md].\n\n\n## Input format\n\nThe tool takes as input a file (`edgelist.tsv`) that represents a graph as tab-separated triples of the form `(head, relation, tail)` and generates three new files, namely `mapped_edgelist.tsv`, `entities_map.tsv`, and `relations_map.tsv`.\n\n```\nsan_marino\tlocatedin\teurope\nbelgium\tlocatedin\teurope\nrussia\tlocatedin\teurope\nmonaco\tlocatedin\teurope\ncroatia\tlocatedin\teurope\npoland\tlocatedin\teurope\n```\n> Example content of the `edgelist.tsv` file.\n\n```\n0\teurope\n1\tsan_marino\n2\trussia\n3\tpoland\n4\tmonaco\n5\tcroatia\n6\tbelgium\n```\n> Content of the `entities_map.tsv` generated from the `edgelist.tsv` file.\n\n```\n0\tlocatedin\n```\n> Content of the `relations_map.tsv` generated from the `edgelist.tsv` file.\n\n```\n1\t0\t0\n6\t0\t0\n2\t0\t0\n4\t0\t0\n5\t0\t0\n3\t0\t0\n```\n> Content of the `mapped_edgelist.tsv` generated from the `edgelist.tsv` file.\n\n\n## CLI Usage\n\nThe CLI takes the following positional arguments:\n```\n  edgelist    Path of the edgelist file\n  output      Path of the output directory\n```\n\nExample usage:\n```bash\npip install git+https://github.com/simonepri/edgelist-mapper\npython -m edgelist_mapper.bin.run \\\n    edgelist.tsv \\\n    .\n```\n> NB: You need Python 3 to run the CLI.\n\n\n## Showcase\n\nThis tool has been used to create [this collection of datasets][repo:datasets-knowledge-embedding].\n\n\n## Authors\n\n- **Simone Primarosa** - [simonepri][github:simonepri]\n\nSee also the list of [contributors][contributors] who participated in this project.\n\n\n## License\n\nThis project is licensed under the MIT License - see the [license][license] file for details.\n\n\n\n<!-- Links -->\n\n[license]: https://github.com/simonepri/edgelist-mapper/tree/master/license\n[contributors]: https://github.com/simonepri/edgelist-mapper/contributors\n\n[github:simonepri]: https://github.com/simonepri\n\n[repo:NLP-progress->relation_prediction.md]:https://github.com/sebastianruder/NLP-progress/blob/master/english/relation_prediction.md\n[repo:datasets-knowledge-embedding]: https://github.com/simonepri/datasets-knowledge-embedding\n',
    'author': 'Simone Primarosa',
    'author_email': 'simonepri@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simonepri/edgelist-mapper#readme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
