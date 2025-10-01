# Theme

## `Theme` Configuration

The easiest way to design your own theme is to create a
YAML configuration file. You should take a copy of our default theme
configuration file and adjust it to suit your needs.
When designing a theme, please consult the [Analysis Function guidance](https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/) to
ensure your new formatting is accessible.

Most of the top level names in the config file represent table elements or their metadata.
The parameters passed below these names are [XlsxWriter format properties](https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties), so you
should check out their documentation to find the appropriate properties and valid
options for your formatting.

`global` refers to the base format that all others will be built upon.
Any format parameter that is repeated for a specific element will override the global format for that element.
The three `cover_` format names refer to elements of the cover page generated from a [`Cover`](doc.cover.md#gptables.core.cover.Cover).

#### NOTE
All top levels names must exist in the config file. Where no properties need to be passed, leave empty after the colon.

The final name in the config file is a special attribute which doed not take
XlsxWriter properties. It does the following:

* `description_order` - specify the order of description elements.
  Must contain a list including `instructions`, `legend`, `source` and `scope`,
  in the order that you would like them to appear.

The configuration file for our default theme looks like this:

```yaml
global:
    font_size: 12
    font_name: Arial
    font_color: 'automatic'

cover_title:
    bold: True
    font_size: 16
    text_wrap: True

cover_subtitle:
    bold: True
    font_size: 14
    text_wrap: True

cover_text:
    text_wrap: True

title:
    bold: True
    font_size: 16

subtitle:
    font_size: 14

instructions:

scope:

column_heading:
    bold: True
    bottom: 1
    text_wrap: 1
    valign: top

index_1:
    bold: True
    text_wrap: 1

index_2:
    text_wrap: 1

index_3:
    text_wrap: 1

data:
    text_wrap: 1

source:
    font_size: 12

legend:
    font_size: 12

description_order:
    - instructions
    - legend
    - source
    - scope
```

For minor adjustments to a theme, a deepcopy can be taken before using the
`Theme` methods below to update the `Theme`’s attributes.

`Theme` objects can altenatively be configured using dictionaries, with the same
structure as the configuration files.

An example using a personalised theme YAML file can be found under [Example Usage](usage.md#example-usage).

## `Theme` Class

### *class* gptables.core.theme.Theme(config=None)

A class that defines a set of format attributes for use in xlsxwriter.

This class associates a dict of format attributes with table elements.

See XlsxWriter
[format properties](https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties)
for valid options.

#### cover_title_format

* **Type:**
  dict

#### cover_subtitle_format

* **Type:**
  dict

#### cover_text_format

* **Type:**
  dict

#### title_format

* **Type:**
  dict

#### subtitle_format

* **Type:**
  dict

#### instructions_format

* **Type:**
  dict

#### scope_format

* **Type:**
  dict

#### column_heading_format

* **Type:**
  dict

#### index_1_format

* **Type:**
  dict

#### index_2_format

* **Type:**
  dict

#### index_3_format

* **Type:**
  dict

#### data_format

* **Type:**
  dict

#### source_format

* **Type:**
  dict

#### legend_format

* **Type:**
  dict

#### description_order

* **Type:**
  list

#### apply_config(config)

Update multiple Theme attributes using a YAML or dictionary config.
This enables extension of build in Themes.

#### print_attributes()

Print all current format attributes and values to the console.

#### update_column_heading_format(format_dict)

Update the column_heading_format attribute. Where keys already exist,
existing items are replaced.

#### update_cover_subtitle_format(format_dict)

Update the cover_subtitle_format attribute. Where keys already exist, existing
items are replaced.

#### update_cover_text_format(format_dict)

Update the cover_text_format attribute. Where keys already exist, existing
items are replaced.

#### update_cover_title_format(format_dict)

Update the cover_title_format attribute. Where keys already exist, existing
items are replaced.

#### update_data_format(format_dict)

Update the data_format attribute. Where keys already exist,
existing items are replaced.

#### update_description_order(order_list)

Update the description_order attribute. Overrides existing order.

#### update_index_1_format(format_dict)

Update the index_1_format attribute. Where keys already exist, existing
items are replaced.

#### update_index_2_format(format_dict)

Update the index_2_format attribute. Where keys already exist, existing
items are replaced.

#### update_index_3_format(format_dict)

Update the index_3_format attribute. Where keys already exist, existing
items are replaced.

#### update_instructions_format(format_dict)

Update the instructions_format attribute. Where keys already exist,
existing items are replaced.

#### update_legend_format(format_dict)

Update the legend_format attribute. Where keys already exist,
existing items are replaced.

#### update_location_format(format_dict)

Update the location_format attribute. Where keys already exist,
existing items are replaced.

#### update_scope_format(format_dict)

Update the scope_format attribute. Where keys already exist, existing
items are replaced.

#### update_source_format(format_dict)

Update the source_format attribute. Where keys already exist,
existing items are replaced.

#### update_subtitle_format(format_dict)

Update the subtitle_format attribute. Where keys already exist,
existing items are replaced.

#### update_title_format(format_dict)

Update the title_format attribute. Where keys already exist, existing
items are replaced.
