# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_revealjs', 'sphinx_revealjs.themes']

package_data = \
{'': ['*'],
 'sphinx_revealjs.themes': ['sphinx_revealjs/*',
                            'sphinx_revealjs/static/revealjs/*',
                            'sphinx_revealjs/static/revealjs/css/*',
                            'sphinx_revealjs/static/revealjs/css/print/*',
                            'sphinx_revealjs/static/revealjs/css/theme/*',
                            'sphinx_revealjs/static/revealjs/css/theme/source/*',
                            'sphinx_revealjs/static/revealjs/css/theme/template/*',
                            'sphinx_revealjs/static/revealjs/js/*',
                            'sphinx_revealjs/static/revealjs/lib/css/zenburn.css',
                            'sphinx_revealjs/static/revealjs/lib/font/league-gothic/*',
                            'sphinx_revealjs/static/revealjs/lib/font/source-sans-pro/*',
                            'sphinx_revealjs/static/revealjs/lib/js/html5shiv.js',
                            'sphinx_revealjs/static/revealjs/plugin/highlight/*',
                            'sphinx_revealjs/static/revealjs/plugin/markdown/*',
                            'sphinx_revealjs/static/revealjs/plugin/math/*',
                            'sphinx_revealjs/static/revealjs/plugin/multiplex/*',
                            'sphinx_revealjs/static/revealjs/plugin/notes-server/*',
                            'sphinx_revealjs/static/revealjs/plugin/notes/*',
                            'sphinx_revealjs/static/revealjs/plugin/print-pdf/*',
                            'sphinx_revealjs/static/revealjs/plugin/search/*',
                            'sphinx_revealjs/static/revealjs/plugin/zoom-js/*']}

install_requires = \
['docutils', 'sphinx']

setup_kwargs = {
    'name': 'sphinx-revealjs',
    'version': '0.10.0',
    'description': 'Sphinx extension with theme to generate Reveal.js presentation',
    'long_description': None,
    'author': 'Kazuya Takei',
    'author_email': 'myself@attakei.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/attakei/sphinx-revealjs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
