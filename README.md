# HtmlTableScraping

A simple module that turns HTML tables into Pandas `DataFrame` objects.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
  - [Running tests](#running-tests)
  - [Linting and type checking](#linting-and-type-checking)
- [License](#license)

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Install the dependencies with:

```bash
uv sync
```

## Usage

The `scraper` module exports one public function: `parse_table(table)`. This function accepts a `BeautifulSoup` `Tag` of type `table` and returns a `pandas.DataFrame` containing the table's contents.

```python
from bs4 import BeautifulSoup
from scraper import parse_table

html = """
<table>
    <tr><th>A</th><th>B</th></tr>
    <tr><td>1</td><td>2</td></tr>
    <tr><td>3</td><td>4</td></tr>
</table>
"""

soup = BeautifulSoup(html, "lxml")
table = soup.find("table")
print(parse_table(table))
```

## Development

This project relies on [pre-commit](https://pre-commit.com/) to run code quality checks. After installing dependencies, run all checks with:

```bash
uv run pre-commit run --all-files
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
