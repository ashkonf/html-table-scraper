# html-table-scraper

A simple, lightweight Python module for scraping HTML tables and converting them into clean, usable `pandas` `DataFrame` objects.

[![PyPI version](https://img.shields.io/pypi/v/your-package)](link-to-pypi-page)
[![codecov](https://codecov.io/github/ashkonf/html-table-scraper/graph/badge.svg?token=7Y596J8IYZ)](https://codecov.io/github/ashkonf/html-table-scraper)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Pytest](https://img.shields.io/badge/pytest-✓-brightgreen)](https://docs.pytest.org)
[![Pyright](https://img.shields.io/badge/pyright-✓-green)](https://github.com/microsoft/pyright)
[![Ruff](https://img.shields.io/badge/ruff-✓-blue?logo=ruff)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Build Status](https://img.shields.io/github/actions/workflow/status/ashkonf/html-table-scraper/ci.yml?branch=main)](https://github.com/ashkonf/html-table-scraper/actions/workflows/ci.yml?query=branch%3Amain)

## Features

- **Simple API**: Convert an HTML table to a `DataFrame` with a single function call.
- **Intelligent Parsing**: Automatically handles `<thead>`, `<tbody>`, and `<th>` tags to structure your data correctly.
- **Cleans Dirty Data**: Strips out unwanted content like superscript footnote markers (e.g., `[1]`, `note 1`) and elements hidden with CSS (`display: none`).
- **Handles Complex Cells**: Normalizes cell content by converting line breaks to spaces and preserving hyperlinks.
- **Flexible**: Choose whether to use the first row as column headers or not.
- **Robust**: Gracefully handles irregular tables, such as those with uneven row lengths or empty cells.
- **Rich Display**: Includes an optional `pretty_print()` method for enhanced table display in Jupyter notebooks.

## Installation

This project is available on PyPI and can be installed with `pip`:

```bash
pip install html-table-scraper
```

This project uses [uv](https://github.com/astral-sh/uv) for development. To install dependencies for local development, run:

```bash
uv sync
```

## Usage

The primary function is `html_table_scraper.parse_table()`. It takes a `BeautifulSoup` `Tag` object representing an HTML `<table>` and returns a `Table` object, which is a subclass of `pandas.DataFrame`.

### Basic Example

```python
from bs4 import BeautifulSoup
from html_table_scraper import parse_table

html = """
<table>
    <tr><th>Year</th><th>Change</th></tr>
    <tr><td>1970</td><td>0.10%</td></tr>
    <tr><td>1971</td><td>10.79%</td></tr>
</table>
"""

soup = BeautifulSoup(html, "lxml")
table = soup.find("table")
df = parse_table(table)

print(df)
```

Output:

```
   Year   Change
0  1970    0.10%
1  1971   10.79%
```

### Handling Complex Content

The parser automatically cleans and normalizes complex cell content, including stripping hidden elements and superscripts.

```python
complex_html = """
<table>
    <tr><th>Country</th><th>Population</th><th>Notes</th></tr>
    <tr>
        <td><a href="/usa">United States</a></td>
        <td>331 million<sup>1</sup></td>
        <td>Data from <span style="display:none">hidden text</span>2020 census</td>
    </tr>
    <tr>
        <td><a href="/china">China</a></td>
        <td>1.4 billion<sup>2</sup></td>
        <td>Estimated<br/>population</td>
    </tr>
</table>
"""

soup = BeautifulSoup(complex_html, "lxml")
table = soup.find("table")
df = parse_table(table)

print(df)
```

Output:

```
         Country    Population                       Notes
0  United States   331 million  Data from 2020 census
1          China  1.4 billion   Estimated population
```

### Tables Without Headers

If your table lacks a header row (`<th>`), you can instruct the parser not to treat the first row as column titles.

```python
no_header_html = """
<table>
    <tr><td>Apple</td><td>Red</td><td>Sweet</td></tr>
    <tr><td>Banana</td><td>Yellow</td><td>Sweet</td></tr>
</table>
"""

soup = BeautifulSoup(no_header_html, "lxml")
table = soup.find("table")
df = parse_table(table, first_row_as_col_titles=False)

print(df)
```

Output:

```
        0       1      2
0   Apple     Red  Sweet
1  Banana  Yellow  Sweet
```

### Rich Display in Notebooks

The returned `Table` object includes a `pretty_print()` method for a clean, titled display in Jupyter environments.

```python
df = parse_table(soup.find("table"))
df.title = "My Awesome Table"
df.pretty_print()
```

## Development

This project uses `pre-commit` to maintain code quality. To run all checks:

```bash
uv run pre-commit run --all-files
```

### Running Tests

Tests are written with `pytest`. To run the test suite:

```bash
uv run pytest
```

### Linting and Type Checking

The project uses `Ruff` for linting and formatting, and `Pyright` for type checking.

```bash
# Format code
uv run ruff format

# Run linter
uv run ruff check

# Run type checker
uv run pyright
```

## Limitations

Currently, the parser does not support tables with `rowspan` or `colspan` attributes. These attributes will be ignored, which may result in misaligned data for complex tables.

## License

`html-table-scraper` is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
