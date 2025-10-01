# GPTable

## Mapping

The `GPTable` Class is used to map your data and metadata to table elements.
The supported table elements are represented like this in the output .xlsx file:

![Cells A1 to A6 contain the title, subtitles, instructions, legend, source and scope. These parameters are mapped individually. The next row contains the column headings. Within the same row but on a new line are the units. The table note references are within the same row on a new line under the units. In columns 1, 2 and 3 of the next row down are index levels 1, 2 and 3. In the next columns are the data. Column headings, indices and data are supplied as a pandas DataFrame. Units and table note references are mapped individually.](static/table_mapping.png)

## Notes

Notes are text elements that appear on the separately generated `Notesheet`.

Notes can be referenced in the `title`, `subtitles`, `scope`, `source`
and `legend` elements. Notes corresponding to entries in the data can be
referenced using the `table_notes` element. This will add a note reference to
the relevant column heading. Note references cannot be added to data cells, as
inserting references here would reduce the usability of the data. We use double
dollar symbols (`$$`) to denote notes in text. For example, a note could be
referenced as `"My table title $$Reference$$"`.

References in text are replaced with numbers, in increasing order from the top-
left corner of the first sheet containing a data table.

See this in practice under [Example Usage](usage.md#example-usage).

#### NOTE
Deprecated in v1.1.0: Ability to reference notes within
`GPTable.table.columns` will be removed in v2 of gptables. Please use
`GPTable.table_notes` to ensure references are correctly placed and ordered.

## Links

Links can added to text using the format `[display text](link)`. Links are
supported in the `title`, `subtitles`, `scope`, `source``and ``legend`
elements. They will also be applied to cells within the data table that use
this format. Links should start with one of the following prefixes:
`http://`, `https://`, `ftp://`, `mailto:`, `internal:` or
`external:`. For more information about the usage of the local URIs, see the
[XlsxWriter documentation](https://xlsxwriter.readthedocs.io/worksheet.html#worksheet-write-url).

#### NOTE
Excel does not support links being applied to specific words within
cells. The link will be applied to the whole cell, not just the
display text.

## Rich Text

Rich text is text that contains mixed formatting. You shouldn’t use formatting
to represent data or important information, as most formatting is neither
accessible nor machine readable. You can still use to make things look
appealing for sighted people.

Rich text is supported in the `title`, `subtitles`, `scope`, `source`
and `legend` elements. Where you would normally provide a string to a
parameter, you can instead provide a list of strings and dictionaries.
Dictionaries in this list should contain valid [XlsxWriter format properties](https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties)
and values. The formatting defined in these dictionaries will be applied to the
next string in the list. This formatting is applied in addition to the
formatting of that element specified in the [`Theme`](doc.theme.md#gptables.core.theme.Theme).

`["It is ", {"bold": True}, "inevitable"]` would give you “It is **inevitable**”.

See this in practice under [Example Usage](usage.md#example-usage).

#### NOTE
Rich text is not currently supported if the cell also contains note
references or links. This may be changed in the future if there is
sufficient user need, so please raise an issue if this is functionality
you need.

## Additional formatting

In some cases you may want to apply one-off formatting on specific rows, columns or cells of the data.
As mentioned above, this formatting should not be used to represent data or important information.

Bespoke formatting can be applied to an individual `GPTable` via the `additional_formatting` parameter,
when creating a `GPTable` instance. This parameter takes a list of dictionaries, where each dictionary
defines formatting for one or more rows, columns or cells.

These dictionaries have a single key indicating the type of selection, from “column”, “row” or “cell”.
Their value is another dictionary, which specifies the indexing, formatting and whether row and column
indexes are included in the selection.

Indexing supports selection of columns by name or 0-indexed number, but rows and cells can only
be indexed by number. Numeric indexing refers to position within the data element of the table (column
headings, row indexes and data), not position in the output Excel sheet.

This `additional_formatting` parameter is best demonstrated by example:

```python
additional_formatting = [
      # Align data center, but not column indexes
      {"column":
            {"columns": ["some_column", "another_column"],  # str, int or list of either
            "format": {"align": "center"},
            "include_names": False  # Whether to include column headings (optional)
            }
      },

      # Align column left, including column index
      {"column":
            {"columns": [3],
            "format": {"left": 1},
            "include_names": True
            }
      },

      # Underline the bottom of the table, including row index
      {"row":
            {"rows": -1,  # Numbers only, but can refer to last row using -1
            "format": {"bottom": 1},  # Underline row
            "include_names": True  # Whether to include row indexes
            }
      },

      # A bad example, turning a single cell's font red
      {"cell":
            {"cells": (3, 3),  # tuple or list of tuples (numbers only)
            "format": {"font_color": "red"}
            }
      }
]
```

### Formatting methods

The following tables show the Excel format categories, along with an example demonstrating the syntax required
for use in gptables. Some formatting methods use indexing to map to Excel’s built-in formats. This information
can be found in the applicable sections below.

#### Font formatting

This table demonstrates the font formatting methods available. You can find all options
for [underline styles in the XlsxWriter documentation](https://xlsxwriter.readthedocs.io/format.html#format-set-underline).

| Description     | Example usage                                                                           |
|-----------------|-----------------------------------------------------------------------------------------|
| Font type       | {“font_name”: “Arial”}                                                                  |
| Font size       | {“font_size”: 30}                                                                       |
| Font colour     | {“font_color”: “red”}                                                                   |
| Bold            | {“bold”: True}                                                                          |
| Italic          | {“italic”: True}                                                                        |
| Underline       | {“underline”: 1}                                                                        |
| Strikeout       | {“font_strikeout”: True}                                                                |
| Super/Subscript | {“font_script”: 1} # Superscript<br/><br/><br/>{“font_script”: 2} # Subscript<br/><br/> |

#### Number formatting

This table demonstrates how to set the numeric format using indexing and string arguments. You can find all
options for [numeric formats in the XlsxWriter documentation](https://xlsxwriter.readthedocs.io/format.html#format-set-num-format).

| Description    | Example usage                                                                                         |
|----------------|-------------------------------------------------------------------------------------------------------|
| Numeric format | {“num_format”: 1} # Format index<br/><br/><br/>{“num_format”: “d mmm yyyy”} # Format string<br/><br/> |

#### Protection formatting

This table demonstrates the protection methods available.

| Description   | Example usage    |
|---------------|------------------|
| Lock cells    | {“locked”: True} |
| Hide formulas | {“hidden”: True} |

#### Alignment formatting

This table demonstrates the alignment formatting options available. You can find all options for
[horizontal and vertical alignment in the XlsxWriter documentation](https://xlsxwriter.readthedocs.io/format.html#format-set-align).

| Description      | Example usage               |
|------------------|-----------------------------|
| Horizontal align | {“align”: “center”}         |
| Vertical align   | {“align”: “vcenter”}        |
| Rotation         | {“rotation”: 30}            |
| Text wrap        | {“text_wrap”: True}         |
| Center across    | {“set_center_across”: True} |
| Indentation      | {“indentation”:2}           |
| Shrink to fit    | {“shrink”: True}            |

#### Pattern formatting

This table demonstrates the pattern formatting options available.

| Description       | Example usage         |
|-------------------|-----------------------|
| Cell pattern      | {“pattern”: 1}        |
| Background colour | {“bg_color”: “white”} |
| Foreground colour | {“fg_color”: “white”} |

#### Border formatting

This table demonstrates the border formatting options available. You can find all options
for [border styles in the XlsxWriter documentation](https://xlsxwriter.readthedocs.io/format.html#format-set-border).

| Description   | Example usage              |
|---------------|----------------------------|
| Cell border   | {“border”: 1}              |
| Bottom border | {“bottom”: 1}              |
| Top border    | {“top”: 1}                 |
| Left border   | {“left”: 1}                |
| Right border  | {“right”: 1}               |
| Border colour | {“border_color”: “red”}    |
| Bottom colour | {“bottom_color”:”#FF0000”} |
| Top colour    | {“top_color”: “red”}       |
| Left colour   | {“left_color”: “#FF0000”}  |
| Right colour  | {“right_color”: “red”}     |

For any formatting beyond this, if the package should support it then please raise an issue
or create a pull request. Otherwise, you will need to modify the underlying
[`GPWorkbook`](doc.wrappers.md#gptables.core.wrappers.GPWorkbook) or [`GPWorksheet`](doc.wrappers.md#gptables.core.wrappers.GPWorksheet) objects
before they are written to Excel.

See this in practice under [Example Usage](usage.md#example-usage).

## `GPTable` Class

### *class* gptables.core.gptable.GPTable(table, table_name, title, scope=None, source=None, units=None, table_notes=None, subtitles=[], instructions='', legend=[], index_columns={2: 0}, additional_formatting=[])

A Good Practice Table. Stores a table and metadata for writing a table
to excel.

#### NOTE
Deprecated in v1.1.0: Ability to reference notes within
`GPTable.table.columns` will be removed in v2 of gptables. Please use
`GPTable.table_notes` to ensure references are correctly placed and ordered.

#### table

table to be written to an Excel workbook

* **Type:**
  pandas.DataFrame

#### table_name

name for table. Should be unique with no spaces and always begin with a
letter, an underscore character, or a backslash. Use letters, numbers,
periods, and underscore characters for the rest of the name.

* **Type:**
  str

#### title

title of the table

* **Type:**
  str

#### subtitles

subtitles as a list of strings

* **Type:**
  List[str], optional

#### instructions

instructions on how to read the sheet. If not provided, defaults to
“This worksheet contains one table. Some cells may refer to notes,
which can be found on the notes worksheet.”

* **Type:**
  str, optional

#### scope

description of scope/basis of data in table if not included in title

* **Type:**
  str, optional

#### source

description of the source of the data in table if not included in cover

* **Type:**
  str, optional

#### units

units used in each (dict) column of table

* **Type:**
  dict, optional

#### legend

descriptions of special notation used in table

* **Type:**
  list, optional

#### index_columns

mapping an index level to a 0-indexed column as {level: column}.
Default is a level two index in the first column ({2: 0}).

* **Type:**
  dict, optional

#### additional_formatting

table-specific formatting for columns, rows or individual cells

* **Type:**
  dict, optional

#### add_legend(new_legend)

Add a single legend entry to the existing legend list.

#### add_subtitle(new_subtitle)

Add a single subtitle to the existing list of subtitles.

#### set_additional_formatting(new_formatting)

Set a dictionary of additional formatting to be applied to this table.

#### set_index_columns(new_index_columns)

Set the index_columns attribute. Overwrites any existing values.
A dict must be supplied. This dict should map index level to a
single 0-indexed column number. All other columns will be considered
as data columns.

#### set_instructions(new_instructions)

Set instructions attribute.

#### set_legend(new_legend, overwrite=True)

Set a list of legend entries to the legend attribute. Overwrites
existing legend entries by default. If overwrite is False, new entries
are appended to the legend list.

#### set_scope(new_scope)

Set the scope attribute.

#### set_source(new_source)

Set the source attribute to the specified str.

#### set_subtitles(new_subtitles, overwrite=True)

Set a list of subtitles to the subtitles attribute. Overwrites
existing ist of subtitles by default. If overwrite is False, new list
is appended to existing list of subtitles.

#### set_table(new_table, new_index_columns=None, new_units=None, new_table_notes=None)

Set the table, index_columns, units and table_notes attributes. Overwrites
existing values for these attributes.

#### set_table_name(new_table_name)

Set the table_name attribute.

#### set_table_notes(new_table_notes)

Adds note references to column headers.
table_notes should be in the format {column: “$$note_reference$$”}.
Column can be column name or 0-indexed column number in table.

#### set_title(new_title)

Set the title attribute.

#### set_units(new_units)

Adds units to column headers.
Units should be in the format {column: units_text}. Column can be column name or 0-indexed column
number in table.
