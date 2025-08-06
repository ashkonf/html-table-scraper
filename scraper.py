from bs4 import BeautifulSoup
import pandas as pd
import IPython.display

def _deep_copy(soup):
    return BeautifulSoup(str(soup), "lxml")

def _get_text(element):
    if isinstance(element, str):
        return element
    else:
        element = _deep_copy(element)
        for br in element.find_all("br"):
            br.replace_with("\n")
        if element is not None: 
            return element.get_text()
        else: 
            return ""
    
class TableCell(object):
    """Representation of a single HTML table cell.

    The class stores the visible text of the cell as well as any hyperlinks
    and superscript elements that were present.  This makes it easier to
    perform more sophisticated analyses on the cell contents without losing
    potentially useful metadata (for example, Wikipedia footnotes or links to
    related pages).
    """

    def __init__(self, text="", links=None, sups=None):
        self.text = text
        self.links = links or []
        self.sups = sups or []

    @classmethod
    def from_soup(cls, soup):
        """Construct a :class:`TableCell` from a BeautifulSoup element."""
        if soup is None:
            return cls()

        soup_copy = _deep_copy(soup)

        # Capture hyperlinks before stripping tags.
        links = []
        for a in soup_copy.find_all("a"):
            links.append({
                "href": a.get("href"),
                "text": _get_text(a)
            })

        # Extract and store superscripts (often footnote markers on pages like
        # Wikipedia).  Remove them from the copy so that they do not appear in
        # the plain text.
        sups = []
        for sup in soup_copy.find_all("sup"):
            sups.append(_get_text(sup))
            sup.extract()

        text = _parse_cell(soup_copy) if soup_copy else ""

        return cls(text=text, links=links, sups=sups)

    def to_df(self):
        """Convert the cell into a one-row :class:`pandas.DataFrame`.

        This provides an easy bridge for downstream code that expects a
        dataframe representation of the cell's contents.
        """
        return pd.DataFrame([
            {
                "text": self.text,
                "links": self.links,
                "sups": self.sups,
            }
        ])

class Table(pd.DataFrame):
    
    def __init__(self, *args, **kwargs):
        title = kwargs.get("title", None)
        if "title" in kwargs:
            del kwargs["title"]
        super(Table, self).__init__(*args, **kwargs)
        self.title = title
        
    def pretty_print(self):
        if self.title is not None:
            print(self.title)
        IPython.display.display(IPython.display.HTML(self.to_html()))

def _parse_element(soup):
    if soup is None:
        return None
    
    else:
        soup = _deep_copy(soup)
        
        for span in soup.find_all("span"):
            if span is not None and "style" in span.attrs and "display:none" in span["style"].lower():
                span.extract()
        
        sups = soup.find_all("sup")
        [sup.extract() for sup in sups]
        
        return _get_text(soup).strip()

def _parse_cell(soup):
    return _parse_element(soup).replace("\n", " ")

def _parse_row(soup):
    return [_parse_cell(cell) for cell in soup.find_all(["th", "td"])]

def parse_table(table, first_row_as_col_titles=True, ignore_first_row=False):
    if table is not None:
        rows = table.find_all("tr")
        if ignore_first_row:
            rows = rows[1:]
        
        if len(rows) > 0:
            row_lists =[]
            if first_row_as_col_titles:
                columns = _parse_row(rows[0])
                for row in rows[1:]:
                    row_lists.append(_parse_row(row))
            else:
                columns = []
                for row in rows:
                    row_lists.append(_parse_row(row))
                
            max_len = max(len(row) for row in [columns] + row_lists)
            normalize_length = lambda row_list: row_list + [""] * (max_len - len(row_list))
            columns = normalize_length(columns)
            for index, row_list in enumerate(row_lists):
                row_lists[index] = normalize_length(row_list)
                
            if columns:
                return Table(row_lists, columns=columns)
            else:
                return Table(row_lists)
            
    return Table()
