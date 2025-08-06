# HtmlTableScraping
A simple module that turns HTML tables into Pandas `DataFrames`.
## Contents
  - [Setup](#Setup)
  - [License](#license)
  - [Usage](#Usage)

## Setup

### Installation

Simply include the `scraper.py` file in your project and use away! Just make sure to install its dependencies first, as described below.

### Dependencies

This library relies on the following Python libraries:
 - bs4
 - pandas
 - ipython
 - ipython-genutils
These dependencies are defined in `pyproject.toml` and can be installed with [uv](https://github.com/astral-sh/uv):

```bash
uv sync
```

## License

`HtmlTableScraping` is licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Usage

The `scraper` module exports one public function: `parse_table(table)`. This function accepts a single `table` argument as input, which should be a `BeautifulSoup` `Tag` of type `table`. It sill return a `Pandas` `DataFrame` containing the table's contents.
### Example Usage

```
>>> import requests
>>> from bs4 import BeautifulSoup
>>> from scraper import parse_table

>>> html = requests.get("https://en.wikipedia.org/wiki/S%26P_500").text
>>> soup = BeautifulSoup(html, "lxml")
>>> table = soup.find_all("table")[1]
>>> parse_table(table)

      Year  Change in Index  Total Annual Return Including Dividends  ...  15 Year Annualized Return  20 Year Annualized Return  25 Year Annualized Return
0     1970            0.10%                                    4.01%  ...                          -                          -                          -
1     1971           10.79%                                   14.31%  ...                          -                          -                          -
2     1972           15.63%                                   18.98%  ...                          -                          -                          -
3     1973          −17.37%                                  −14.66%  ...                          -                          -                          -
4     1974          −29.72%                                  −26.47%  ...                          -                          -                          -
5     1975           31.55%                                   37.20%  ...                          -                          -                          -
6     1976           19.15%                                   23.84%  ...                          -                          -                          -
7     1977          −11.50%                                   −7.18%  ...                          -                          -                          -
8     1978            1.06%                                    6.56%  ...                          -                          -                          -
9     1979           12.31%                                   18.44%  ...                          -                          -                          -
10    1980           25.77%                                   32.50%  ...                          -                          -                          -
11    1981           −9.73%                                   −4.92%  ...                          -                          -                          -
12    1982           14.76%                                   21.55%  ...                          -                          -                          -
13    1983           17.27%                                   22.56%  ...                          -                          -                          -
14    1984            1.40%                                    6.27%  ...                      8.76%                          -                          -
15    1985           26.33%                                   31.73%  ...                     10.49%                          -                          -
16    1986           14.62%                                   18.67%  ...                     10.76%                          -                          -
17    1987            2.03%                                    5.25%  ...                      9.86%                          -                          -
18    1988           12.40%                                   16.61%  ...                     12.17%                          -                          -
19    1989           27.25%                                   31.69%  ...                     16.61%                     11.55%                          -
20    1990           −6.56%                                   −3.10%  ...                     13.94%                     11.16%                          -
21    1991           26.31%                                   30.47%  ...                     14.34%                     11.90%                          -
22    1992            4.46%                                    7.62%  ...                     15.47%                     11.34%                          -
23    1993            7.06%                                   10.08%  ...                     15.72%                     12.76%                          -
24    1994           −1.54%                                    1.32%  ...                     14.52%                     14.58%                     10.98%
25    1995           34.11%                                   37.58%  ...                     14.81%                     14.60%                     12.22%
26    1996           20.26%                                   22.96%  ...                     16.80%                     14.56%                     12.55%
27    1997           31.01%                                   33.36%  ...                     17.52%                     16.65%                     13.07%
28    1998           26.67%                                   28.58%  ...                     17.90%                     17.75%                     14.94%
29    1999           19.53%                                   21.04%  ...                     18.93%                     17.88%                     17.25%
30    2000          −10.14%                                   −9.10%  ...                     16.02%                     15.68%                     15.34%
31    2001          −13.04%                                  −11.89%  ...                     13.74%                     15.24%                     13.78%
32    2002          −23.37%                                  −22.10%  ...                     11.48%                     12.71%                     12.98%
33    2003           26.38%                                   28.68%  ...                     12.22%                     12.98%                     13.84%
34    2004            8.99%                                   10.88%  ...                     10.94%                     13.22%                     13.54%
35    2005            3.00%                                    4.91%  ...                     11.52%                     11.94%                     12.48%
36    2006           13.62%                                   15.79%  ...                     10.64%                     11.80%                     13.37%
37    2007            3.53%                                    5.49%  ...                     10.49%                     11.82%                     12.73%
38    2008          −38.49%                                  −37.00%  ...                      6.46%                      8.43%                      9.77%
39    2009           23.45%                                   26.46%  ...                      8.04%                      8.21%                     10.54%
40    2010           12.78%                                   15.06%  ...                      6.76%                      9.14%                      9.94%
41    2011           -0.00%                                    2.11%  ...                      5.45%                      7.81%                      9.28%
42    2012           13.41%                                   16.00%  ...                      4.47%                      8.22%                      9.71%
43    2013           29.60%                                   32.39%  ...                      4.68%                      9.22%                     10.26%
44    2014           11.39%                                   13.69%  ...                      4.24%                      9.85%                      9.62%
45    2015           −0.73%                                    1.38%  ...                      5.00%                      8.19%                      9.82%
46    2016            9.54%                                   11.96%  ...                      6.69%                      7.68%                      9.15%
47    2017           19.42%                                   21.83%  ...                      9.92%                      7.19%                      9.69%
48    2018           −6.24%                                   −4.38%  ...                      7.77%                      5.62%                      9.07%
49    2019           28.88%                                   31.49%  ...                      9.00%                      6.06%                     10.22%
50    2020           16.26%                                   18.40%  ...                      9.88%                      7.47%                      9.56%
51    High           34.11%                                   37.58%  ...                     18.93%                     17.88%                     17.25%
52     Low          −38.49%                                  −37.00%  ...                      4.24%                      5.62%                      9.07%
53  Median           12.31%                                   15.06%  ...                     10.76%                     11.68%                     10.98%
54    Year  Change in Index  Total Annual Return Including Dividends  ...  15 Year Annualized Return  20 Year Annualized Return  25 Year Annualized Return

[55 rows x 9 columns]
```
