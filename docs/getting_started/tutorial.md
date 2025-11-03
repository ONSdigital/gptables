# Getting started with `gptables`

## Installation
To install gptables, simply use:

```
pip install gptables
```

## Tutorial

gptables helps produce consistently structured and formatted tables.

This section demonstrates basic use of the gptables with the Penguins dataset. More indepth information can be found in the how-tos and API docs.

The tutorial code can be run from the
[examples](https://github.com/ONSdigital/gptables/tree/main/gptables/examples) folder.

### Starting out

This example looks at how to produce a basic gptables spreadsheet of data from the Palmer Penguins dataset.
The data is first read in for presentation. Next, information about the data is supplied to
gptables. Then this information is used by gptables to produce the spreadsheet object. Finally, we
write out the spreadsheet.

First, import `gptables` alongside any other necessary packages so that the data can be read in. Any
additional preparation like cleaning can be done here, and the output should be a `pandas.DataFrame`.


```python
from pathlib import Path
import pandas as pd
import gptables as gpt

penguins_data = pd.read_csv("penguins.csv")
```

Then construct the `GPTable`, defining some main elements. These will be displayed in the resulting
spreadsheet.

```python
penguins_table = gpt.GPTable(
    table = penguins_data,
    table_name = "penguins_statistics",
    title = "The Palmer Penguins Dataset",
    subtitles = ["This is the first subtitle",
                 "This is another subtitle"],
    scope = "Penguins",
    source = "Palmer Station, Antarctica",
)
```

If preferred, this can alternatively be done using a dictionary of keyword arguments:

```python
kwargs = {
    "table_name": "penguins_statistics",
    "title": "The Palmer Penguins Dataset",
    "subtitles": ["This is the first subtitle",
                 "This is another subtitle"],
    "scope": "Penguins",
    "source": "Palmer Station, Antarctica",
}

penguins_table = gpt.GPTable(table = penguins_data, **kwargs)
```

Each table should be associated to a sheet name for writing. Collate the sheets with their names in
a dictionary:

```python
penguins_sheets = {"Penguins": penguins_table}
```

Finally, use `gptables.write_workbook()` to create and write out the workbook with the output path,
the sheets, and any additional elements.

```python
gpt.write_workbook(
    filename="python_penguins_gptable.xlsx",
    sheets=penguins_sheets,
    contentsheet_options={"additional_elements": ["subtitles", "scope"]},
)
```

`gptables` creates a table of contents, with worksheet labels linking to the worksheets, and a description of their contents. There is a sheet with the dataset, and it presents the
specified details in a minimal style with text of a legible font and size.

![](../static/getting_started_before_and_after.png)

The code is combined below in an extendable tab.

??? "Starting out"
    ```python
    from pathlib import Path
    import pandas as pd
    import gptables as gpt

    penguins_data = pd.read_csv("penguins.csv")

    penguins_table = gpt.GPTable(
        table = penguins_data,
        table_name = "penguins_statistics",
        title = "The Palmer Penguins Dataset",
        subtitles = ["This is the first subtitle",
                    "This is another subtitle"],
        scope = "Penguins",
        source = "Palmer Station, Antarctica",
    )

    penguins_sheets = {"Penguins": penguins_table}

    gpt.write_workbook(
        filename="python_penguins_gptable.xlsx",
        sheets=penguins_sheets,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    ```

### Table of contents

The description column in the table of contents can be customised by passing additional
elements from the `GPTable` into the `contentsheet_options` parameter
of `gptables.write_workbook()`.

`contentsheet_options` can take `additional_elements`, such as `'subtitles'`, `'scope'`,
`'source'`, or `'instructions'` to give more information about individual sheets within
the workbook:

```python
    penguins_table = gpt.GPTable(
        ...
        instructions="This workbook contains a single sheet. The name is a link to it."
        subtitles=["This is the first subtitle", "This is another subtitle"],
        scope="Penguins",
        source="Palmer Station, Antarctica",
        ...
    )

    ...

    gpt.write_workbook(
        filename=output_path,
        sheets=penguins_sheets,
        contentsheet_options={"additional_elements": ["instructions", "subtitles", "scope", "source"]},
    )
```

![](../static/table_of_contents_additional_elements.png)

`contentsheet_options` also allows for customisation of the table of contents `title`, `subtitles`,
`table_name`, `instructions` and `column_names`. For example:

```python
    gpt.write_workbook(
        filename=output_path,
        sheets=penguins_sheets,
        contentsheet_options={"title": "A title for the table of contents",
                                "subtitles": ["A subtitle for the table of contents"],
                                "additional_elements": ["subtitles", "scope"]},
    )
```

![](../static/table_of_contents_customisation.png)

Set `contentsheet_label = None` inside `gptables.write_workbook()` to disable creating
a table of contents.

More information can be found in the [function documentation](../api/functions.md#gptables.core.api.write_workbook).

### Penguins - Notes Example

This example demonstrates how to include notes in a GPTable. Notes cannot
be included in data cells but may appear either in column headers or in text such
as titles, subtitles, etc.

Placeholders for notes are put in using the notation, $$note$$. The actual note text
must be provided as a Pandas dataframe to the notes_table argument of the `gptables.write_workbook` function.
This dataframe should contain the text of the placeholder, the actual text you want in the note and (optionally)
any hyperlinks you want in the note.

```python
from pathlib import Path

import pandas as pd

import gptables as gpt

# Read data
parent_dir = Path(__file__).parents[1]

penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

# Any data processing could go here as long as you end with a Pandas dataframe that you want to write in a spreadsheet

# Define table elements

penguins_table_name = "penguins_statistics"

# Notes are added by using $$note$$ in text
penguins_title = "The Penguins Dataset$$noteabouty$$"
penguins_subtitles = [
    "This is the first subtitle$$noteaboutx$$",
    "Just another subtitle",
]

# Notes can also be included in column headers, see below
penguins_table_notes = {
    "species": "$$noteaboutx$$",
    2: "$$noteaboutz$$",
}  # Columns can be referenced either by index or by name
penguins_units = {
    2: "mm",
    "bill_depth_mm": "mm",
    4: "mm",
    "body_mass_g": "g",
}  # As above for column referencing
penguins_scope = "Penguins"
penguins_source = "Palmer Station, Antarctica"

kwargs = {
    "table_name": penguins_table_name,
    "title": penguins_title,
    "subtitles": penguins_subtitles,
    "units": penguins_units,
    "table_notes": penguins_table_notes,
    "scope": penguins_scope,
    "source": penguins_source,
}

# Define our GPTable
penguins_table = gpt.GPTable(table=penguins_data, **kwargs)

penguins_sheets = {"Penguins": penguins_table}

# Notesheet - Note that the ordering of each list only matters with respect to the other lists in the "notes" dictionary.
# GPTables will use the "Note reference" list to ensure the "Note text" is assigned correctly
notes = {
    "Note reference": ["noteaboutz", "noteaboutx", "noteabouty"],
    "Note text": [
        "This is a note about z linking to google.",
        "This is a note about x linking to duckduckgo.",
        "This is a note about y linking to the ONS website.",
    ],
    "Useful link": [
        "[google](https://www.google.com)",
        "[duckduckgo](https://duckduckgo.com/)",
        "[ONS](https://www.ons.gov.uk)",
    ],
}
penguins_notes_table = pd.DataFrame.from_dict(notes)

# Use write_workbook to win!
if __name__ == "__main__":
    output_path = parent_dir / "python_penguins_gptable.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets=penguins_sheets,
        notes_table=penguins_notes_table,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    print("Output written at: ", output_path)
```

### Cover Sheet Example

This example uses the [Starting out](tutorial.md#starting-out) example above, and adds a cover sheet to the workbook.

Cover sheets can be used to provide information that is general to all tables in a workbook. See the [Analysis Function Guidance](https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/#section-11) for more information about what to include in a cover sheet, and how to make sure it is accessible.

Note: Cover sheets are added as the first sheet in the workbook when written by `gptables`. This is important when applying additional formatting to other worksheets by their index in the workbook.

To include a cover sheet, first map your text elements to the attributes of a [Cover](../api/cover.md) object:

```python
penguins_cover = gpt.Cover(
    cover_label = "Cover",
    title = "Palmer Penguins Dataset",
    intro=[
        "This spreadsheet contains a table of data obtained from the palmerpenguins package",
        "This is intended to be a simple example of how to use the gptables package to create a spreadsheet with a cover sheet and data sheets.",
    ],
    about=[
        "Additional information about your publication can go here",
    ],
    contact=[
        "Tel: 01234 567890",
        "Email: [example@email.address](mailto: example@email.address)",
    ],
)
```
This will automatically create a cover sheet with the subheadings "Introductory information", "About these data", and "Contact" where these attributes are included.

Add additional formatting to create further subheadings as needed:

```python
penguins_cover = gpt.Cover(
    cover_label = "Cover",
    title = "Palmer Penguins Dataset",
    intro=[
        "This spreadsheet contains a table of data obtained from the palmerpenguins package",
        "This an example of how to use the gptables package to create a spreadsheet with a cover sheet and data sheets.",
    ],
    about=[
        "Additional information about your publication can go here",
        [{"bold": True}, "Publication dates"],
        "This data tables in this spreadsheet were originally published at 7:00am 01 January 2025.",
        "The next publication will be published at 7:00am 01 January 2026.",
        [{"bold": True}, "Methodology notes"],
        "Information on methodology can be useful to users of your data",
        [{"bold": True}, "Notes, blank cells and units"],
        "Some cells in the tables refer to notes which can be found in the notes worksheet. Note markers are presented in square brackets, for example: [note 1].",
        "Blank cells indicate no data. An explanation of why there is no data is given in the notes worksheet.",
        "Some column headings give units, when this is the case the units are presented in round brackets to differentiate them from note markers.",
    ],
    contact=[
        "Tel: 01234 567890",
        "Email: [example@email.address](mailto: example@email.address)",
    ],
)

```

Finally, pass the cover object to the `cover_sheet` argument of the `gptables.write_workbook()` function:

```python
gpt.write_workbook(
    filename="python_penguins_gptable_with_cover.xlsx",
    sheets=penguins_sheets,
    cover_sheet=penguins_cover,
    contentsheet_options={"additional_elements": ["subtitles", "scope"]},
)
```
The resulting cover sheet is shown below.

![](../static/cover_sheet.png)

The code is combined below in an extendable tab.

??? "Adding a cover sheet"
    ```python
    from pathlib import Path
    import pandas as pd
    import gptables as gpt

    penguins_data = pd.read_csv("penguins.csv")

    penguins_table = gpt.GPTable(
        table = penguins_data,
        table_name = "penguins_statistics",
        title = "The Palmer Penguins Dataset",
        subtitles = ["This is the first subtitle",
                    "This is another subtitle"],
        scope = "Penguins",
        source = "Palmer Station, Antarctica",
    )

    penguins_sheets = {"Penguins": penguins_table}

    penguins_cover = gpt.Cover(
        cover_label = "Cover",
        title = "Palmer Penguins Dataset",
        intro=[
            "This spreadsheet contains a table of data obtained from the palmerpenguins package",
            "This is intended to be a simple example of how to use the gptables package to create a spreadsheet with a cover sheet and data sheets.",
        ],
        about=[
            "Additional information about your publication can go here",
            [{"bold": True}, "Publication dates"],
            "Date published: 01 January 2025.",
            "Next release: 01 January 2026.",
            [{"bold": True}, "Methodology notes"],
            "Information on methodology can be useful to users of your data",
            [{"bold": True}, "Notes, blank cells and units"],
            "Some cells in the tables refer to notes which can be found in the notes worksheet. Note markers are presented in square brackets, for example: [note 1].",
            "Blank cells indicate no data. An explanation of why there is no data is given in the notes worksheet, see the column headings for which notes you should refer to.",
            "Some column headings give units, when this is the case the units are presented in round brackets to differentiate them from note markers.",
        ],
        contact=[
            "Tel: 01234 567890",
            "Email: [example@email.address](mailto: example@email.address)",
        ],
    )

    gpt.write_workbook(
        filename="python_penguins_gptable.xlsx",
        sheets=penguins_sheets,
        cover=penguins_cover,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    ```

### Multiple sheets

This example uses the [Starting out](tutorial.md#starting-out) example above, and adds a second data sheet to the workbook.

To include another data sheet, you must construct another `GPTable`, similarly to how it was done with a single data sheet. This extra sheet can have it's own unique elements, including data.
```python
penguins_table_1 = gpt.GPTable(
    table=penguins_data_1,
    table_name="penguins_statistics_1",
    title="The Palmer Penguins Dataset (Sheet 1)",
    subtitles=["This is the first subtitle", "This is another subtitle"],
    scope="Penguins",
    source="Palmer Station, Antarctica",
)

penguins_table_2 = gpt.GPTable(
    table=penguins_data_2,
    table_name="penguins_statistics_2",
    title="The Palmer Penguins Dataset (Sheet 2)",
    subtitles=["This is the first subtitle for sheet 2", "Another subtitle for sheet 2"],
    scope="Penguins",
    source="Palmer Station, Antarctica",
)
```

Each table should be associated to a sheet name for writing. Collate the sheets with their names in a dictionary:

```python
penguins_sheets = {
        "Penguins 1": penguins_table_1,
        "Penguins 2": penguins_table_2
    }
```

Finally, use `gptables.write_workbook()` to create and write out the workbook with the output path, the sheets, and any additional elements.

```python
gpt.write_workbook(
    filename="python_penguins_gptable.xlsx",
    sheets=penguins_sheets,
    contentsheet_options={"additional_elements": ["subtitles", "scope"]},
)
```

The code is combined below in an extendable tab.

??? "Multiple sheets"
    ```python
    from pathlib import Path
    import pandas as pd
    import gptables as gpt


    # Read the CSV once
    penguins_data = pd.read_csv("penguins.csv")

    # Split the penguins data into two halves, keeping the first 3 colums as keys.
    penguins_data_1 = penguins_data.iloc[:, :10]
    penguins_data_2 = pd.concat([penguins_data.iloc[:, :3], penguins_data.iloc[:, 10:]], axis=1)

    # Create two different GPTable objects
    penguins_table_1 = gpt.GPTable(
        table=penguins_data_1,
        table_name="penguins_statistics_1",
        title="The Palmer Penguins Dataset (Sheet 1)",
        subtitles=["This is the first subtitle", "This is another subtitle"],
        scope="Penguins",
        source="Palmer Station, Antarctica",
    )

    penguins_table_2 = gpt.GPTable(
        table=penguins_data_2,
        table_name="penguins_statistics_2",
        title="The Palmer Penguins Dataset (Sheet 2)",
        subtitles=["This is the first subtitle for sheet 2", "Another subtitle for sheet 2"],
        scope="Penguins",
        source="Palmer Station, Antarctica",
    )

    # Add both tables to the sheets dictionary
    penguins_sheets = {
        "Penguins 1": penguins_table_1,
        "Penguins 2": penguins_table_2
    }

    gpt.write_workbook(
        filename="python_penguins_gptable.xlsx",
        sheets=penguins_sheets,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    ```
