jinja2_base64_filters
=====================

.. image:: https://img.shields.io/pypi/v/jinja2_base64_filters.svg
    :target: https://pypi.python.org/pypi/jinja2_base64_filters
    :alt: Latest PyPI version

Tiny jinja2 extension to add b64encode and b64decode filters.


Usage
-----
.. code-block:: python

        from jinja2_base64_filters import jinja2_base64_filters
        from jinja2 import Environment

        env = Environment(extensions=["jinja2_base64_filters.Base64Filters"])

        # "my_string" -> "bXlfc3RyaW5n"
        env.from_string("{{teststring|b64encode}}").render(teststring="my_string")

        # "bXlfc3RyaW5n" -> "my_string"
        env.from_string("{{teststring|b64decode}}").render(teststring="bXlfc3RyaW5n")


Installation
------------
**jinja2_base64_filters** is available for download from PyPI via pip::

    $ pip install jinja2-base64-filters

It will automatically install jinja2

Requirements
^^^^^^^^^^^^

Compatibility
-------------

Licence
-------
* Free software: MIT license

Authors
-------

jinja2_base64_filters was written by `Timothée GERMAIN <timothee@lumapps.com>`_.

This package was created with Cookiecutter_ and the `kragniz/cookiecutter-pypackage-minimal`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`kragniz/cookiecutter-pypackage-minimal`: https://github.com/kragniz/cookiecutter-pypackage-minimal.git