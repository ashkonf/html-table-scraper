import os
import sys

import pandas as pd
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scraper import parse_table, Table


def test_parse_table_basic():
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


def test_parse_table_removes_hidden_and_sups_and_normalizes():
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

    expected = pd.DataFrame([
        ["row1col1", "visible line", ""],
        ["a", "b", "c"],
    ], columns=["Col1", "Col2", "Col3"])
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_without_header():
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
