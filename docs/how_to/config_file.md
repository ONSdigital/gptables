# Using a config file for cover and notes pages

A YAML config file can be used to define the content and settings for the introduction (cover) page
and the notes page, rather than passing them as arguments directly to `write_workbook()` or
`produce_workbook()`. This is useful when the same cover and notes configuration is reused across
multiple scripts, or when you want to separate publication metadata from data processing code.

The sample code can be run from the
[examples](https://github.com/ONSdigital/gptables/tree/main/gptables/examples) folder.

## Creating a config file

A pages config file is a YAML file with two optional top-level sections: `cover` and `notesheet`.

```yaml
cover:
  cover_label: "Cover"
  title: "Publication Title"
  intro:
    - "Introductory text paragraph."
    - "Second introductory paragraph."
  about:
    - "About these data."
  contact:
    - "Tel: 01234 567890"
    - "Email: example@email.address"
  width: 85

notesheet:
  label: "Notes"
  title: "Notes"
  instructions: "This worksheet contains one table."
```

Valid keys for each section are:

| Section | Key | Description |
|---|---|---|
| `cover` | `title` | Cover page title (required) |
| `cover` | `cover_label` | Tab label (default `"Cover"`) |
| `cover` | `intro` | List of introductory text paragraphs |
| `cover` | `about` | List of "about these data" paragraphs |
| `cover` | `contact` | List of contact detail paragraphs |
| `cover` | `width` | Column width in characters (default `85`) |
| `notesheet` | `label` | Sheet tab label (default `"Notes"`) |
| `notesheet` | `title` | Notes page title (default `"Notes"`) |
| `notesheet` | `table_name` | Notes table name (default `"notes_table"`) |
| `notesheet` | `instructions` | Notes page instructions text |

### Rich text in the config

Bold or otherwise formatted subheadings can be added to `intro`, `about` and `contact` using
nested YAML lists where the first element is a format dictionary:

```yaml
about:
  - "Plain paragraph."
  - - {bold: true, font_size: 14}
    - "Bold subheading"
  - "Another plain paragraph."
```

## Using the config in Python

Load the YAML file, build the `Cover` object, and extract the notesheet settings before
passing them to `write_workbook()`:

```python
import yaml
import gptables as gpt

with open("penguins_pages_config.yaml") as f:
    config = yaml.safe_load(f)

cover = gpt.Cover(**config["cover"])

notesheet = config.get("notesheet", {})
notesheet_label = notesheet.get("label", "Notes")
notesheet_options = {k: v for k, v in notesheet.items() if k != "label"}

gpt.write_workbook(
    filename="output.xlsx",
    sheets={"Penguins": penguins_table},
    notes_table=penguins_notes_table,
    cover=cover,
    notesheet_label=notesheet_label,
    notesheet_options=notesheet_options,
)
```

## Full example

??? "Using a config file"

    **`penguins_pages_config.yaml`**
    ```yaml
    cover:
      cover_label: "Cover"
      title: "Palmer Penguins Dataset"
      intro:
        - "This spreadsheet contains a table of data obtained from the palmerpenguins package."
        - "This example demonstrates how to use a config file to define cover and notes page settings."
      about:
        - - {bold: true}
          - "About the data"
        - "The Palmer Penguins dataset contains size measurements for three penguin species."
        - - {bold: true}
          - "Notes, blank cells and units"
        - "Some cells refer to notes which can be found in the notes worksheet."
      contact:
        - "Tel: 01234 567890"
        - "Email: example@email.address"

    notesheet:
      label: "Notes"
      title: "Notes"
      instructions: "This worksheet contains one table. Note numbers correspond to references in the data sheets."
    ```

    **`tutorial_config_file.py`**
    ```python
    from pathlib import Path

    import yaml
    import pandas as pd
    import gptables as gpt

    penguins_data = pd.read_csv("penguins.csv")

    penguins_table = gpt.GPTable(
        table=penguins_data,
        table_name="penguins_statistics",
        title="The Palmer Penguins Dataset$$note_about_x$$",
        subtitles=["This is the first subtitle", "This is another subtitle"],
        scope="Penguins",
        source="Palmer Station, Antarctica",
    )

    notes = {
        "Note reference": ["note_about_x"],
        "Note text": ["Data collected from the Palmer Station, Antarctica LTER."],
        "Useful link": ["[palmerpenguins](https://allisonhorst.github.io/palmerpenguins/)"],
    }
    penguins_notes_table = pd.DataFrame.from_dict(notes)

    with open("penguins_pages_config.yaml") as f:
        config = yaml.safe_load(f)

    cover = gpt.Cover(**config["cover"])
    notesheet = config.get("notesheet", {})
    notesheet_label = notesheet.get("label", "Notes")
    notesheet_options = {k: v for k, v in notesheet.items() if k != "label"}

    gpt.write_workbook(
        filename="gpt_tutorial_config_file.xlsx",
        sheets={"Penguins": penguins_table},
        notes_table=penguins_notes_table,
        cover=cover,
        notesheet_label=notesheet_label,
        notesheet_options=notesheet_options,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    ```
