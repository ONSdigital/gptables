# Cover

Cover sheets can be used to provide information that is general to all tables in a Workbook.

#### NOTE
Cover sheets are added as the first sheet in the Worbook when written by `gptables`.
This is important when applying additional formatting to other Worksheets by their index in the Workbook.

## Mapping

To include a cover sheet, map your text elements to the attributes of a `Cover` object and pass this object to the `cover` parameter of either [`produce_workbook()`](doc.api.md#gptables.core.api.produce_workbook) or [`write_workbook()`](doc.api.md#gptables.core.api.write_workbook).
Text attributes which take a list (most except for title) will write one element per cell vertically in the Worksheet.

## Formatting

Formatting of cover sheet text is managed by the `cover_` attributes of the Workbook’s [`Theme`](doc.theme.md#gptables.core.theme.Theme).

## `Cover` Class

### *class* gptables.core.cover.Cover(title: str, intro: List = None, about: List = None, contact: List = None, cover_label: str = 'Cover', width: int = 85)

dataclass for storing cover sheet text.

#### title

cover page title

* **Type:**
  str

#### intro

introductory text

* **Type:**
  List[str, list], optional

#### about

about/notes text

* **Type:**
  List[str, list], optional

#### contact

contact details text

* **Type:**
  List[str, list], optional

#### cover_label

cover page tab label, defaults to Cover

* **Type:**
  str

#### width

width of the column, defaults to 85

* **Type:**
  int
