# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_elasticsearch',
 'django_elasticsearch.management',
 'django_elasticsearch.management.commands',
 'django_elasticsearch.test']

package_data = \
{'': ['*']}

install_requires = \
['django>=1.11', 'elasticsearch-dsl>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'django-elasticsearch',
    'version': '7.0.2',
    'description': 'Wrapper around elasticsearch-dsl for django models',
    'long_description': '![PyPI](https://img.shields.io/pypi/v/django_elasticsearch)\n![python version](https://img.shields.io/badge/python-3.6+-blue.svg)\n![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-elasticsearch)\n![ElasticSearch Version](https://img.shields.io/badge/elasticsearch-7.0%2B-blue)\n![Travis (.com)](https://img.shields.io/travis/com/django-elasticsearch/django-elasticsearch)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n# Django-Elasticsearch\n\nDjango-Elasticsearch is a package that allows indexing of django models in elasticsearch.\nIt utilizes [elasticsearch-dsl](https://github.com/elastic/elasticsearch-dsl-py)\nso you can use all the features developed by the elasticsearch-dsl-py team.\n\n## Installation\n\n```bash\npip install django_elasticsearch\n# or, you know... \npoetry add django_elasticsearch\n```\n\n## Usage\n\nAt the moment, follow https://django-elasticsearch-dsl.readthedocs.io/\nbut replace `django_elasticsearch_dsl` with `django_elasticsearch`\n\n## Features\n\n- Based on [elasticsearch-dsl](https://github.com/elastic/elasticsearch-dsl-py) so you can make queries with the [Search](http://elasticsearch-dsl.readthedocs.io/en/stable/search_dsl.html) class.\n- Django signal receivers on save and delete for keeping Elasticsearch in sync.\n- Management commands for creating, deleting, rebuilding and populating indices.\n- Elasticsearch auto mapping from django models fields.\n- Complex field type support (ObjectField, NestedField).\n- Index fast using `parallel` indexing.\n\n### Elasticsearch Compatibility\nThe library is currently **only** compatible with Elasticsearch 7\n',
    'author': 'Sabricot',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
