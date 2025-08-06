from bs4 import BeautifulSoup
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from scraper import parse_table


def test_parse_table_basic():
    html = """
    <table>
        <tr><th>Name</th><th>Age</th></tr>
        <tr><td>Alice</td><td>30</td></tr>
        <tr><td>Bob</td><td>40</td></tr>
    </table>
    """
    table_tag = BeautifulSoup(html, "lxml").table
    df = parse_table(table_tag)
    assert list(df.columns) == ["Name", "Age"]
    assert df.iloc[0].tolist() == ["Alice", "30"]
    assert df.iloc[1].tolist() == ["Bob", "40"]


def test_parse_table_ignore_first_row():
    html = """
    <table>
        <tr><td>ignore</td><td>row</td></tr>
        <tr><th>A</th><th>B</th></tr>
        <tr><td>C</td><td>D</td></tr>
    </table>
    """
    table_tag = BeautifulSoup(html, "lxml").table
    df = parse_table(table_tag, ignore_first_row=True)
    assert list(df.columns) == ["A", "B"]
    assert df.iloc[0].tolist() == ["C", "D"]


def test_parse_table_no_header():
    html = """
    <table>
        <tr><td>A</td><td>B</td></tr>
        <tr><td>C</td><td>D</td></tr>
    </table>
    """
    table_tag = BeautifulSoup(html, "lxml").table
    df = parse_table(table_tag, first_row_as_col_titles=False)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["", ""]
    assert df.iloc[0].tolist() == ["A", "B"]


def test_parse_table_strips_hidden_and_sup_and_br():
    html = """
    <table>
        <tr><th>Col</th></tr>
        <tr><td>Visible<span style="display:none">hidden</span><sup>1</sup>line<br/>break</td></tr>
    </table>
    """
    table_tag = BeautifulSoup(html, "lxml").table
    df = parse_table(table_tag)
    cell = df.iloc[0, 0]
    assert cell == "Visibleline break"
    assert "hidden" not in cell and "1" not in cell
