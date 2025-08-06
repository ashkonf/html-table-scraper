from typing import List, Optional, Union

from bs4 import BeautifulSoup, Tag
import pandas as pd
import IPython.display

def _deep_copy(soup: Tag) -> BeautifulSoup:
    return BeautifulSoup(str(soup), "lxml")


def _get_text(element: Union[str, Tag]) -> str:
    if isinstance(element, str):
        return element
    element = _deep_copy(element)
    for br in element.find_all("br"):
        br.replace_with("\n")
    return element.get_text() if element is not None else ""


class Table(pd.DataFrame):

    def __init__(self, *args, title: Optional[str] = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = title

    def pretty_print(self) -> None:
        if self.title is not None:
            print(self.title)
        IPython.display.display(IPython.display.HTML(self.to_html()))


def _parse_element(soup: Optional[Tag]) -> Optional[str]:
    if soup is None:
        return None
    soup = _deep_copy(soup)
    for span in soup.find_all("span"):
        if "style" in span.attrs and "display:none" in span["style"].lower():
            span.extract()
    for sup in soup.find_all("sup"):
        sup.extract()
    return _get_text(soup).strip()


def _parse_cell(soup: Tag) -> str:
    parsed = _parse_element(soup)
    return parsed.replace("\n", " ") if parsed else ""


def _parse_row(soup: Tag) -> List[str]:
    return [_parse_cell(cell) for cell in soup.find_all(["th", "td"])]


def parse_table(
    table: Optional[Tag],
    first_row_as_col_titles: bool = True,
    ignore_first_row: bool = False,
) -> Table:
    if table is not None:
        rows = table.find_all("tr")
        if ignore_first_row:
            rows = rows[1:]

        if rows:
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
