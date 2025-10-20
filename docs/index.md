# Good Practice Tables (gptables)

[![Actions build status](https://github.com/best-practice-and-impact/gptables/workflows/continuous-integration/badge.svg)](https://github.com/best-practice-and-impact/gptables/actions)[![PyPI release](https://badge.fury.io/py/gptables.svg)](https://badge.fury.io/py/gptables)

`gptables` produces Excel spreadsheets that follow much of the
[Analysis Function guidance](https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/) on
releasing statistics in spreadsheets. This aims to implement digital accessibility standards like
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) as well as follow other good practice, such as the use of notes on cover sheets. `gptables` helps users by creating spreadsheets consistently and more quickly than implementing this manually.

## Features
Some of the key features of `gptables` outputs are:

* A minimalist presentation style
* Coloured and underlined hyperlinks
* Default text formatting in legible fonts and sizes
* Formatted tables of contents and cover sheets
* The ability to use custom themes to adapt `gptables` outputs to your needs

![](static/getting_started_before_and_after.png)

**Note**: This package does not create perfectly accessible spreadsheets. Users should refer to the releasing statistics in spreadsheets [guidance](https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/) and the [spreadsheet accessibility checklist](https://analysisfunction.civilservice.gov.uk/policy-store/making-spreadsheets-accessible-a-brief-checklist-of-the-basics/) to
ensure the standards are completely met.

## Get in touch
Get in touch at [ASAP@ons.gov.uk](mailto:ASAP@ons.gov.uk) if you use `gptables` - we'd love to feature your work on the [examples](reference/examples.md) page, and get any feedback on how we make `gptables` even better.

Got a feature request, or found a bug? Raise an [issue](https://github.com/ONSdigital/gptables/issues) on GitHub.

## Related Packages
Users may also be interested in [aftables](https://best-practice-and-impact.github.io/aftables/), an R native equivalent to
`gptables`, and [csvcubed](https://onsdigital.github.io/csvcubed-docs/external/), a package for turning data and metadata into
machine-readable CSV-W files.
