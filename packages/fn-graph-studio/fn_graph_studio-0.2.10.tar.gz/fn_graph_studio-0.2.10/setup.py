# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fn_graph_studio']

package_data = \
{'': ['*']}

install_requires = \
['dash-treebeard>=0.0.1,<0.0.2',
 'dash>=1.7,<2.0',
 'dash_core_components>=1.6,<2.0',
 'dash_interactive_graphviz>=0.1.0,<0.2.0',
 'dash_split_pane>=1.0,<2.0',
 'fn_graph>=0.5.0',
 'pandas>=0.25.3,<0.26.0',
 'plotly>=4.4,<5.0',
 'sh>=1.12.14,<2.0.0']

entry_points = \
{'console_scripts': ['run_graph_studio = '
                     'fn_graph_studio.cli:run_studio_command']}

setup_kwargs = {
    'name': 'fn-graph-studio',
    'version': '0.2.10',
    'description': 'A web based explorer for fn_graph function composers',
    'long_description': None,
    'author': 'James Saunders',
    'author_email': 'james@businessoptics.biz',
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
