"""
Penguins - End-to-End Example
--------------------------------------------

This example demonstrates a full workflow:
- Data loading
- Cleaning (handling missing values, renaming columns, recoding values)
- Rounding measurement columns
- Converting between wide and long formats
- Preparing data for gptables
- Applying additional formatting

"""

from pathlib import Path

import pandas as pd

import gptables as gpt

# Read data
parent_dir = Path(__file__).parents[1]
penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

# --- Data Cleaning ---
# Drop rows with missing values in columns other than "Comments"
cols_to_check = [col for col in penguins_data.columns if col != "Comments"]
cleaned = penguins_data.dropna(subset=cols_to_check)

# Rename columns
cleaned = cleaned.rename(
    columns={
        "Culmen Length (mm)": "Bill Length (mm)",
        "Culmen Depth (mm)": "Bill Depth (mm)",
    }
)

# Recode Sex column
cleaned["Sex"] = cleaned["Sex"].replace({"MALE": "M", "FEMALE": "F"})

# --- Rounding ---
# Round measurement columns to nearest integer
measurement_cols = [
    "Bill Length (mm)",
    "Bill Depth (mm)",
    "Flipper Length (mm)",
    "Body Mass (g)",
]
for col in measurement_cols:
    if col in cleaned.columns:
        cleaned[col] = cleaned[col].round(0).astype("Int64")

# --- Wide to Long Conversion ---
# Example: melt measurements into a long format
long_df = pd.melt(
    cleaned,
    id_vars=["Species", "Island", "Sex"],
    value_vars=[
        "Bill Length (mm)",
        "Bill Depth (mm)",
        "Flipper Length (mm)",
        "Body Mass (g)",
    ],
    var_name="Measurement",
    value_name="Value",
)
# --- Prepare for gptables ---
table_name = "penguins_long_format"
title = "Penguins Dataset (Long Format Example)"
subtitles = ["Demonstrates data cleaning, rounding, and wide-to-long conversion."]
scope = "Penguins"
source = "Palmer Station, Antarctica"

# Additional formatting: highlight 'Value' column
additional_formatting = [
    {"column": {"columns": ["Value"], "format": {"bg_color": "#DDEEFF"}}}
]

penguins_table = gpt.GPTable(
    table=long_df,
    table_name=table_name,
    title=title,
    subtitles=subtitles,
    scope=scope,
    source=source,
    additional_formatting=additional_formatting,
)

if __name__ == "__main__":
    output_path = parent_dir / "python_penguins_end_to_end_gptable.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets={"Penguins (Long Format)": penguins_table},
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
    )
    print("Output written at: ", output_path)
