"""
Tutorial - Using a Config File for Cover and Notes Pages
---------------------------------------------------------
This example demonstrates how to load a YAML config file to define settings
for the introduction (cover) and notes pages, and pass them to write_workbook().
"""

from pathlib import Path

import pandas as pd
import yaml

import gptables as gpt

parent_dir = Path(__file__).parents[1]
penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

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

config_path = Path(__file__).parent / "penguins_pages_config.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

cover = gpt.Cover(**config["cover"])

notesheet = config.get("notesheet", {})
notesheet_label = notesheet.get("label", "Notes")
notesheet_options = {k: v for k, v in notesheet.items() if k != "label"}

if __name__ == "__main__":
    output_path = parent_dir / "gpt_tutorial_config_file.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets={"Penguins": penguins_table},
        notes_table=penguins_notes_table,
        cover=cover,
        notesheet_label=notesheet_label,
        notesheet_options=notesheet_options,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    print("Output written at: ", output_path)
