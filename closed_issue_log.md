# Closed Issue Log

This log documents feature requests that we do not currently intend to implement in gptables.
This is due to the request being non-compliant with Analysis Function [spreadsheet accessibility guidance][guidance].
These issues may be re-opened in future if guidance changes - please contribute to the discussion by heading to
the GitHub issue.

## [180][issue-180]: Multiple tables in a single spreadsheet
Section 13 of the guidance, 'Worksheets with multiple tables', dissuades this.\w

[guidance]: https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/
[issue-180]: https://github.com/best-practice-and-impact/gptables/issues/180

## [265][issue-265]: Rounding decimals
A user requested the ability to round a column to a given number of decimal places. This issue was closed because it can be handled by pandas.

[pandas]: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.round.html
[issue-265]: https://github.com/best-practice-and-impact/gptables/issues/265
