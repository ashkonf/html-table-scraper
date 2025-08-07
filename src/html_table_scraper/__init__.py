"""Convenient imports for HTML table scraping utilities."""

from .table import (
    Table,
    TableCell,
    _deep_copy,
    _get_text,
    _parse_cell,
    _parse_element,
    _parse_row,
    parse_table,
)

__all__ = [
    "Table",
    "TableCell",
    "parse_table",
    "_parse_element",
    "_parse_cell",
    "_parse_row",
    "_deep_copy",
    "_get_text",
]
