# Good Practice Tables (gptables)

[![Actions build status](https://github.com/best-practice-and-impact/gptables/workflows/continuous-integration/badge.svg)](https://github.com/best-practice-and-impact/gptables/actions)[![PyPI release](https://badge.fury.io/py/gptables.svg)](https://badge.fury.io/py/gptables)

`gptables` produces .xlsx files from your `pandas` dataframes in
either python or R (using [reticulate](https://rstudio.github.io/reticulate/)). You define the mapping from your
data to elements of the table and `gptables` does the rest.

Table element mapping:

![Cells A1 to A6 contain the title, subtitles, instructions, legend, source and scope. These parameters are mapped individually. The next row contains the column headings. Within the same row but on a new line are the units. The table note references are within the same row on a new line under the units. In columns 1, 2 and 3 of the next row down are index levels 1, 2 and 3. In the next columns are the data. Column headings, indices and data are supplied as a pandas DataFrame. Units and table note references are mapped individually.](imgs/table_mapping.png)

`gptables` uses the official [guidance on good practice spreadsheets](https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/).
It advocates a strong adherence to the guidance by restricting the range of possible operations.
The default formatting theme `gptheme` accommodates many use cases.
However, the [`Theme`](theme.md#theme-class) Class allows development of custom themes, where alternative formatting is required.

`gptables` is developed and maintained by the [Analysis Function](https://analysisfunction.civilservice.gov.uk/). It can be
installed from [PyPI](https://pypi.org/project/gptables/) or [GitHub](https://github.com/best-practice-and-impact/gptables). The source code is maintained on GitHub.
Users may also be interested in [aftables](https://best-practice-and-impact.github.io/aftables/), an R native equivalent to
`gptables`, and [csvcubed](https://gss-cogs.github.io/csvcubed-docs/external/), a package for turning data and metadata into
machine-readable CSV-W files.

## 5 Simple Steps

1. You map your data to the elements of a [`GPTable`](gptable.md#gptable-class).
2. You can define the format of each element with a custom [`Theme`](theme.md#theme-class), or simply use the default - gptheme.
3. Optionally design a [`Cover`](cover.md#cover-class) to provide information that relates to all of the tables in your Workbook.
4. Optionally upload a `notes_table` with information about any notes.
5. You [`write_workbook()`](api.md#write_workbook-function) to win.

**Note**: This package is not intending to create perfectly accessible spreadsheets but will help with the bulk of the work needed. Users of this packages should refer back to the [main spreadsheet guidance](https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/) or the [spreadsheet accessibility checklist](https://analysisfunction.civilservice.gov.uk/policy-store/making-spreadsheets-accessible-a-brief-checklist-of-the-basics/) after using it to make sure nothing has been missed. Please email [Analysis.Function@ons.gov.uk](mailto:Analysis.Function@ons.gov.uk) if you use the package so we can monitor use and the outputs produced.
