from pathlib import Path

import pandas as pd

import gptables as gpt

parent_dir = Path(__file__).parents[1]
penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

penguins_table = gpt.GPTable(
    table=penguins_data,
    table_name="penguins_statistics",
    title="The Palmer Penguins Dataset$$note_about_x$$",
    subtitles=[
        "This is the first subtitle$$note_about_y$$",
        "This is another subtitle",
    ],
    scope="Penguins",
    source="Palmer Station, Antarctica",
)

penguins_sheets = {"Penguins": penguins_table}

notes = {
    "Note reference": [
        "note_about_x",
        "note_about_y",
        "note_about_z",
        "note_with_no_link",
    ],
    "Note text": [
        "This is a note about x linking to google.",
        "This is a note about y linking to duckduckgo.",
        "This is a note about z linking to the ONS website.",
        "This is a note with no link.",
    ],
    "Useful link": [
        "[google](https://www.google.com)",
        "[duckduckgo](https://duckduckgo.com/)",
        "[ONS](https://www.ons.gov.uk)",
        None,
    ],
}
penguins_notes_table = pd.DataFrame.from_dict(notes)

if __name__ == "__main__":
    output_path = parent_dir / "gpt_adding_notes.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets=penguins_sheets,
        notes_table=penguins_notes_table,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    print("Output written at: ", output_path)
