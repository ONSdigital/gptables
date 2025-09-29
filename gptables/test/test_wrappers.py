from collections import namedtuple

import pandas as pd
import pytest
import xlsxwriter
from pandas.testing import assert_frame_equal, assert_series_equal

import gptables
from gptables import Theme, gptheme
from gptables.core.gptable import FormatList
from gptables.core.wrappers import GPWorkbook, GPWorksheet
from gptables.test.test_gptable import does_not_raise

Tb = namedtuple("Testbook", "wb ws")

valid_text_elements = [  # Not None
    "This is a string",
    FormatList(["More than ", {"italic": True}, "just ", "a string"]),
    FormatList([{"bold": True}, "text"]),
]

test_text_list = [
    "This has a $$reference$$",
    "This one doesn't",
    "Here's $$another$$one",
]

exp_text_list = ["This has a [note 1]", "This one doesn't", "Here's one[note 2]"]


invalid_text_elements = [dict(), set(), 42, 3.14, True]


@pytest.fixture()
def testbook():
    # See https://github.com/jmcnamara/XlsxWriter/issues/746#issuecomment-685869888
    wb = GPWorkbook(options={"in_memory": True})
    ws = wb.add_worksheet()
    yield Tb(wb, ws)
    wb.fileclosed = 1


class TestGPWorksheetInit:
    """
    Test that default attributes are set when GPWorksheets are created.
    """

    def test_subclass(self):
        """
        Test that the GPWorksheet class is a subclass of the XlsxWriter
        Worksheet class.
        """
        assert issubclass(GPWorksheet, xlsxwriter.worksheet.Worksheet)

    def test_default_theme_set(self, testbook):
        """
        Test that the default theme (gptheme) is used when no theme is set.
        """
        assert testbook.wb.theme == gptheme

    def test_default_gridlines(self, testbook):
        """
        Test that print and screen gridlines are hidden by default.
        """
        assert testbook.ws.print_gridlines == 0
        assert testbook.ws.screen_gridlines == 0

    def test_wb_reference(self, testbook):
        """
        Test that GPWorksheets reference their parent GPWorkbook.
        """
        assert testbook.ws._workbook == testbook.wb

    @pytest.mark.parametrize(
        "not_a_gptable", [dict(), set(), [], 1, 3.14, "test_string", pd.DataFrame()]
    )
    def test_invalid_write_gptable(self, not_a_gptable, testbook):
        """
        Test that write_gptable() raises a TypeError when argument is not a
        gptables.GPTable object.
        """
        with pytest.raises(TypeError):
            testbook.ws.write_gptable(not_a_gptable)


class TestGPWorksheetWriting:
    """
    Test that additional writing methods correctly write to GPWorksheet object.
    """

    def test__smart_write_str(self, testbook):
        """
        Test that strings are stored in the GPWorksheet as expected.
        """
        testbook.ws._smart_write(0, 0, valid_text_elements[0], {})
        # Strings are stored in a lookup table for efficiency
        got_string = testbook.ws.str_table.string_table
        exp_string = {valid_text_elements[0]: 0}
        assert got_string == exp_string

        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        got_lookup = testbook.ws.table[0][0][0]
        exp_lookup = 0
        assert got_lookup == exp_lookup

    def test__smart_write_formatted_str(self, testbook):
        testbook.ws._smart_write(1, 2, valid_text_elements[0], {"bold": True})
        # Strings are stored in a lookup table for efficiency
        got_string = testbook.ws.str_table.string_table
        exp_string = {valid_text_elements[0]: 0}
        assert got_string == exp_string

        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        cell = testbook.ws.table[1][2]
        got_lookup = cell[0]
        exp_lookup = 0
        assert got_lookup == exp_lookup

        format_obj = cell[1]
        assert format_obj.bold

    def test__smart_write_rich_text(self, testbook):
        testbook.wb.set_theme(Theme({}))

        testbook.ws._smart_write(0, 0, valid_text_elements[1], {})
        # Strings are stored in a lookup table for efficiency
        got_string = testbook.ws.str_table.string_table
        exp_string = {
            '<r><t xml:space="preserve">More than </t></r><r><rPr><i'
            '/><sz val="11"/><color theme="1"/><rFont val="Calibri"/'
            '><family val="2"/><scheme val="minor"/></rPr><t xml:spa'
            'ce="preserve">just </t></r><r><rPr><sz val="11"/><color'
            ' theme="1"/><rFont val="Calibri"/><family val="2"/><sch'
            'eme val="minor"/></rPr><t>a string</t></r>': 0
        }
        assert got_string == exp_string

        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        got_lookup = testbook.ws.table[0][0][0]
        exp_lookup = 0
        assert got_lookup == exp_lookup

    def test__smart_write_formatted_rich_text(self, testbook):
        testbook.wb.set_theme(Theme({}))

        testbook.ws._smart_write(1, 2, valid_text_elements[1], {})
        # Strings are stored in a lookup table for efficiency
        got_string = testbook.ws.str_table.string_table
        exp_string = {
            '<r><t xml:space="preserve">More than </t></r><r><rPr>'
            '<i/><sz val="11"/><color theme="1"/><rFont val="Calib'
            'ri"/><family val="2"/><scheme val="minor"/></rPr><t xml'
            ':space="preserve">just </t></r><r><rPr><sz val="11"'
            '/><color theme="1"/><rFont val="Calibri"/><family val="'
            '2"/><scheme val="minor"/></rPr><t>a string</t></r>': 0
        }

        assert got_string == exp_string

        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        cell = testbook.ws.table[1][2]
        got_lookup = cell[0]
        exp_lookup = 0
        assert got_lookup == exp_lookup

    def test__smart_write_link(self, testbook):
        testbook.wb.set_theme(Theme({}))

        display_text = "gov.uk"
        url = "https://www.gov.uk/"

        testbook.ws._smart_write(0, 0, {display_text: url}, {})

        got_string = testbook.ws.str_table.string_table
        exp_string = {display_text: 0}
        assert got_string == exp_string

        got_hyperlink = testbook.ws.hyperlinks[0][0]._link
        exp_hyperlink = url
        assert got_hyperlink == exp_hyperlink

        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        cell = testbook.ws.table[0][0]

        got_lookup = cell[0]
        exp_lookup = 0
        assert got_lookup == exp_lookup

        format_obj = cell[1]
        assert format_obj.underline is True
        assert format_obj.font_color._rgb_hex_value() == "0000FF"  # aka Blue

    def test__smart_write_null_cell(self, testbook):
        testbook.ws._smart_write(0, 0, None, {})
        # Strings are stored in a lookup table for efficiency
        got_string = testbook.ws.str_table.string_table
        exp_string = {}
        assert got_string == exp_string

        # Strings referenced using a named tuple (string, Format)
        # When cell has no content, tuple only contains Format
        cell = testbook.ws.table[0][0]
        assert len(cell) == 1

    def test__write_empty_table(self, testbook, create_gptable_with_kwargs):
        gptable = create_gptable_with_kwargs({"table": pd.DataFrame({"col": [None]})})
        with pytest.raises(ValueError):
            testbook.ws._write_table_elements([0, 0], gptable, auto_width=True)

    def test__write_integer_table(self, testbook, create_gptable_with_kwargs):
        gptable = create_gptable_with_kwargs(
            {"table": pd.DataFrame({"a": [0], "b": [1]})}
        )

        # Testing that this function executes with no errors
        testbook.ws._write_table_elements([0, 0], gptable, auto_width=True)

    @pytest.mark.parametrize(
        "cell_value1,cell_value2,expectation",
        [
            (None, "valid text", pytest.warns(UserWarning)),
            ("", "valid text", pytest.warns(UserWarning)),
            (" ", "valid text", pytest.warns(UserWarning)),
            ("    ", "valid text", pytest.warns(UserWarning)),
            ("_", "valid text", pytest.raises(ValueError)),
            (" *", "valid text", pytest.raises(ValueError)),
            (" Hello_World! ", "valid text", does_not_raise()),
        ],
    )
    def test__write_table_elements_cell_validation(
        self,
        testbook,
        create_gptable_with_kwargs,
        cell_value1,
        cell_value2,
        expectation,
    ):
        gptable = create_gptable_with_kwargs(
            {
                "table": pd.DataFrame(
                    {
                        "colA": [cell_value1, cell_value2],
                        "colB": ["valid text", "valid text"],
                    }
                )
            }
        )
        with expectation:
            testbook.ws._write_table_elements([0, 0], gptable, auto_width=True)

    def test__apply_column_alignments(self, testbook):
        data_table = pd.DataFrame(
            {
                "index_column": [1, 2],
                "integer_column": [1, 2],
                "float_column": [1.1, 2.2],
                "string_column": ["A", "B"],
                "url_column": [{"display_text": "link"}, {"display_text": "link"}],
                "integer_with_confidential_shorthand": [1, "[c]"],
                "float_with_significant_shorthand": ["1.1[sss]", 2.2],
            }
        )

        format_table = pd.DataFrame(
            {
                "index_column": [{}, {}],
                "integer_column": [{}, {}],
                "float_column": [{}, {}],
                "string_column": [{}, {}],
                "url_column": [{}, {}],
                "integer_with_confidential_shorthand": [{}, {}],
                "float_with_significant_shorthand": [{}, {}],
            }
        )

        testbook.ws._apply_column_alignments(
            data_table, format_table, index_columns=[0]
        )

        exp_format_table = pd.DataFrame(
            {
                "index_column": [{"align": "left"}, {"align": "left"}],
                "integer_column": [{"align": "right"}, {"align": "right"}],
                "float_column": [{"align": "right"}, {"align": "right"}],
                "string_column": [{"align": "left"}, {"align": "left"}],
                "url_column": [{"align": "left"}, {"align": "left"}],
                "integer_with_confidential_shorthand": [
                    {"align": "right"},
                    {"align": "right"},
                ],
                "float_with_significant_shorthand": [
                    {"align": "right"},
                    {"align": "right"},
                ],
            }
        )

        assert_frame_equal(format_table, exp_format_table)


class TestGPWorksheetReferences:
    """
    Test that GPTable note references are modified correctly by GPWorksheet
    during write_gptable().
    """

    @pytest.mark.parametrize("text", test_text_list)
    def test__replace_reference(self, text, testbook):
        """
        Test that references ($$ref$$ style) in strings are replaced with
        [note n], in order of appearance. Also tests replacement in lists.
        """
        got_output = []
        reference_order = ["reference", "another"]

        got_output = [
            testbook.ws._replace_reference(text, reference_order)
            for text in test_text_list
        ]

        exp_refs = ["reference", "another"]
        assert reference_order == exp_refs
        assert got_output == exp_text_list

    @pytest.mark.parametrize(
        "text,refs,output",
        zip(
            test_text_list,
            [["reference"], [], ["another"]],
            ["This has a [note 1]", "This one doesn't", "Here's one[note 2]"],
        ),
    )
    def test__replace_reference_in_attr_str(self, text, refs, output, testbook):
        """
        Test that references are replaced in a single string.
        """
        reference_order = ["reference", "another"]
        got_text = testbook.ws._replace_reference_in_attr(text, reference_order)

        assert got_text == output

    def test__replace_reference_in_attr_dict(self, testbook):
        """
        Test that references are replaced in dictionary values, but not keys.
        """
        reference_order = ["reference", "another"]
        test_text_dict = {
            "$$key$$": "This is a value with a $$reference$$",
            "second_key": "Second value",
            "another_key": "$$another$$reference",
        }
        got_text = testbook.ws._replace_reference_in_attr(
            test_text_dict, reference_order
        )

        exp_text_dict = {
            "$$key$$": "This is a value with a [note 1]",
            "second_key": "Second value",
            "another_key": "reference[note 2]",
        }

        assert got_text == exp_text_dict


class TestGPWorksheetFormatUpdate:
    """
    Test that GPWorksheet format updating methods work as expected.
    """

    def test__apply_format_dict(self, testbook):
        test = dict()
        format_dict = {"bold": True}
        testbook.ws._apply_format(test, format_dict)
        exp = {"bold": True}
        assert test == exp

    def test__apply_format_series(self, testbook):
        test = pd.Series([{} for n in range(3)])
        format_dict = {"bold": True}
        testbook.ws._apply_format(test, format_dict)
        exp = pd.Series([{"bold": True} for n in range(3)])
        assert_series_equal(test, exp)

    def test__apply_format_dataframe(self, testbook):
        test = pd.DataFrame(columns=[0, 1, 2], index=[0, 1])
        test.iloc[0] = [{} for n in range(3)]
        test.iloc[1] = [{} for n in range(3)]

        format_dict = {"bold": True}
        testbook.ws._apply_format(test, format_dict)
        exp = pd.DataFrame(columns=[0, 1, 2], index=[0, 1])
        exp.iloc[0] = [{"bold": True} for n in range(3)]
        exp.iloc[1] = [{"bold": True} for n in range(3)]
        assert_frame_equal(test, exp)


class TestGPWorksheetTable:
    """
    Test that the table property inherited from `xlsxwriter.Worksheet` is set correctly.
    """

    def test__mark_data_as_worksheet_table(self, testbook, create_gptable_with_kwargs):
        df = pd.DataFrame({"col1": ["x", "y"], "col2": [0, 1]})
        gptable = create_gptable_with_kwargs(
            {
                "table": df,
            }
        )
        gptable._set_data_range()

        table_format = pd.DataFrame({"col1": [{}, {}], "col2": [{}, {}]})

        testbook.ws._write_array(
            [0, 2], df, table_format
        )  # First two rows reserved for title and instructions

        testbook.ws._mark_data_as_worksheet_table(gptable, table_format)

        assert len(testbook.ws.tables) == 1

        table = testbook.ws.tables[0]

        got_table_range = table["a_range"]
        exp_table_range = xlsxwriter.utility.xl_range(*gptable.data_range)

        assert got_table_range == exp_table_range

        assert table["name"] == gptable.table_name

        got_number_of_columns = len(table["columns"])
        exp_number_of_columns = df.shape[0]
        assert got_number_of_columns == exp_number_of_columns

        for n in range(got_number_of_columns):
            got_column_name = table["columns"][n]["name"]
            exp_column_name = df.columns[n]
            assert got_column_name == exp_column_name

            got_heading_format = table["columns"][n]["name_format"]
            exp_heading_format = testbook.wb.add_format(table_format.iloc[0, n])
            assert got_heading_format.__dict__ == exp_heading_format.__dict__

    @pytest.mark.parametrize(
        "data,format,exp_width",
        [
            # Single column, normal case
            (["string", "longer string"], [{"font_size": 12}, {"font_size": 12}], [93]),
            # Multiple columns
            (
                pd.DataFrame({"col1": ["a", "bb"], "col2": ["ccc", "dddd"]}),
                pd.DataFrame(
                    {
                        "col1": [{"font_size": 11}, {"font_size": 12}],
                        "col2": [{"font_size": 10}, {"font_size": 14}],
                    }
                ),
                [26, 50],
            ),
            # Bold formatting
            (
                ["bold", "bolder"],
                [{"font_size": 11, "bold": True}, {"font_size": 12, "bold": True}],
                [58],
            ),
            # Multi-line cell
            (
                ["short\nlongest\nmid", "tiny"],
                [{"font_size": 11}, {"font_size": 11}],
                [53],
            ),
            # Empty string
            (["", ""], [{"font_size": 11}, {"font_size": 11}], [0]),
            # Number cell
            ([123, 4567], [{"font_size": 11}, {"font_size": 11}], [35]),
        ],
    )
    def test__calculate_column_widths(self, testbook, data, format, exp_width):
        if isinstance(data, pd.DataFrame):
            table = data
            table_format = format
        else:
            table = pd.DataFrame({"col": data})
            table_format = pd.DataFrame({"col": format})

        got_width = testbook.ws._calculate_column_widths(table, table_format)
        assert got_width == exp_width
        assert all(isinstance(w, int) for w in got_width)

    @pytest.mark.parametrize(
        "format_dict,expected",
        [
            ({"font_size": 11, "bold": False}, 1.0),
            ({"font_size": 12, "bold": False}, 12 / 11),
            ({"font_size": 11, "bold": True}, 1.1),
            ({"font_size": 12, "bold": True}, (12 / 11) * 1.1),
            ({}, 1.0),
        ],
    )
    def test__get_scaling_factor(self, testbook, format_dict, expected):
        got = testbook.ws._get_scaling_factor(format_dict)
        assert got == expected

    @pytest.mark.parametrize(
        "cell_val,expected",
        [
            ("short\nlongest\nmid", "longest"),
            ("one line", "one line"),
            (["a", "bb", "ccc"], "ccc"),
            ("a\nbb\nccc", "ccc"),
        ],
    )
    def test__get_longest_line(self, testbook, cell_val, expected):
        got = testbook.ws._get_longest_line(cell_val)
        assert got == expected

    @pytest.mark.parametrize(
        "cell_val,expected",
        [
            ("abc", "abc"),
            (123, "123"),
            (["a", "b", "c"], "a\nb\nc"),
            ({"x": 1, "y": 2}, "x\ny"),
        ],
    )
    def test__get_cell_string(self, testbook, cell_val, expected):
        # Patch FormatList handling if needed
        got = testbook.ws._get_cell_string(cell_val)
        assert got == expected


class TestGPWorkbookStatic:
    """
    Test that the GPWorkbook static methods work as expected.
    """

    @pytest.mark.parametrize(
        "input, expected",
        [
            ("no references", "no references"),
            ("ref at end$$1$$", "ref at end"),
            ("$$1$$ref at start", "ref at start"),
            ("two$$1$$ refs$$2$$", "two refs"),
            ("three$$1$$ refs$$2$$, wow$$3$$", "three refs, wow"),
        ],
    )
    def test__strip_annotation_references(self, input, expected):
        assert GPWorkbook._strip_annotation_references(input) == expected


class TestGPWorkbook:
    """
    Test that GPWorkbook initialisation and methods work as expected.
    """

    def test_subclass(self):
        """
        Test that the GPWorkbook class is a subclass of the XlsxWriter
        Workbook class.
        """
        assert issubclass(GPWorkbook, xlsxwriter.Workbook)

    def test_default_theme_set(self, testbook):
        """
        Test that the workbook theme is set to gptheme by default.
        """
        assert testbook.wb.theme == gptheme

    def test_valid_set_theme(self, testbook):
        """
        Test that setting a new theme with a Theme object works as expected.
        Essentially, make sure that gptheme is not used.
        """
        theme_config = {"title": {"bold": True}}
        theme = gptables.Theme(theme_config)
        testbook.wb.set_theme(theme)

        assert testbook.wb.theme == gptables.Theme(theme_config)

    @pytest.mark.parametrize(
        "not_a_theme", [dict(), set(), [], 1, 3.14, "test_string", pd.DataFrame()]
    )
    def test_invalid_set_theme(self, not_a_theme, testbook):
        """
        Test that setting theme with an object that is not a gptables.Theme
        raises a TypeError.
        """
        with pytest.raises(TypeError):
            testbook.wb.set_theme(not_a_theme)

    def test__update_annotations(self, testbook, create_gptable_with_kwargs):
        """
        Test that _update_annotations produces a correctly ordered list of
        note references used in sheets.
        """
        table = pd.DataFrame(columns=["col"])

        kwargs1 = {
            "title": "Title$$1$$",
            "subtitles": ["Subtitle$$2$$"],
            "units": {0: "Unit$$3$$"},
            "table_notes": {0: "Note$$4$$"},
            "table": table,
        }

        kwargs2 = {
            "title": "Title$$1$$",
            "subtitles": ["Subtitle$$3$$"],
            "units": {0: "Unit$$5$$"},
            "table_notes": {0: "Note$4$$"},
            "table": table,
        }

        gptable1 = create_gptable_with_kwargs(kwargs1)
        gptable2 = create_gptable_with_kwargs(kwargs2)
        sheets = {"sheet1": gptable1, "sheet2": gptable2}

        gpworkbook = testbook.wb
        gpworkbook._update_annotations(sheets)

        assert gpworkbook._annotations == ["1", "2", "3", "4", "5"]

    @pytest.mark.parametrize(
        "additional_elements,values",
        [
            (None, None),
            (["scope"], ["scope"]),
            (
                ["subtitles", "instructions", "scope", "source"],
                [["subtitles"], "instructions", "scope", "source"],
            ),
        ],
    )
    def test_make_table_of_contents(
        self, testbook, create_gptable_with_kwargs, additional_elements, values
    ):
        """
        Test that attributes are set as expected when contentsheet is created.
        """
        kwargs = {}
        if additional_elements:
            kwargs.update(dict(zip(additional_elements, values)))

        exp_toc = pd.DataFrame(
            {
                "Sheet name": [{"sheet": "internal:'sheet'!A1"}],
                "Table description": [["Sheet title", *kwargs.keys()]],
            }
        )
        exp_contentsheet = create_gptable_with_kwargs(
            {
                "table_name": "contents_table",
                "title": "Table of contents",
                "instructions": "This worksheet contains one table.",
                "table": exp_toc,
                "index_columns": {2: 0},
            }
        )

        got_contentsheet = testbook.wb.make_table_of_contents(
            sheets={
                "sheet": create_gptable_with_kwargs({"title": "Sheet title", **kwargs})
            },
            additional_elements=list(kwargs.keys()),
        )

        assert_frame_equal(got_contentsheet.table, exp_contentsheet.table)

        got_contentsheet.table = None
        exp_contentsheet.table = None

        assert got_contentsheet.__dict__ == exp_contentsheet.__dict__

    def test_make_notesheet(self, testbook, create_gptable_with_kwargs):
        """
        Test that creating a notes table sheet using `make_notesheet` generates
        the same gptables.GPTable object as expected.
        """
        gpworkbook = testbook.wb
        gpworkbook._annotations = [1, 2]
        dummy_table = pd.DataFrame(
            data={"Note number": [1, 2], "Note text": ["text", "more text"]}
        )

        notes_name = "Just_a_notesheet"
        notes_title = "Are these the notes you're looking for?"
        notes_instructions = "These are not the notes you're looking for"

        got_notesheet = gpworkbook.make_notesheet(
            notes_table=dummy_table,
            table_name=notes_name,
            title=notes_title,
            instructions=notes_instructions,
        )
        exp_notesheet = create_gptable_with_kwargs(
            {
                "table": dummy_table,
                "table_name": notes_name,
                "title": notes_title,
                "instructions": notes_instructions,
            }
        )

        assert_frame_equal(got_notesheet.table, exp_notesheet.table)

        got_notesheet.table = None
        exp_notesheet.table = None

        assert got_notesheet.__dict__ == exp_notesheet.__dict__

    def test_notesheet_defaults(self, testbook, create_gptable_with_kwargs):
        """
        Test that creating a notes table sheet with arguments set to defaults generates
        the same gptables.GPTable object as expected.
        """
        gpworkbook = testbook.wb
        gpworkbook._annotations = [1, 2]
        dummy_table = pd.DataFrame(
            data={"Note number": [1, 2], "Note text": ["text", "more text"]}
        )

        notes_name = "notes_table"
        notes_title = "Notes"
        notes_instructions = "This worksheet contains one table."

        got_notesheet = gpworkbook.make_notesheet(notes_table=dummy_table)
        exp_notesheet = create_gptable_with_kwargs(
            {
                "table": dummy_table,
                "table_name": notes_name,
                "title": notes_title,
                "instructions": notes_instructions,
            }
        )

        assert_frame_equal(got_notesheet.table, exp_notesheet.table)

        got_notesheet.table = None
        exp_notesheet.table = None

        assert got_notesheet.__dict__ == exp_notesheet.__dict__
