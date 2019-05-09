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

import ads

DESCRIPTION = "Query the ADS database."

# Set up the command line options
ARGUMENTS = (
    (["-a", "--author"], {"nargs": '?',
                          "type": str,
                          "help": "Author search string e.g. doe, john."}),
    (["-b", "--bibstem"], {"nargs": '?',
                           "type": str,
                           "help": "Bibstem search string e.g. apj."}),
    (["-f", "--full"], {"nargs": '?',
                        "type": str,
                        "help": "Full text search e.g. gravity."}),
    (["-n", "--rows"], {"nargs": '?',
                        "type": int,
                        "default": 10,
                        "help": "Number of rows to show."}),
    (["-s", "--sort"], {"nargs": '?',
                        "type": str,
                        "default": "citation_count desc",
                        "help": "Sort string e.g. citation_count desc."}),
    (["-y", "--year"], {"nargs": '?',
                        "type": str,
                        "help": "Year search string e.g. 2000-2001."}),
)

# Parse the command line arguments
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
for args, kwargs in ARGUMENTS:
    PARSER.add_argument(*args, **kwargs)
ARGS = PARSER.parse_args()

# Build the query dictionary i.e. filter out `none` values
QUERY_DICT = {k: v for k, v in ARGS.__dict__.items() if v}

# Include these fields in the query result
FIELDS = ["first_author", "bibcode", "title", "year"]

def get_link(paper):
    """
    Return a link for the papers bibcode.
    """
    return "https://ui.adsabs.harvard.edu/link_gateway/%s/" % paper.bibcode

def print_header():
    """
    Pretty print the header information
    """
    print("%-19s %-15s %-04s %-100s" % ("bibcode", "author", "year", "title"),
          file=sys.stderr)
    print("", file=sys.stderr)

def print_row(paper):
    """
    Pretty print the essential information of a paper
    """
    func_trunc = lambda s, x: s if len(s) < x else s[:x-3] + "..."
    print(u"%-19s %-15s %04s %-100s"
          % (paper.bibcode,
             func_trunc(paper.first_author, 15),
             paper.year,
             func_trunc(paper.title[0], 100)))

def main():
    """
    Query ADS for the search string and print formatted results.
    """

    # Check for empty dictionary
    if (len(QUERY_DICT) == 2
        and ("sort" in QUERY_DICT)
        and "rows" in QUERY_DICT):
        print("Error: At least one search parameter must be provided.",
              file=sys.stderr)
        PARSER.print_usage()
        return 0

    # Query the ADS database
    query = ads.SearchQuery(fl=FIELDS, **QUERY_DICT)

    # Print the output
    print_header()
    for paper in query:
        print_row(paper)

    # Print useful information about remaining quota and reset time
    print("", file=sys.stderr)
    print("Remaining (limit): %4s (%4s)"
          % (query.response.get_ratelimits()["remaining"],
             query.response.get_ratelimits()["limit"]), file=sys.stderr)
    print("Reset (UTC): %s"
          % time.ctime(int(query.response.get_ratelimits()["reset"])),
          file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
