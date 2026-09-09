import warnings
from pathlib import Path
from typing import Any, Dict, Optional, Union

import pandas as pd

from gptables.core.cover import Cover
from gptables.core.gptable import GPTable
from gptables.core.theme import Theme
from gptables.core.wrappers import GPWorkbook


def produce_workbook(
    filename: str,
    sheets: Dict[str, "GPTable"],
    theme: Optional["Theme"] = None,
    cover: Optional["Cover"] = None,
    contentsheet_label: str = "Contents",
    contentsheet_options: Optional[Dict[str, Any]] = None,
    contentsheet_location: str = "sheet",
    notes_table: Optional[pd.DataFrame] = None,
    notesheet_label: str = "Notes",
    notesheet_options: Optional[Dict[str, Any]] = None,
    auto_width: Union[bool, Dict[str, bool]] = True,
    gridlines: str = "hide_all",
    cover_gridlines: bool = False,
) -> GPWorkbook:
    """
    Produces a formatted workbook.

    Can be written to an `.xlsx` file as specified in `filename` using `.close()`.

    Parameters
    ----------
    filename : str
        path to write final workbook to (an `.xlsx` file)
    sheets : dict
        mapping worksheet labels to ``GPTable`` objects
    theme : gptables.Theme, optional
        formatting to be applied to GPTable elements. ``gptheme`` is used by
        default.
    cover : gptables.Cover, optional
        cover page text. Including this argument will generate a cover page.
    contentsheet_label : str
        table of contents sheet label, defaults to "Contents". If None, table
        of contents will not be generated.
    contentsheet_options : dict, optional
        dictionary of contentsheet customisation parameters. Valid keys are
        `additional_elements`, `column_names`, `table_name`, `title`,
        `subtitles` and `instructions`.
    contentsheet_location : str, optional
        where to place the table of contents. ``"sheet"`` (default) places it
        on its own worksheet named by ``contentsheet_label``. ``"cover"``
        appends it to the cover sheet. Requires ``cover`` to be provided when
        set to ``"cover"``.
    notes_table : pd.DataFrame, optional
        table with notes reference, text and (optional) link columns. If None,
        notes sheet will not be generated.
    notesheet_label : str, optional
        notes sheet label, defaults to "Notes"
    notesheet_options : dict, optional
        dictionary of notesheet customisation parameters. Valid keys are
        `table_name`, `title` and `instructions`.
    auto_width : bool or dict, optional
        If bool, applies to all sheets. If dict, should map sheet labels to bools.
    gridlines : string, optional
        option to hide or show gridlines on worksheets. "show_all" - don't
        hide gridlines, "hide_printed" - hide printed gridlines only, or
        "hide_all" - hide screen and printed gridlines.
    cover_gridlines : bool, optional
        indication if gridlines should apply to the cover worksheet. False
        by default.

    Returns
    -------
    workbook : gptables.GPWorkbook
    """
    valid_locations = ("sheet", "cover")
    if contentsheet_location not in valid_locations:
        raise ValueError(
            f"`contentsheet_location` must be one of {valid_locations},"
            f" got '{contentsheet_location}'"
        )
    if contentsheet_location == "cover" and cover is None:
        raise ValueError(
            "`contentsheet_location='cover'` requires a `cover` to be provided"
        )

    if contentsheet_options is None:
        contentsheet_options = {}
    if notesheet_options is None:
        notesheet_options = {}

    if isinstance(filename, Path):
        filename = filename.as_posix()

    wb = GPWorkbook(filename)

    if theme is not None:
        wb.set_theme(theme)

    cover_ws = None
    cover_pos = None
    if cover is not None:
        if cover_gridlines:
            cover_ws = wb.add_worksheet(cover.cover_label, gridlines=gridlines)
        else:
            cover_ws = wb.add_worksheet(cover.cover_label, gridlines="hide_all")
        cover_pos = cover_ws.write_cover(cover)

    contents_gptable = None
    if contentsheet_label is not None:
        if contentsheet_options:
            valid_keys = [
                "additional_elements",
                "column_names",
                "table_name",
                "title",
                "subtitles",
                "instructions",
            ]
            if not all(key in valid_keys for key in contentsheet_options.keys()):
                msg = (
                    "Valid `contentsheet_options` keys are 'additional_elements',"
                    "'column_names', 'table_name', 'title', 'subtitles', 'instructions'"
                )
                raise ValueError(msg)
        contents_gptable = wb.make_table_of_contents(sheets, **contentsheet_options)

    wb._update_annotations(sheets)

    contentsheet = {}
    if contents_gptable is not None:
        if contentsheet_location == "cover":
            if isinstance(auto_width, dict):
                toc_auto_width = auto_width.get(cover.cover_label, True)
            else:
                toc_auto_width = auto_width
            cover_ws.write_gptable(
                contents_gptable, toc_auto_width, [], start_pos=cover_pos
            )
            # Restore column A width: write_gptable auto-width overwrites the
            # width set by write_cover, making cover text wrap too narrowly.
            cover_ws.set_column(0, 0, cover.width)
        else:
            contentsheet = {contentsheet_label: contents_gptable}

    notesheet = {}
    if notes_table is None:
        warnings.warn("No note text provided, notes sheet has not been generated")
    else:
        note_gptable = wb.make_notesheet(notes_table, **notesheet_options)
        notesheet = {notesheet_label: note_gptable}

    sheets = {**contentsheet, **notesheet, **sheets}
    for label, gptable in sheets.items():
        ws = wb.add_worksheet(label, gridlines=gridlines)
        if isinstance(auto_width, dict):
            sheet_auto_width = auto_width.get(label, True)
        else:
            sheet_auto_width = auto_width
        ws.write_gptable(gptable, sheet_auto_width, wb._annotations)

    return wb


def write_workbook(
    filename: str,
    sheets: Dict[str, "GPTable"],
    theme: Optional["Theme"] = None,
    cover: Optional["Cover"] = None,
    contentsheet: Optional[str] = None,
    contentsheet_label: str = "Contents",
    contentsheet_options: Optional[Dict[str, Any]] = None,
    contentsheet_location: str = "sheet",
    notes_table: Optional[pd.DataFrame] = None,
    notesheet_label: str = "Notes",
    notesheet_options: Optional[Dict[str, Any]] = None,
    auto_width: Union[bool, Dict[str, bool]] = True,
    gridlines: str = "hide_all",
    cover_gridlines: bool = False,
) -> None:
    """
    Writes a formatted Excel workbook to `filename`.

    Parameters
    ----------
    filename : str
        Path to write final workbook to (an `.xlsx` file)
    sheets : dict
        mapping worksheet labels to ``GPTable`` objects
    theme : gptables.Theme, optional
        formatting to be applied to GPTable elements. ``gptheme`` is used by
        default.
    cover : gptables.Cover, optional
        cover page text. Including this argument will generate a cover page.
    contentsheet_label : str
        table of contents sheet label, defaults to "Contents". If None, table
        of contents will not be generated.
    contentsheet_options : dict, optional
        dictionary of contentsheet customisation parameters. Valid keys are
        `additional_elements`, `column_names`, `table_name`, `title`,
        `subtitles` and `instructions`
    contentsheet_location : str, optional
        where to place the table of contents. ``"sheet"`` (default) places it
        on its own worksheet named by ``contentsheet_label``. ``"cover"``
        appends it to the cover sheet. Requires ``cover`` to be provided when
        set to ``"cover"``.
    notes_table : pd.DataFrame, optional
        table with notes reference, text and (optional) link columns. If None,
        notes sheet will not be generated.
    notesheet_label : str, optional
        notes sheet label, defaults to "Notes"
    notesheet_options : dict, optional
        dictionary of notesheet customisation parameters. Valid keys are
        `table_name`, `title` and `instructions`.
    auto_width : bool, optional
        indicate if column widths should be automatically determined. True by
        default.
    gridlines : string, optional
        option to hide or show gridlines on worksheets. "show_all" - don't
        hide gridlines, "hide_printed" - hide printed gridlines only, or
        "hide_all" - hide screen and printed gridlines.
    cover_gridlines : bool, optional
        indication if gridlines should apply to the cover worksheet. False
        by default.

    Returns
    -------
    None
    """

    if contentsheet_options is None:
        contentsheet_options = {}
    if notesheet_options is None:
        notesheet_options = {}

    wb = produce_workbook(
        filename,
        sheets,
        theme,
        cover,
        contentsheet_label,
        contentsheet_options,
        contentsheet_location,
        notes_table,
        notesheet_label,
        notesheet_options,
        auto_width,
        gridlines,
        cover_gridlines,
    )
    wb.close()
