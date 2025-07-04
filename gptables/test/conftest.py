import pandas as pd
import pytest

from gptables.core.gptable import GPTable


@pytest.fixture(scope="function")
def create_gptable_with_kwargs():

    def generate_gptable(format_dict=None):
        base_gptable = {
            "table": pd.DataFrame(),
            "table_name": "table_name",
            "title": "",
            "index_columns": {},  # Override default, as no columns in table
        }
        if format_dict is not None:
            base_gptable.update(format_dict)
        return GPTable(**base_gptable)

    return generate_gptable
