"""
Penguins - Wide vs Long Data Example
------------------------------------

This example demonstrates:
- The difference between wide and long data formats
- How to convert between them using pandas
- How to use gptables with both formats

See https://www.statology.org/long-vs-wide-data/ for an
overview of wide vs long data formats.
Also see https://tidyr.tidyverse.org/articles/tidy-data.html
for more on tidy data principles.
"""

from pathlib import Path

import pandas as pd

import gptables as gpt

# Read data
parent_dir = Path(__file__).parents[1]
penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

# --- Wide Format ---
# The original penguins_data is in wide format: each measurement is a separate column

wide_table = gpt.GPTable(
    table=penguins_data,
    table_name="penguins_wide",
    title="Penguins Dataset (Wide Format)",
    subtitles=[
        "Each measurement is a separate column.",
        "Wide format is common for spreadsheets and some analyses.",
    ],
    scope="Penguins",
    source="Palmer Station, Antarctica",
)

# --- Long Format ---
# Convert to long format using melt
# This example combines measurements into a single column
long_df = pd.melt(
    penguins_data,
    id_vars=["Species", "Island", "Sex"],
    value_vars=[
        "Culmen Length (mm)",
        "Culmen Depth (mm)",
        "Flipper Length (mm)",
        "Body Mass (g)",
    ],
    var_name="Measurement",
    value_name="Value",
)

long_table = gpt.GPTable(
    table=long_df,
    table_name="penguins_long",
    title="Penguins Dataset (Long Format)",
    subtitles=[
        "Measurements are stacked in a single column.",
        "Long format is preferred for tidy data and many analyses.",
    ],
    scope="Penguins",
    source="Palmer Station, Antarctica",
)

if __name__ == "__main__":
    output_path = parent_dir / "python_penguins_wide_long_gptable.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets={"Wide Format": wide_table, "Long Format": long_table},
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    print("Output written at: ", output_path)
