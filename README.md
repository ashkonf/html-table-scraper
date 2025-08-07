# html-table-scraper

A simple module that turns HTML tables into Pandas `DataFrame` objects.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
  - [Running tests](#running-tests)
  - [Linting and type checking](#linting-and-type-checking)
- [License](#license)

## Features

- Convert HTML tables into pandas DataFrames.
- Strips superscript footnotes and elements hidden with CSS.
- Provides a `Table` class with an optional `pretty_print` helper.

## Installation

This project relies on:

- beautifulsoup4
- pandas
- ipython
- ipython-genutils

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Install the dependencies with:

```bash
uv sync
```

## Usage

The `html_table_scraper` package exports one public function: `parse_table(table)`. This function accepts a `BeautifulSoup` `Tag` of type `table` and returns a `pandas.DataFrame` containing the table's contents.

The module exposes one public function, `parse_table(table)`, where `table` is a BeautifulSoup `table` tag. It returns a `Table` (a subclass of `pandas.DataFrame`) containing the parsed data.

### Example

```python
from bs4 import BeautifulSoup
from html_table_scraper import parse_table

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

## Development

This project relies on [pre-commit](https://pre-commit.com/) to run code quality checks. After installing dependencies, run all checks with:

```bash
uv run pre-commit run --all-files
```

## Tests

This project includes a small pytest suite in `tests/test_parse_table.py` that validates the table parsing logic for
cases like hidden elements, irregular row lengths, and empty inputs. After installing the dependencies, run the tests with:

```bash
pip install -r requirements.txt
pip install pytest lxml
pytest
```

### Running tests

```bash
uv run pytest
```

### Linting and type checking

```bash
uv run ruff format
uv run ruff check
uv run pyright
```

## License

`HtmlTableScraping` is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Limitations

`parse_table` currently does not handle `rowspan` or `colspan` attributes. Tables using these features may not be parsed correctly.

## License

HtmlTableScraping is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
