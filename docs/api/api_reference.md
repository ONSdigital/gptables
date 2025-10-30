# API Reference

| Object                | Description               |
|-----------------------|---------------------------|
| `produce_workbook()` | Creates a formatted workbook suitable for further editing. |
| `write_workbook()` | Creates and Writes out a formatted workbook. |
| `GPWorkbook` | Wrapper for `XlsxWriter.Workbook` to support further editing after `produce_workbook()` |
| `GPWorksheet` | Wrapper for `XlsxWriter.Worksheet` to support further editing after `produce_workbook()` |
| `GPTable` | Stores information about data in a table. |
| `Cover` | Stores information for the cover sheet of a workbook. |
| `Theme` | Used to set the formatting of various elements throughout the workbook. |
