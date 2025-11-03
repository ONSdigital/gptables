# API Reference

## Functions

| Object                | Description               |
|-----------------------|---------------------------|
| `produce_workbook()` | Creates a formatted workbook suitable for further editing. |
| `write_workbook()` | Creates and Writes out a formatted workbook. |

## Classes
| Object                | Description               |
|-----------------------|---------------------------|
| `Cover` | Stores information for the cover sheet of a workbook. |
| `GPTable` | Stores information about data in a table. |
| `GPWorkbook` | Wrapper for `XlsxWriter.Workbook` to support further editing after `produce_workbook()` |
| `GPWorksheet` | Wrapper for `XlsxWriter.Worksheet` to support further editing after `produce_workbook()` |
| `Theme` | Used to set the formatting of various elements throughout the workbook. |
