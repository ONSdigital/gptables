# API Reference

## Functions

| Object                | Description               |
|-----------------------|---------------------------|
| [`produce_workbook()`](produce_workbook.md) | Creates a formatted workbook suitable for further editing. |
| [`write_workbook()`](write_workbook.md) | Creates and Writes out a formatted workbook. |

## Classes
| Object                | Description               |
|-----------------------|---------------------------|
| [`Cover`](cover.md) | Stores information for the cover sheet of a workbook. |
| [`GPTable`](gptable.md) | Stores information about data in a table. |
| [`GPWorkbook`](gpworkbook.md) | Wrapper for `XlsxWriter.Workbook` to support further editing after `produce_workbook()` |
| [`GPWorksheet`](gpworksheet.md) | Wrapper for `XlsxWriter.Worksheet` to support further editing after `produce_workbook()` |
| `Theme` | Used to set the formatting of various elements throughout the workbook. |
