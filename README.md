# HtmlTableScraping

A tiny utility that converts HTML `<table>` elements into pandas `DataFrame` objects. It removes superscripts and hidden spans and returns a convenient `Table` subclass for pretty-printing.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
  - [Dependencies](#dependencies)
- [Usage](#usage)
  - [Example](#example)
- [Limitations](#limitations)
- [License](#license)

## Features

- Convert HTML tables into pandas DataFrames.
- Strips superscript footnotes and elements hidden with CSS.
- Provides a `Table` class with an optional `pretty_print` helper.

## Installation

### Dependencies

This project relies on:

- beautifulsoup4
- pandas
- ipython
- ipython-genutils

Install them with `pip`:

```bash
pip install -r requirements.txt
```

Simply include `scraper.py` in your project after installing the dependencies.

## Usage

The module exposes one public function, `parse_table(table)`, where `table` is a BeautifulSoup `table` tag. It returns a `Table` (a subclass of `pandas.DataFrame`) containing the parsed data.

### Example

```python
from bs4 import BeautifulSoup
from scraper import parse_table

html = '''
<table>
    <tr><th>Year</th><th>Change</th></tr>
    <tr><td>1970</td><td>0.10%</td></tr>
    <tr><td>1971</td><td>10.79%</td></tr>
</table>
'''
soup = BeautifulSoup(html, "lxml")
table = soup.find("table")
print(parse_table(table))
```

_Output:_

```
   Year Change
0  1970  0.10%
1  1971 10.79%
```

## Limitations

`parse_table` currently does not handle `rowspan` or `colspan` attributes. Tables using these features may not be parsed correctly.

## License

HtmlTableScraping is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
