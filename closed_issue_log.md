# Closed Issue Log

This log documents feature requests that we do not currently intend to offer in gptables.
This is due to the request being non-compliant with Analysis Function [spreadsheet accessibility guidance][guidance],
or otherwise being out of scope of the package, designed for implementing this guidance.
These issues may be re-opened in future if guidance changes - please contribute to the discussion by heading to
the GitHub issue.

## [180][issue-180]: Multiple tables in a single spreadsheet (05/08/2025)
Section 13 of the guidance, 'Worksheets with multiple tables', dissuades this.

## [265][issue-265]: Rounding decimals (02/09/2025)
A user requested the ability to round a column to a given number of decimal places. This issue was closed because it can be handled by [pandas][pandas-decimal-rounding].

## [136][issue-136]: Add hyperlinks to Theme format elements (05/09/2025)
Section 7 of the guidance, under 'Making hyperlinks accessible' says links should be underlined and in a colour of suitable
contrast. Further advice was sought from the Presentation Champions group, with the feedback that users expect links to be blue.

[guidance]: https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/
[issue-136]: https://github.com/best-practice-and-impact/gptables/issues/136
[issue-180]: https://github.com/best-practice-and-impact/gptables/issues/180
[issue-265]: https://github.com/best-practice-and-impact/gptables/issues/265
[pandas-decimal-rounding]: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.round.html
