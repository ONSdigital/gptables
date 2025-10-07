# XlsxWriter wrappers

These Classes are only likely used following use
of the [`produce_workbook()`](api.md#produce_workbook-function) API function,
which returns a [`GPWorkbook`](wrappers.md#gpworkbook-class) object.

You may use these objects to carry out modification of any aspects of the
workbook or individual worksheets that are outside of the scope of `GPTables`.
To see this in practice, see the additional formatting example under usage.
Please also see the XlsxWriter documentation on their [Workbook](https://xlsxwriter.readthedocs.io/workbook.html) and [Worksheet](https://xlsxwriter.readthedocs.io/worksheet.html) Classes,
which are super-classses of those below, for details on further modfication.

The methods which we’ve extended these Classes with are not shown here, but feel
free to check out the source code to see how `gptables` works under the hood.

## `GPWorkbook` Class

### *class* gptables.core.wrappers.GPWorkbook(filename=None, options={})

Wrapper for and XlsxWriter Workbook object. The Worksheets class has been
replaced by an alternative with a method for writting GPTable objects.

## `GPWorksheet` Class

### *class* gptables.core.wrappers.GPWorksheet

Wrapper for an XlsxWriter Worksheet object. Provides a method for writing
a good practice table (GPTable) to a Worksheet.
