# XlsxWriter wrappers

These Classes are only likely used following use
of the [`produce_workbook()`](functions.md#gptables.core.api.produce_workbook) API function,
which returns a [`GPWorkbook`](wrappers.md#gptables.core.wrappers.GPWorkbook) object.

You may use these objects to carry out modification of any aspects of the
workbook or individual worksheets that are outside of the scope of `GPTables`.
To see this in practice, see the additional formatting example under usage.
Please also see the XlsxWriter documentation on their [Workbook](https://xlsxwriter.readthedocs.io/workbook.html) and [Worksheet](https://xlsxwriter.readthedocs.io/worksheet.html) Classes,
which are super-classses of those below, for details on further modfication.

The methods which we’ve extended these Classes with are not shown here, but feel
free to check out the source code to see how `gptables` works under the hood.

::: gptables.core.wrappers.GPWorkbook
    options:
        heading: "GPWorkbook"

&nbsp;

::: gptables.core.wrappers.GPWorksheet
    options:
        heading: "GPWorksheet"
