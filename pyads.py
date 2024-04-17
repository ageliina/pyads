#!/usr/bin/env python3
"""
pads
    Query the ADS database via the command line.

example
    $ pyads.py -a "doe, j" -b apj -y=2000-2001
returns whatever is found from the ADS database with the constraints. See help
for details.

help
    $ pyads.py --help

useful links for the ADS API and the ads python package
    https://ads.readthedocs.io/en/latest/
    https://ui.adsabs.harvard.edu/about/
    http://adsabs.github.io/help/api/
    https://github.com/adsabs/adsabs-dev-api/blob/master/Search_API.ipynb
    https://adsabs.github.io/help/search/comprehensive-solr-term-list
"""


import argparse
import sys
import time

DESCRIPTION = "Query the ADS database."
PARSER = argparse.ArgumentParser(description=DESCRIPTION)

# Arguments to control the ADS query
GROUP_QUERY = \
    PARSER.add_argument_group(title="Query arguments",
                              description="Arguments for ADS query control")
GROUP_QUERY.add_argument("-a", "--author", nargs='?', type=str,
                         help="Author search string e.g. doe, john.")
GROUP_QUERY.add_argument("-b", "--bibstem", nargs='?', type=str,
                         help="Bibstem search string e.g. apj.")
GROUP_QUERY.add_argument("-c", "--bibcode", nargs='?', type=str,
                         help="ADS Bibcode search string")
GROUP_QUERY.add_argument("-f", "--full", nargs='?', type=str,
                         help="Full text search e.g. gravity.")
GROUP_QUERY.add_argument("-n", "--rows", nargs='?', type=int, default=10,
                         help="Number of rows to show.")
GROUP_QUERY.add_argument("-s", "--sort", nargs='?', type=str,
                         default="citation_count desc",
                         help="Sort string e.g. citation_count desc.")
GROUP_QUERY.add_argument("-y", "--year", nargs='?', type=str,
                         default=time.localtime().tm_year,
                         help="Year search string e.g. 2000-2001.")

# Arguments to control the output formatting
GROUP_OUTPUT = PARSER.add_mutually_exclusive_group(required=True)
GROUP_OUTPUT.add_argument("--print_row", action="store_true",
                          help="Print a formatted row (bibcode, first author,\
                                year, title) for each query result.")
GROUP_OUTPUT.add_argument("--print_abstract", action="store_true",
                          help="Print the full abstract.")
GROUP_OUTPUT.add_argument("--print_bibtex", action="store_true",
                          help="Print the bibtex entry.")
GROUP_OUTPUT.add_argument("--print_url_abs", action="store_true",
                          help="Print the ADS URL for the abstract.")
GROUP_OUTPUT.add_argument("--print_url_pdf", action="store_true",
                          help="Print the ADS URL for the downloadables.")

# Debug argument
PARSER.add_argument("--debug", help="Enter debug mode", action="store_true")

# Parse the command line arguments
ARGS = PARSER.parse_args()

# Build the query dictionary i.e. filter out `none` values and invalid fields
VALID_FIELDS = ["author", "bibstem", "bibcode", "full", "rows", "sort", "year"]
QUERY_DICT = {"database": "astronomy"}
QUERY_DICT.update({k: v for k, v in ARGS.__dict__.items() if v and k in VALID_FIELDS})

# Include these fields in the query result
FIELDS = [
    "abstract",
    "bibcode",
    "bibtex",
    "doi",
    "first_author",
    "title",
    "year"
]

# Import the ads module
if not ARGS.debug:
    import ads
else:
    import ads.sandbox as ads


def print_row(paper):
    """
    Pretty print the essential information of a paper.
    """
    def func_trunc(string, limit):
        """Truncate a `string` to `limit` characters followed by an ellipsis"""
        return string if len(string) < limit else string[:limit - 3] + "..."
    print(u"%-19s %-20s %-s"
          % (paper.bibcode,
             func_trunc(paper.first_author, 20),
             func_trunc(paper.title[0], 200)))


def print_abstract(paper):
    """
    Print the full abstract of the paper.
    """
    print(paper.abstract)


def print_bibtex(paper):
    """
    Print the bibtex entry of the paper.
    """
    print(ads.ExportQuery(paper.bibcode)())


def print_url_abs(paper):
    """
    Print the url to the ADS abstract.
    """
    if paper.bibcode is None:
        return
    print("https://ui.adsabs.harvard.edu/abs/%s/abstract" % paper.bibcode)


def print_url_pdf(paper):
    """
    Print the publisher/arxiv url to the ADS link gateway.
    """
    if paper.bibcode is None:
        return
    url = "https://ui.adsabs.harvard.edu/link_gateway/%s" % paper.bibcode
    print(url + "/%s_PDF" % ("PUB" if paper.doi is not None else "EPRINT"))


def main():
    """
    Query ADS for the search string and print formatted results.
    """

    # Query the ADS database
    query = ads.SearchQuery(fl=FIELDS, **QUERY_DICT)

    # Print the output
    for paper in query:
        for cond, func in [(ARGS.print_row, print_row),
                           (ARGS.print_abstract, print_abstract),
                           (ARGS.print_bibtex, print_bibtex),
                           (ARGS.print_url_abs, print_url_abs),
                           (ARGS.print_url_pdf, print_url_pdf)]:
            if cond:
                func(paper)

    # Print useful information about remaining quota and reset time
    print("Remaining (limit): %4s (%4s)"
          % (query.response.get_ratelimits()["remaining"],
             query.response.get_ratelimits()["limit"]), file=sys.stderr)

    try:
        time_reset = int(query.response.get_ratelimits()["reset"])
    except ValueError:
        time_reset = 0
    print("Reset (UTC): %s" % time.ctime(time_reset), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
