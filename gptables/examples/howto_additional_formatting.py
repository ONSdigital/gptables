from pathlib import Path

import pandas as pd

import gptables as gpt

parent_dir = Path(__file__).parents[1]
penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

formatted_subtitles = [
    "The first subtitle",
    [{"bold": True}, "This", " is another subtitle"],
]

sample_additional_formatting = [
    {
        "column": {
            "columns": ["Species", "Island"],
            "format": {
                "align": "center",
                "italic": True,
            },
        }
    },
    {"column": {"columns": [3], "format": {"left": 1}}},
    {
        "row": {
            "rows": -1,
            "format": {
                "bottom": 1,
                "indent": 2,
            },
        }
    },
]

penguins_table = gpt.GPTable(
    table=penguins_data,
    table_name="penguins_statistics",
    title="The Palmer Penguins Dataset",
    subtitles=formatted_subtitles,
    scope="Penguins",
    source="Palmer Station, Antarctica",
    additional_formatting=sample_additional_formatting,
)

penguins_sheets = {"Penguins": penguins_table}

if __name__ == "__main__":
    output_path = parent_dir / "gpt_additional_formatting.xlsx"
    wb = gpt.produce_workbook(filename=output_path, sheets=penguins_sheets)
    wb.close()
    print("Output written at: ", output_path)
