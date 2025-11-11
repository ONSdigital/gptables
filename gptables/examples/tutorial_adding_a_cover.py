from pathlib import Path

import pandas as pd

import gptables as gpt

parent_dir = Path(__file__).parents[1]
penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

penguins_table = gpt.GPTable(
    table=penguins_data,
    table_name="penguins_statistics",
    title="The Palmer Penguins Dataset",
    subtitles=["This is the first subtitle", "This is another subtitle"],
    scope="Penguins",
    source="Palmer Station, Antarctica",
)

penguins_sheets = {"Penguins": penguins_table}

penguins_cover = gpt.Cover(
    cover_label="Cover",
    title="Palmer Penguins Dataset",
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

if __name__ == "__main__":
    output_path = parent_dir / "gpt_adding_cover.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets=penguins_sheets,
        cover=penguins_cover,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    print("Output written at: ", output_path)
