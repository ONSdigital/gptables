# API functions

#### NOTE
`auto_width` functionality is experimental - any feedback is welcome!
It currently does not account for alternative fonts, font sizes or font wrapping.

## Table of contents

By default, the API functions will add a table of contents sheet to your
Excel workbook. This will contain a single table with two columns. The first
column will contain the worksheet label and link for each worksheet in the
workbook. The second column will contain a description of the sheet contents.
By default, this is the title of the `GPTable` in that sheet. This
description can be customised by passing additional elements from the
`GPTable` into the `contentsheet_options` parameter. This parameter also
allows for customisation of the table of contents `title`, `subtitles`,
`table_name`, `instructions` and `column_names`.

To customise the worksheet label, pass the new label into the
`contentsheet_label` parameter. This table of contents functionality can be
disabled by setting this parameter to `False`.

See this in practice under [Example Usage](usage.md#example-usage).

## Notes sheet

A notes sheet will be generated if the API functions are provided with a
`notes_table`. The first column of the `notes_table` should contain a
meaningful reference for each note. This reference can then be used in the
worksheets - see the GPTable documentation for more details. When the notes
sheet is produced, this column will be replaced by the order the notes are
referenced in throughout the workbook.

The second column should contain the text for each note. Optional additional
columns can be used for useful links, formatted as `"[display text](link)"`.

The notes sheet can be customised using the `notesheet_options` parameter.
Values for the `title`, `table_name` and `instructions` can be provided
here. To customise the worksheet label, pass the new label into the
`notesheet_label` parameter.

If a `notes_table` is not provided, the notes sheet will not be generated.

See this in practice under [Example Usage](usage.md#example-usage).

## `write_workbook` function

### gptables.core.api.write_workbook(filename, sheets, theme=None, cover=None, contentsheet=None, contentsheet_label='Contents', contentsheet_options={}, notes_table=None, notesheet_label='Notes', notesheet_options={}, auto_width=True, gridlines='hide_all', cover_gridlines=False)

Writes a GPWorkbook to the specified .xlsx file.

This is an alternative main function that will take in data and theme
information. It calls upon the package to write a formatted .xlsx
file to the specified path.

#### NOTE
Deprecated in v1.1.0: contentsheet will be removed
in v2, it is replaced by contentsheet_label

* **Parameters:**
  * **filename** (*str*) – Path to write final workbook to (an .xlsx file)
  * **sheets** (*dict*) – mapping worksheet labels to `GPTable` objects
  * **theme** (*gptables.Theme* *,* *optional*) – formatting to be applied to GPTable elements. `gptheme` is used by
    default.
  * **cover** (*gptables.Cover* *,* *optional*) – cover page text. Including this argument will generate a cover page.
  * **contentsheet_label** (*str*) – table of contents sheet label, defaults to “Contents”. If None, table
    of contents will not be generated.
  * **contentsheet_options** (*dict* *,* *optional*) – dictionary of contentsheet customisation parameters. Valid keys are
    additional_elements, column_names, table_name, title,
    subtitles and instructions
  * **note_table** (*pd.DataFrame* *,* *optional*) – table with notes reference, text and (optional) link columns. If None,
    notes sheet will not be generated.
  * **notesheet_label** (*str* *,* *optional*) – notes sheet label, defaults to “Notes”
  * **notesheet_options** (*dict* *,* *optional*) – dictionary of notesheet customisation parameters. Valid keys are
    table_name, title and instructions.
  * **auto_width** (*bool* *,* *optional*) – indicate if column widths should be automatically determined. True by
    default.
  * **gridlines** (*string* *,* *optional*) – option to hide or show gridlines on worksheets. “show_all” - don’t
    hide gridlines, “hide_printed” - hide printed gridlines only, or
    “hide_all” - hide screen and printed gridlines.
  * **cover_gridlines** (*bool* *,* *optional*) – indication if gridlines should apply to the cover worksheet. False
    by default.
  * **contentsheet** (*str*) – alias for contentsheet_label, deprecated in v1.1.0
* **Return type:**
  None

## `produce_workbook` function

### gptables.core.api.produce_workbook(filename, sheets, theme=None, cover=None, contentsheet_label='Contents', contentsheet_options={}, notes_table=None, notesheet_label='Notes', notesheet_options={}, auto_width=True, gridlines='hide_all', cover_gridlines=False)

Produces a GPWorkbook, ready to be written to the specified .xlsx file
using the `.close()` method.

* **Parameters:**
  * **filename** (*str*) – path to write final workbook to (an .xlsx file)
  * **sheets** (*dict*) – mapping worksheet labels to `GPTable` objects
  * **theme** (*gptables.Theme* *,* *optional*) – formatting to be applied to GPTable elements. `gptheme` is used by
    default.
  * **cover** (*gptables.Cover* *,* *optional*) – cover page text. Including this argument will generate a cover page.
  * **contentsheet_label** (*str*) – table of contents sheet label, defaults to “Contents”. If None, table
    of contents will not be generated.
  * **contentsheet_options** (*dict* *,* *optional*) – dictionary of contentsheet customisation parameters. Valid keys are
    additional_elements, column_names, table_name, title,
    subtitles and instructions.
  * **notes_table** (*pd.DataFrame* *,* *optional*) – table with notes reference, text and (optional) link columns. If None,
    notes sheet will not be generated.
  * **notesheet_label** (*str* *,* *optional*) – notes sheet label, defaults to “Notes”
  * **notesheet_options** (*dict* *,* *optional*) – dictionary of notesheet customisation parameters. Valid keys are
    table_name, title and instructions.
  * **auto_width** (*bool* *,* *optional*) – indicate if column widths should be automatically determined. True
    by default.
  * **gridlines** (*string* *,* *optional*) – option to hide or show gridlines on worksheets. “show_all” - don’t
    hide gridlines, “hide_printed” - hide printed gridlines only, or
    “hide_all” - hide screen and printed gridlines.
  * **cover_gridlines** (*bool* *,* *optional*) – indication if gridlines should apply to the cover worksheet. False
    by default.
* **Returns:**
  **workbook**
* **Return type:**
  gptables.GPWorkbook
