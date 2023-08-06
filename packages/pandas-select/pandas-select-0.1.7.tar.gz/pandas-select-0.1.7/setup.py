# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_select']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.25.1']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.5.0,<2.0.0'],
 'docs': ['sphinx>=2.4.1,<3.0.0',
          'sphinxcontrib-contentui>=0.2.4,<0.3.0',
          'ipython>=7.12.0,<8.0.0',
          'xdoctest>=0.11.0,<0.12.0',
          'scikit-learn>=0.20'],
 'tests': ['coverage[toml]>=5.0.3,<6.0.0',
           'scikit-learn>=0.20',
           'pytest>=5.3,<6.0']}

setup_kwargs = {
    'name': 'pandas-select',
    'version': '0.1.7',
    'description': 'Supercharged DataFrame indexing',
    'long_description': '==================================================\n``pandas-select``: Supercharged DataFrame indexing\n==================================================\n\n.. image:: https://github.com/jeffzi/pandas-select/workflows/tests/badge.svg\n   :target: https://github.com/jeffzi/pandas-select/actions\n   :alt: Github Actions status\n\n.. image:: https://codecov.io/gh/jeffzi/pandas-select/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/jeffzi/pandas-select\n   :alt: Coverage\n\n.. image:: https://readthedocs.org/projects/project-template-python/badge/?version=latest\n   :target: https://pandas-select.readthedocs.io/\n   :alt: Documentation status\n\n.. image:: https://img.shields.io/pypi/v/pandas-select.svg\n   :target: https://pypi.org/project/pandas-select/\n   :alt: Latest PyPI version\n\n.. image:: https://img.shields.io/pypi/pyversions/pandas-select.svg\n   :target: https://pypi.org/project/pandas-select/\n   :alt: Python versions supported\n\n.. image:: https://img.shields.io/pypi/l/pandas-select.svg\n   :target: https://pypi.python.org/pypi/pandas-select/\n   :alt: License\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Code style: black\n\n.. image:: https://img.shields.io/badge/style-wemake-000000.svg\n   :target: https://github.com/wemake-services/wemake-python-styleguide\n\n``pandas-select`` is a collection of DataFrame selectors that facilitates indexing\nand selecting data, fully compatible with pandas vanilla indexing.\n\nThe selector functions can choose variables based on their name, data type, arbitrary\nconditions, or any combination of these.\n\n``pandas-select`` is inspired by two R libraries: `tidyselect <https://tidyselect.r-lib.org/reference/select_helpers.html>`_\nand `recipe <https://tidymodels.github.io/recipes/reference/selections.html>`_.\n\nInstallation\n------------\n\n``pandas-select`` is a Python-only package `hosted on PyPI <https://pypi.org/project/pandas-select/>`_.\nThe recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_-installing\ninto a `virtualenv <https://hynek.me/articles/virtualenv-lives/>`_:\n\n.. code-block:: console\n\n   $ pip install pandas-select\n\n\nDesign goals\n------------\n\n.. why-begin\n\n* Fully compatible with `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_\n  ``[]`` and `pandas.DataFrame.loc <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html?highlight=loc#pandas.DataFrame.loc>`_\n  accessors.\n\n* Emphasise readability and conciseness by cutting boilerplate:\n\n.. code-block:: python\n\n\n    df[AllNumeric()] # pandas-select\n    df.select_dtypes(exclude="number").columns # vanilla\n\n    df[StartsWith("Type") | "Legendary"] # pandas-select\n\n     # vanilla\n    df[df.select_dtypes(exclude="number").columns]\n    cond = lambda col: col.startswith("Type") or col == "Legendary"\n    cols = [col for col in df.columns if cond(col)]\n    df[cols]\n\n* Ease the challenges of `indexing with hierarchical index <https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html#advanced-indexing-with-hierarchical-index>`_\n  and offers an alternative to `slicers <https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html#advanced-mi-slicers>`_\n  when the labels cannot be listed manually.\n\n.. code-block:: python\n\n    # pandas-select\n    selector = Contains("Jeff", axis="index", level="Name")\n    df_mi.loc[selector]\n\n    # vanilla\n    selector = df_mi.index.get_level_values("Name").str.contains("Jeff")\n    df_mi.loc[selector]\n\n* Allow *deferred selection* when the DataFrame\'s columns are not known in advance,\n  for example in automated machine learning applications. ``pandas_select`` offers\n  integration with `sklearn <https://scikit-learn.org/stable/modules/generated/sklearn.compose.`make_column_selector.html>`_.\n\n.. code-block:: python\n\n    from pandas_select import AnyOf, AllBool, AllNominal, AllNumeric, ColumnSelector\n    from sklearn.compose import make_column_transformer\n    from sklearn.preprocessing import OneHotEncoder, StandardScaler\n\n    ct = make_column_transformer(\n        (StandardScaler(), ColumnSelector(AllNumeric() & ~AnyOf("Generation"))),\n        (OneHotEncoder(), ColumnSelector(AllNominal() | AllBool() | "Generation")),\n    )\n    ct.fit_transform(df)\n\nProject Information\n-------------------\n\n``pandas-select`` is released under the `BS3 <https://choosealicense.com/licenses/bsd-3-clause/>`_ license,\nits documentation lives at `Read the Docs <https://pandas-select.readthedocs.io/>`_,\nthe code on `GitHub <https://github.com/jeffzi/pandas-select>`_,\nand the latest release on `PyPI <https://pypi.org/project/pandas-select/>`_.\nIt is tested on Python 3.6+.\n',
    'author': 'Jean-Francois Zinque',
    'author_email': 'jzinque@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeffzi/pandas-select/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
