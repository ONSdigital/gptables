## Penguins - Custom Theme Example

This example demonstrates how to use a custom theme in the production of a workbook.

Summary statistics from the penguins dataset are used to build a `gptables.GPTable`
object. Elements of metadata are provided to the corresponding parameters of the class.
Where you wish to provide no metadata in required parameters, use `None`.

The theme parameter must take either a directory or a yaml file in the `gptables.write_workbook` function.
The yaml file used in this example can be found in the themes folder as ‘’penguins_test_theme.yaml’’.

```python

import pandas as pd

import gptables as gpt

# Read data
parent_dir = Path(__file__).parents[1]

penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

# Any data processing could go here as long as you end with a Pandas dataframe that you want to write in a spreadsheet

# Define table elements
penguins_table_name = "penguins_statistics"
penguins_title = "The Penguins Dataset"
penguins_subtitles = ["This is the first subtitle", "Just another subtitle"]
penguins_scope = "Penguins"
penguins_source = "Palmer Station, Antarctica"

kwargs = {
    "table_name": penguins_table_name,
    "title": penguins_title,
    "subtitles": penguins_subtitles,
    "scope": penguins_scope,
    "source": penguins_source,
}
penguins_table = gpt.GPTable(table=penguins_data, **kwargs)

penguins_sheets = {"Penguins": penguins_table}

# Use write_workbook to win!
# Simply pass the filepath of the yaml file containing your theme to the GPTables Theme class and then to write_workbook
if __name__ == "__main__":
    output_path = parent_dir / "python_penguins_gptable.xlsx"
    theme_path = str(Path(__file__).parent.parent / "themes/penguins_test_theme.yaml")
    gpt.write_workbook(
        filename=output_path,
        sheets=penguins_sheets,
        theme=gpt.Theme(theme_path),
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    print("Output written at: ", output_path)
```

```python
import pandas as pd

import gptables as gpt

# Read data
parent_dir = Path(__file__).parents[1]

penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

# Any data processing could go here as long as you end with a Pandas dataframe that you want to write in a spreadsheet

# Define table elements
penguins_table_name = "penguins_statistics"
penguins_title = "The Penguins Dataset"
penguins_subtitles = ["This is the first subtitle", "Just another subtitle"]
penguins_scope = "Penguins"
penguins_source = "Palmer Station, Antarctica"

kwargs = {
    "table_name": penguins_table_name,
    "title": penguins_title,
    "subtitles": penguins_subtitles,
    "scope": penguins_scope,
    "source": penguins_source,
    "index_columns": {
        2: 0
    },  # The level 2 index from our Pandas dataframe is put in the first (zeroth with Python indexing) column of the spreadsheet
}

# Define our GPTable
penguins_table = gpt.GPTable(
    table=penguins_data, table_name="penguins_statistics", **kwargs
)

penguins_sheets = {"Penguins": penguins_table}

penguins_cover = gpt.Cover(
    cover_label="Cover",
    title="A Workbook containing two copies of the data",
    intro=["This is some introductory information", "And some more"],
    about=["Even more info about my data", "And a little more"],
    contact=[
        "John Doe",
        "Tel: 345345345",
        "Email: [john.doe@snailmail.com](mailto:john.doe@snailmail.com)",
    ],
)

# Use write_workbook to win!
if __name__ == "__main__":
    output_path = parent_dir / "python_penguins_cover_gptable.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets=penguins_sheets,
        cover=penguins_cover,
    )
    print("Output written at: ", output_path)
```

<a id="module-gptables.examples.penguins_notes"></a>
