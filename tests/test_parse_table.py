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


def test_parse_table_ignore_first_row():
    html = """
    <table>
        <tr><td>skip</td><td>me</td></tr>
        <tr><th>X</th><th>Y</th></tr>
        <tr><td>1</td><td>2</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag, ignore_first_row=True)

    expected = pd.DataFrame([["1", "2"]], columns=["X", "Y"])
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_handles_extra_cells():
    html = """
    <table>
        <tr><th>A</th><th>B</th></tr>
        <tr><td>1</td><td>2</td><td>3</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag)

    expected = pd.DataFrame([["1", "2", "3"]], columns=["A", "B", ""])
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_empty_input():
    result_none = parse_table(None)
    assert result_none.empty

    html = "<table></table>"
    soup = BeautifulSoup(html, "lxml")
    result_empty = parse_table(soup.find("table"))
    assert result_empty.empty

def test_parse_table_br_tags():
    html = """
    <table>
        <tr><th>A</th></tr>
        <tr><td>line1<br/>line2</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag)

    expected = pd.DataFrame([["line1 line2"]], columns=["A"])
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_html_entities():
    html = """
    <table>
        <tr><th>Name</th></tr>
        <tr><td>Tom &amp; Jerry</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag)

    expected = pd.DataFrame([["Tom & Jerry"]], columns=["Name"])
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_th_in_data_rows():
    html = """
    <table>
        <tr><th>A</th><th>B</th></tr>
        <tr><th>1</th><td>2</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag)

    expected = pd.DataFrame([["1", "2"]], columns=["A", "B"])
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_ignore_first_row_without_header():
    html = """
    <table>
        <tr><td>a</td><td>b</td></tr>
        <tr><td>c</td><td>d</td></tr>
        <tr><td>e</td><td>f</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag, first_row_as_col_titles=False, ignore_first_row=True)

    expected = pd.DataFrame([["c", "d"], ["e", "f"]], columns=["", ""])
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_handles_thead_tbody():
    html = """
    <table>
        <thead>
            <tr><th>Col</th></tr>
        </thead>
        <tbody>
            <tr><td>val</td></tr>
        </tbody>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag)

    expected = pd.DataFrame([["val"]], columns=["Col"])
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_header_only():
    html = """
    <table>
        <tr><th>A</th><th>B</th></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag)

    expected = pd.DataFrame(columns=["A", "B"])
    pd.testing.assert_frame_equal(result, expected)


def test_parse_table_nested_tags():
    html = """
    <table>
        <tr><th>Text</th></tr>
        <tr><td><div><b>Bold</b> and <i>italic</i></div></td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "lxml")
    table_tag = soup.find("table")

    result = parse_table(table_tag)

    expected = pd.DataFrame([["Bold and italic"]], columns=["Text"])
    pd.testing.assert_frame_equal(result, expected)

