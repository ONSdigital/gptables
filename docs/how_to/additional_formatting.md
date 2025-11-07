# Add additional formatting
There may be specific user needs or organisational reasons requiring 
formatting other than the `gptables` defaults. If this is required regularly, consider
the use of a [theme](custom_theme.md).

A wide range of options are possible
with the `gptable.GPTable(..., additional_formatting = ...)` parameter. See the [XlsxWriter documentation](https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties) for all formatting options.

!!! warning "Consider accessibility implications to formatting changes"
    Additional formatting changes the `gptables` defaults, which can introduce accessibility issues.
    Refer to the Releasing statistics in spreadsheets [guidance](https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/) and consider user needs
    regarding accessiblity before adjusting the formatting.

The sample code can be run from thes
[examples](https://github.com/ONSdigital/gptables/tree/main/gptables/examples) folder.

## Using `additional_formatting`

The `gptable.GPTable(..., additional_formatting = ...)` parameter allows for specifying
columns, rows, and/or cells and the corresponding formatting changes to make.

!!! warning "Formatting conflicts"
    There are some conflicts between additional formatting options, for example wrapping
    and shrinking text. Outputs should be reviewed for correctness.

The option of what to format is specified, followed by the specific columns, rows, or cells,
and then the formatting changes. To change the properties of columns called Species and Island
to be center-aligned and italic, for example:

```python
sample_additional_formatting = [
    {
        "column": {
            "columns": ["Species", "Island"],
            "format": {
                "align": "center",
                "italic": True,
            },
        }
    }
]
```
Columns can be referenced by name or number. Rows may only be referenced by number, with `-1`
corresponding to the last row. Column and row numbers include indices and column headings. Numeric indexing refers to position within the table, not the position in the output Excel sheet. Cell formatting takes highest precedence, followed by row formatting, and finally column formatting.

Multiple selections of columns, rows, and cells can be made in a single `additional_formatting` list.

```python
penguins_additional_formatting = [
    {
        "column": {
            "columns": ["Species", "Island"],
            "format": {
                "align": "center",
                "italic": True,
            },
        }
    },
    {
        "column": {"columns": [3], "format": {"left": 1}}
    },
    {
        "row": {
            "rows": -1,
            "format": {
                "bottom": 1,
                "indent": 2,
            },
        }
    },
]
```

This is combined with a basic example below in an extendable tab. The result is
italicisation of two columns, left bordering on the 4th column, and indentation in the final row.

??? "Using additional formatting"
    ```python
    import pandas as pd
    import gptables as gpt

    penguins_data = pd.read_csv("spenguins.csv")

    penguins_additional_formatting = [
        {
            "column": {
                "columns": ["Species", "Island"],
                "format": {
                    "align": "center",
                    "italic": True,
                },
            }
        },
        {
            "column": {"columns": [3], "format": {"left": 1}}
        },
        {
            "row": {
                "rows": -1,
                "format": {
                    "bottom": 1,
                    "indent": 2,
                },
            }
        },
    ]

    penguins_table = gpt.GPTable(
        table = penguins_data,
        table_name = "penguins_statistics",
        title = "The Palmer Penguins Dataset",
        subtitles = ["This is the first subtitle",
                    "This is another subtitle"],
        scope = "Penguins",
        source = "Palmer Station, Antarctica",
        additional_formatting = penguins_additional_formatting,
    )

    penguins_sheets = {"Penguins": penguins_table}

    wb = gpt.produce_workbook(
        filename="gpt_additional_formatting.xlsx",
        sheets=penguins_sheets
    )
    wb.close()
    ```

![](../static/howto_additional_formatting.png)

## Formatting text

Formatting can also be applied to the text in `title`, `subtitles`, `scope`, `source`
and `legend` elements without using `additional_formatting`. Avoid using text formatting to represent data or important information, as most formatting is neither accessible nor machine readable.

Instead of a string, provide a list of strings and dictionaries containing valid [XlsxWriter format properties](https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties)
and values to the relevant parameter. The formatting defined in these dictionaries will be applied to the
next string in the list.  For example:

```python
formatted_subtitles = [
    "The first subtitle",
    [{"bold": True}, "This", " is another subtitle"],
]
```

![](../static/howto_additional_formatting_text.png)

This is combined with a basic example below in an extendable tab.

??? "Formatting text"
    ```python
    import pandas as pd
    import gptables as gpt

    penguins_data = pd.read_csv("penguins.csv")

    formatted_subtitles = [
        "The first subtitle",
        [{"bold": True}, "This", " is another subtitle"],
    ]

    penguins_table = gpt.GPTable(
        table = penguins_data,
        table_name = "penguins_statistics",
        title = "The Palmer Penguins Dataset",
        subtitles = formatted_subtitles
        scope = "Penguins",
        source = "Palmer Station, Antarctica",
    )

    penguins_sheets = {"Penguins": penguins_table}

    wb = gpt.produce_workbook(
        filename="additional_formatting_example.xlsx",
        sheets=penguins_sheets
    )
    wb.close()
    ```

This formatting is applied in addition to the
formatting of that element specified in the [`Theme`](../api/classes/theme.md).

!!! warning "Formatting of note references and links"
    Text formatting is not currently supported if the cell also contains note
    references or links. This may be changed in the future if there is
    sufficient user need, so please raise an issue if this is functionality
    you need.


## Further formatting

`gptables` outputs can also be built on with the [Format](https://xlsxwriter.readthedocs.io/format.html#the-format-class), [Workbook](https://xlsxwriter.readthedocs.io/workbook.html#the-workbook-class)
and [Worksheet](https://xlsxwriter.readthedocs.io/worksheet.html#the-worksheet-class) classes from
XlsxWriter.

!!! warning "Competing formatting"
    Some formatting will only occur where cells do not already have formatting applied,
    for example in the `gptables` global [theme](https://github.com/ONSdigital/gptables/blob/e0dc2348e8172972ddd6ea2f737cb6047f591780/gptables/themes/gptheme.yaml#L1-L4) settings.

    Consult the XlsxWriter [Worksheet class documentation](https://xlsxwriter.readthedocs.io/worksheet.html#the-worksheet-class) as well as the `gptables` [theme how-to](../how_to/custom_theme.md) for more information.

Worksheet properties can be altered directly, for example setting row height:

```python
ws = wb.worksheets()[0]
ws.set_row(0, 30)
```

Or, by using `Format` objects:

```python
italic_format = wb.add_format({"italic": True})
ws.set_column(
    2, 3, 10, italic_format
)
```