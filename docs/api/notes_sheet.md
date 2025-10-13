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

See this in practice in the [Tutorial](../getting_started/usage.md#penguins-notes-example).