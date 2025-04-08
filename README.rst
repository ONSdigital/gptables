Good Practice Tables (gptables)
===============================

.. image:: https://github.com/best-practice-and-impact/gptables/workflows/continuous-integration/badge.svg
    :target: https://github.com/best-practice-and-impact/gptables/actions
    :alt: Actions build status

.. image:: https://badge.fury.io/py/gptables.svg
    :target: https://badge.fury.io/py/gptables
    :alt: PyPI release


``gptables`` is an opinionated python package for spreadsheet production.
It produces ``.xlsx`` files from your ``pandas`` dataframes.

``gptables`` uses the Analysis Function `spreadsheet guidance`_.
It advocates a strong adherence to the guidance by restricting the range of operations possible.
The default theme ``gptheme`` should accommodate most use cases.
However, the ``Theme`` object allows development of custom themes, where other formatting is required.

Users may also be interested in `csvcubed`_, a package for turning data and metadata into
machine-readable CSV-W files.

R users should check out `aftables`_, an R native equivalent to ``gptables``.

Requirements
------------
- Python 3.9+

Install
-------
gptables is available from `PyPI`_.

As a user:

- Using a virtual environment? Use `pip install gptables` in a terminal.
- If you're not using a virtual environment, use `python -m pip install gptables` instead.

All done!

As a developer:

- Navigate to the directory where this repo is cloned.
- Use `pip install -e .` to install an editable version of the package.
- Use `pip install .[dev]`to install the dependencies for developers.
- For working on docs, also use `pip install .[docs]`.
- Set up pre-commit to run automatically with `pre-commit install`.

Usage
-----

1. Map your data to the elements of a ``GPTable``.

2. Define the format of each element with a custom ``Theme`` - or simply use the default ``gptheme``.

3. Optionally design a ``Cover`` page to provide information that relates to all of the tables in your Workbook.

4. Optionally supply a ``notes_table`` with information about any notes.

5. Make you gptable with ``write_workbook``!

**Note**: This package create perfectly accessible spreadsheets but will help with many requirements.
Users should refer to the Analysis Function `spreadsheet guidance`_  and the `spreadsheet accessibility checklist`_.

Contributing
------------
Found a bug, or would like to suggest a new feature? The best way is to let us know by raising an `issue`_.

Alternatively, please email us - the Analysis Standards at Pipelines team at the Office for National Statistics (ASAP@ons.gov.uk).

Let us know if you use the package. We'd love to know what's working well, and what could be improved!

Requests and fixes are managed according to resource capacity, and we aim to acknowledge queries within one working week. Please follow up in the case of this taking longer.

.. _`spreadsheet guidance`: https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/
.. _`spreadsheet accessibility checklist`: https://analysisfunction.civilservice.gov.uk/policy-store/making-spreadsheets-accessible-a-brief-checklist-of-the-basics/
.. _`PyPI`: https://pypi.org/project/gptables/
.. _`aftables`: https://best-practice-and-impact.github.io/aftables/index.html
.. _`csvcubed`: https://onsdigital.github.io/csvcubed-docs/external/
.. _`issue`: https://github.com/best-practice-and-impact/gptables/issues
