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

See this in practice in the [Tutorial](../getting_started/usage.md#cover-page-example).