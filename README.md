# pyads

Stupid command line tool to query the ADS database.

# Installation

For querying the ADS database, one needs to sign up to ADS and obtain an API
key. Detailed instructions may be found from the installation guide for the
`ads` python package at <https://ads.readthedocs.io/en/latest/>.

# Examples

    $ pyads.py -a "doe, j" -b apj -y=2000-2001

returns whatever is found from the ADS database with the constraints. See help
for details.

Probably the most important output information is the bibcode of each returned
item. See the example scripts for some potentially useful scenarios.

# Help

Try

    $ pyads.py --help

Useful links for the ADS API and the `ads` python package
+ <https://ads.readthedocs.io/en/latest/>
+ <https://ui.adsabs.harvard.edu/about/>
+ <http://adsabs.github.io/help/api/>
+ <https://github.com/adsabs/adsabs-dev-api/blob/master/Search_API.ipynb>
+ <https://adsabs.github.io/help/search/comprehensive-solr-term-list>

# TODO

+ Extend the list of arguments already provided
+ Add options for controlling output e.g. provide links to abstract, pdf
  download.
