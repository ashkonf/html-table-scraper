"""Utilities for converting HTML tables into :class:`pandas.DataFrame` objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import pandas as pd
from bs4 import BeautifulSoup, Tag


def _deep_copy(soup: Tag) -> BeautifulSoup:
    """Return a deep copy of a BeautifulSoup tag."""

    return BeautifulSoup(str(soup), "html.parser")


def _get_text(element: Tag | str | None) -> str:
    """Extract visible text from an element, preserving line breaks."""

    if element is None:
        return ""
    if isinstance(element, str):
        return element
    element = _deep_copy(element)
    for br in element.find_all("br"):
        br.replace_with("\n")
    return element.get_text()


@dataclass
class TableCell:
    """Representation of a single HTML table cell.

    The class stores the visible text of the cell as well as any hyperlinks
    and superscript elements that were present. This makes it easier to
    perform more sophisticated analyses on the cell contents without losing
    potentially useful metadata (for example, Wikipedia footnotes or links to
    related pages).
    """

    text: str = ""
    links: List[Dict[str, str]] = field(default_factory=list)
    sups: List[str] = field(default_factory=list)

    @classmethod
    def from_soup(cls, soup: Optional[Tag]) -> "TableCell":
        """Construct a :class:`TableCell` from a BeautifulSoup element."""

        if soup is None:
            return cls()

        soup_copy = _deep_copy(soup)

        # Capture hyperlinks before stripping tags.
        links: List[Dict[str, str]] = []
        for a in soup_copy.find_all("a"):
            links.append({"href": a.get("href"), "text": _get_text(a)})

        # Extract and store superscripts (often footnote markers on pages like
        # Wikipedia).  Remove them from the copy so that they do not appear in
        # the plain text.
        sups: List[str] = []
        for sup in soup_copy.find_all("sup"):
            sups.append(_get_text(sup))
            sup.extract()

        text = _parse_cell(soup_copy) if soup_copy else ""

        return cls(text=text, links=links, sups=sups)

    def to_df(self) -> pd.DataFrame:
        """Convert the cell into a one-row :class:`pandas.DataFrame`.

        This provides an easy bridge for downstream code that expects a
        dataframe representation of the cell's contents.
        """

        return pd.DataFrame(
            [
                {"text": self.text, "links": self.links, "sups": self.sups},
            ]
        )


class Table(pd.DataFrame):
    """DataFrame subclass with an optional title for display."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Create a ``Table`` optionally including a title."""

        title = kwargs.get("title", None)
        if "title" in kwargs:
            del kwargs["title"]
        super(Table, self).__init__(*args, **kwargs)
        self.title: Optional[str] = title

    def pretty_print(self) -> None:
        """Display the table using IPython rich HTML."""

        if self.title is not None:
            print(self.title)
        try:
            from IPython.display import HTML, display
        except ImportError as exc:  # pragma: no cover - depends on IPython
            raise ImportError("IPython is required for pretty_print()") from exc

        display(HTML(self.to_html()))


def _parse_element(soup: Optional[Tag]) -> Optional[str]:
    """Parse a single HTML element, removing hidden spans and superscripts."""

    if soup is None:
        return None

    soup = _deep_copy(soup)

    for span in soup.find_all("span"):
        if (
            span is not None
            and "style" in span.attrs
            and "display:none" in span["style"].lower()
        ):
            span.extract()

    sups = soup.find_all("sup")
    [sup.extract() for sup in sups]

    return _get_text(soup).strip()


def _parse_cell(soup: Optional[Tag]) -> str:
    """Parse an individual table cell into plain text."""

    parsed = _parse_element(soup) or ""
    return parsed.replace("\n", " ")


def _parse_row(soup: Tag) -> List[str]:
    """Parse a table row into a list of cell strings."""
    return [_parse_cell(cell) for cell in soup.find_all(["th", "td"], recursive=False)]


def parse_table(
    table: Optional[Tag],
    first_row_as_col_titles: bool = True,
    ignore_first_row: bool = False,
) -> Table:
    """Convert an HTML ``<table>`` tag into a :class:`Table`.

    Args:
        table: BeautifulSoup ``<table>`` tag to convert.
        first_row_as_col_titles: Whether to use the first row as column names.
        ignore_first_row: Whether to skip the first row entirely.

    Returns:
        Parsed ``Table`` instance containing the data.
    """

    if table is not None:
        rows: List[Tag] = []
        for child in table.find_all(["tr", "thead", "tbody", "tfoot"], recursive=False):
            if child.name == "tr":
                rows.append(child)
            else:
                rows.extend(child.find_all("tr", recursive=False))

        if ignore_first_row:
            rows = rows[1:]

        if len(rows) > 0:
            row_lists: List[List[str]] = []
            if first_row_as_col_titles:
                columns = _parse_row(rows[0])
                for row in rows[1:]:
                    row_lists.append(_parse_row(row))
            else:
                columns: List[str] = []
                for row in rows:
                    row_lists.append(_parse_row(row))

            max_len = max(len(row) for row in [columns] + row_lists)

            def normalize_length(row_list: List[str]) -> List[str]:
                return row_list + [""] * (max_len - len(row_list))

            columns = normalize_length(columns)
            for index, row_list in enumerate(row_lists):
                row_lists[index] = normalize_length(row_list)

            if columns:
                return Table(row_lists, columns=columns)
            return Table(row_lists)

    return Table()
