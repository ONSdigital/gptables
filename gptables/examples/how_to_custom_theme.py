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

if __name__ == "__main__":
    output_path = parent_dir / "gpt_custom_theme.xlsx"
    theme_path = str(Path(__file__).parent.parent / "themes/example_theme_basic.yaml")
    gpt.write_workbook(
        filename=output_path,
        sheets=penguins_sheets,
        theme=gpt.Theme(theme_path),
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    print("Output written at: ", output_path)
