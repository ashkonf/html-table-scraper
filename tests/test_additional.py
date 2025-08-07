"""Additional test cases for html_table_scraper utilities."""

import pandas as pd
from bs4 import BeautifulSoup

from html_table_scraper import TableCell, _parse_element, parse_table


def test_parse_element_hidden_span_case_insensitive() -> None:
    """Spans hidden with case-insensitive style should be removed."""

    soup = BeautifulSoup(
        '<td><span style="DISPLAY:none">hide</span>visible</td>', "lxml"
    )
    assert _parse_element(soup.td) == "visible"


def test_tablecell_multiple_links_and_sups() -> None:
    """``TableCell`` captures multiple links and superscripts."""

    html = '<td>t<a href="/a">A</a><a href="/b">B</a><sup>1</sup><sup>2</sup></td>'
    soup = BeautifulSoup(html, "lxml")
    cell = TableCell.from_soup(soup.td)

    assert cell.text == "tAB"
    assert cell.links == [
        {"href": "/a", "text": "A"},
        {"href": "/b", "text": "B"},
    ]
    assert cell.sups == ["1", "2"]

    df = cell.to_df()
    assert df.iloc[0]["links"] == [
        {"href": "/a", "text": "A"},
        {"href": "/b", "text": "B"},
    ]


def test_parse_table_multiple_tbody_sections() -> None:
    """Tables with multiple ``<tbody>`` sections are parsed correctly."""

    html = """
    <table>
        <tbody>
            <tr><th>A</th><th>B</th></tr>
        </tbody>
        <tbody>
            <tr><td>1</td><td>2</td></tr>
            <tr><td>3</td><td>4</td></tr>
        </tbody>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    result = parse_table(soup.find("table"))

    expected = pd.DataFrame([["1", "2"], ["3", "4"]], columns=["A", "B"])
    pd.testing.assert_frame_equal(result, expected)
