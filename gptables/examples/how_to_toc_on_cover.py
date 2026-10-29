"""
Example showing how to place the table of contents on the cover sheet
instead of a separate worksheet.
"""

from pathlib import Path

import pandas as pd

import gptables as gpt

parent_dir = Path(__file__).parents[1]
penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

penguins_table = gpt.GPTable(
    table=penguins_data,
    table_name="penguins_statistics",
    title="The Palmer Penguins Dataset",
    subtitles=["Summary statistics for Palmer penguins"],
    scope="Penguins",
    source="Palmer Station, Antarctica",
)

penguins_sheets = {"Penguins": penguins_table}

penguins_cover = gpt.Cover(
    cover_label="Cover",
    title="Palmer Penguins Dataset",
    intro=[
        "This spreadsheet contains a table of data from the palmerpenguins package.",
    ],
    about=[
        "Additional information about this publication can go here.",
    ],
    contact=[
        "Tel: 01234 567890",
        "Email: [example@email.address](mailto:example@email.address)",
    ],
)

if __name__ == "__main__":
    output_path = parent_dir / "gpt_toc_on_cover.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets=penguins_sheets,
        cover=penguins_cover,
        contentsheet_label="Table of contents",
        contentsheet_location="cover",  # places ToC on the cover sheet
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    print("Output written at: ", output_path)
