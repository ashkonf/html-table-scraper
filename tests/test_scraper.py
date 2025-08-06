"""Tests for the :mod:`scraper` module."""

from __future__ import annotations

import IPython.display
import pandas as pd
from bs4 import BeautifulSoup

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper import (
    Table,
    TableCell,
    _deep_copy,
    _get_text,
    _parse_cell,
    _parse_element,
    _parse_row,
    parse_table,
)


def test_deep_copy() -> None:
    """Ensure that a deep copy does not affect the original element."""

    soup = BeautifulSoup("<p>hello</p>", "lxml")
    copy = _deep_copy(soup.p)
    soup.p.string.replace_with("changed")
    assert _get_text(copy) == "hello"
    assert _get_text(soup.p) == "changed"


def test_get_text_with_br() -> None:
    """``_get_text`` should preserve line breaks."""

    soup = BeautifulSoup("<td>first<br/>second</td>", "lxml")
    assert _get_text(soup.td) == "first\nsecond"
    assert _get_text("plain") == "plain"
    assert _get_text(None) == ""


def test_tablecell_from_soup_and_to_df() -> None:
    """``TableCell`` should capture links and superscripts."""

    html = '<td><a href="/a">link</a>text<sup>1</sup></td>'
    soup = BeautifulSoup(html, "lxml")
    cell = TableCell.from_soup(soup.td)
    assert cell.text == "linktext"
    assert cell.links == [{"href": "/a", "text": "link"}]
    assert cell.sups == ["1"]
    df = cell.to_df()
    assert list(df.columns) == ["text", "links", "sups"]
    assert df.iloc[0]["text"] == "linktext"

    empty = TableCell.from_soup(None)
    assert empty.text == "" and not empty.links and not empty.sups


def test_parse_element_and_cell() -> None:
    """Hidden spans and superscripts are ignored in parsed text."""

    html = '<td><span style="display:none">hide</span>ok<sup>1</sup><br/>line</td>'
    soup = BeautifulSoup(html, "lxml")
    element_text = _parse_element(soup.td)
    assert element_text == "ok\nline"
    assert _parse_cell(soup.td) == "ok line"
    assert _parse_element(None) is None


def test_parse_row() -> None:
    """``_parse_row`` returns the text of each cell."""

    soup = BeautifulSoup("<tr><td>a</td><th>b</th></tr>", "lxml")
    assert _parse_row(soup.tr) == ["a", "b"]


def test_parse_table_basic() -> None:
    """Parse a simple table with column headers."""

    html = """
    <table>
        <tr><th>A</th><th>B</th></tr>
        <tr><td>1</td><td>2</td></tr>
        <tr><td>3</td><td>4</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag)
    expected = pd.DataFrame([["1", "2"], ["3", "4"]], columns=["A", "B"])
    assert isinstance(result, Table)
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_removes_hidden_and_sups_and_normalizes() -> None:
    """Extra span and sup tags should be removed and rows normalized."""

    html = """
    <table>
        <tr><th>Col1</th><th>Col2</th><th>Col3</th></tr>
        <tr>
            <td>row1col1</td>
            <td><span style="display:none">hide</span>visible<sup>1</sup><br/>line</td>
        </tr>
        <tr><td>a</td><td>b</td><td>c</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag)
    expected = pd.DataFrame(
        [["row1col1", "visible line", ""], ["a", "b", "c"]],
        columns=["Col1", "Col2", "Col3"],
    )
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_without_header() -> None:
    """Tables without headers should still parse correctly."""

    html = """
    <table>
        <tr><td>A</td><td>B</td></tr>
        <tr><td>1</td><td>2</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag, first_row_as_col_titles=False)
    expected = pd.DataFrame([["A", "B"], ["1", "2"]], columns=["", ""])
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_ignore_first_row() -> None:
    """Ignoring the first row skips it from the result."""

    html = """
    <table>
        <tr><th>A</th><th>B</th></tr>
        <tr><td>1</td><td>2</td></tr>
        <tr><td>3</td><td>4</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag, ignore_first_row=True)
    expected = pd.DataFrame([["3", "4"]], columns=["1", "2"])
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_empty_and_none() -> None:
    """Empty tables and ``None`` return empty ``Table`` objects."""

    empty_html = "<table></table>"
    soup = BeautifulSoup(empty_html, "lxml")
    pd.testing.assert_frame_equal(parse_table(soup.find("table")), Table())
    pd.testing.assert_frame_equal(parse_table(None), Table())


def test_parse_table_empty_header_rows() -> None:
    """Tables with empty header rows return data without columns."""

    html = """
    <table>
        <tr></tr>
        <tr></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")
    result = parse_table(table_tag)
    assert list(result.columns) == []
    assert len(result) == 1


def test_table_pretty_print(monkeypatch, capsys) -> None:
    """``Table.pretty_print`` prints a title and displays HTML."""

    displayed: list[str] = []

    def fake_display(html: object) -> None:
        displayed.append(str(html))

    monkeypatch.setattr(IPython.display, "display", fake_display)
    table = Table([["1"]], columns=["A"], title="Title")
    table.pretty_print()
    captured = capsys.readouterr()
    assert "Title" in captured.out
    assert displayed, "display should be called"
