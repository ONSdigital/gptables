from pathlib import Path

import pytest
import yaml

from gptables.core.cover import Cover

EXAMPLE_CONFIG = Path(__file__).parents[1] / "examples/penguins_pages_config.yaml"


@pytest.fixture()
def config():
    with open(EXAMPLE_CONFIG) as f:
        return yaml.safe_load(f)


class TestYAMLConfigLoading:
    def test_config_file_loads(self, config):
        assert "cover" in config
        assert "notesheet" in config

    def test_cover_section_has_required_keys(self, config):
        assert "title" in config["cover"]
        assert "cover_label" in config["cover"]

    def test_notesheet_section_has_label(self, config):
        assert "label" in config["notesheet"]


class TestCoverFromConfig:
    def test_cover_built_from_config(self, config):
        cover = Cover(**config["cover"])
        assert isinstance(cover, Cover)

    def test_cover_title_matches_config(self, config):
        cover = Cover(**config["cover"])
        assert cover.title == config["cover"]["title"]

    def test_cover_label_matches_config(self, config):
        cover = Cover(**config["cover"])
        assert cover.cover_label == config["cover"]["cover_label"]


class TestNotesheetFromConfig:
    def test_notesheet_label_extracted(self, config):
        notesheet = config.get("notesheet", {})
        label = notesheet.get("label", "Notes")
        assert label == config["notesheet"]["label"]

    def test_notesheet_options_exclude_label(self, config):
        notesheet = config.get("notesheet", {})
        options = {k: v for k, v in notesheet.items() if k != "label"}
        assert "label" not in options

    def test_notesheet_options_contains_expected_keys(self, config):
        notesheet = config.get("notesheet", {})
        options = {k: v for k, v in notesheet.items() if k != "label"}
        valid_keys = {"table_name", "title", "instructions"}
        assert set(options.keys()).issubset(valid_keys)
