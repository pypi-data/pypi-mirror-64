# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fn_graph_studio', 'fn_graph_studio.examples']

package_data = \
{'': ['*']}

install_requires = \
['dash-dangerously-set-inner-html>=0.0.2,<0.0.3',
 'dash-treebeard>=0.0.1,<0.0.2',
 'dash>=1.7,<2.0',
 'dash_core_components>=1.6,<2.0',
 'dash_interactive_graphviz>=0.1.0,<0.2.0',
 'dash_split_pane>=1.0,<2.0',
 'fn_graph>=0.5.0',
 'pandas>=0.25.3',
 'plotly>=4.4,<5.0',
 'seaborn>=0.10.0,<0.11.0',
 'sh>=1.0,<2.0',
 'statsmodels>=0.11.1,<0.12.0']

entry_points = \
{'console_scripts': ['run_graph_studio = '
                     'fn_graph_studio.cli:run_studio_command']}

setup_kwargs = {
    'name': 'fn-graph-studio',
    'version': '0.3.0',
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
