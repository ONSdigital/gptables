from pathlib import Path
import pandas as pd
import gptables as gpt

parent_dir = Path(__file__).parents[1]
penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

penguins_data_1 = penguins_data.iloc[:, :10]
penguins_data_2 = pd.concat([penguins_data.iloc[:, :3], penguins_data.iloc[:, 10:]], axis=1)


penguins_table_1 = gpt.GPTable(
    table=penguins_data_1,
    table_name="penguins_statistics_1",
    title="The Palmer Penguins Dataset (Sheet 1)",
    subtitles=["This is the first subtitle", "This is another subtitle"],
    scope="Penguins",
    source="Palmer Station, Antarctica",
)

penguins_table_2 = gpt.GPTable(
    table=penguins_data_2,
    table_name="penguins_statistics_2",
    title="The Palmer Penguins Dataset (Sheet 2)",
    subtitles=["This is the first subtitle for sheet 2", "Another subtitle for sheet 2"],
    scope="Penguins",
    source="Palmer Station, Antarctica",
)


penguins_sheets = {
    "Penguins 1": penguins_table_1,
    "Penguins 2": penguins_table_2
}

if __name__ == "__main__":
    output_path = parent_dir / "gpt_adding_datasheets.xlsx"
    gpt.write_workbook(filename=output_path,
                       sheets=penguins_sheets,
                       contentsheet_options={"additional_elements": ["subtitles", "scope"]})
    print("Output written at: ", output_path)
