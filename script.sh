#!/bin/sh
#
# A shell script template. Remove this line and add your description.
#
# Author: Akke Viitanen
# Email: akke.viitanen@helsinki.fi

author=$1
year=$2

# Print a list of articles to choose from
choice=$(python3 pyads.py -n 20 -a "^$author" -y $year --print_row \
         | dmenu -l 20 \
         | cut -f 1 -d ' ')

# Fetch the bibtex for chosen article
python3 pyads.py -a $author -c "$choice" -y $year --print_bibtex
