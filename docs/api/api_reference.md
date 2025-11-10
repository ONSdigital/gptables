# API Reference

<h2>Functions</h2>

| Object                | Description               |
|-----------------------|---------------------------|
| [`produce_workbook()`](functions/produce_workbook.md) | Creates a formatted workbook suitable for further editing. |
| [`write_workbook()`](functions/write_workbook.md) | Creates and Writes out a formatted workbook. |

<h2>Classes</h2>
| Object                | Description               |
|-----------------------|---------------------------|
| [`Cover`](classes/cover.md) | Stores information for the cover sheet of a workbook. |
| [`GPTable`](classes/gptable.md) | Stores information about data in a table. |
| [`GPWorkbook`](classes/gpworkbook.md) | Wrapper for `XlsxWriter.Workbook` to support further editing after `produce_workbook()` |
| [`GPWorksheet`](classes/gpworksheet.md) | Wrapper for `XlsxWriter.Worksheet` to support further editing after `produce_workbook()` |
| [`Theme`](classes/theme.md) | Used to set the formatting of various elements throughout the workbook. |
