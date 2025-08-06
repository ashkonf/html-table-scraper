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

    # TODO: get links, sups, etc.
    # TODO: have a to_df method (or just make it a super class of df so that it's that by default)
    
    def __init__(self):
        pass
        
    @classmethod
    def from_soup(cls, soup):
        sups = soup.find_all("sup")
        
        [sup.extract() for sup in sups]

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
