# -*- coding: utf-8 -*-

"""
Provides CLI interface for package aggregate-prefixes
"""

from __future__ import absolute_import
import fileinput
import sys
from itertools import ifilter

from aggregate_prefixes.aggregate_prefixes import aggregate_prefixes


def main():
    """
    Aggregates IPv4 or IPv6 prefixes from file or STDIN.

    Reads a list of unsorted IPv4 or IPv6 prefixes from a file or STDIN.
    Returns a sorted list of aggregates to STDOUT.
    """

    prefixes = ifilter(None, set([_.strip() for _ in fileinput.input()]))
    try:
        aggregates = aggregate_prefixes(prefixes)
    except (ValueError, TypeError), error:
        sys.exit(error)
    print '\n'.join(aggregates)


if __name__ == '__main__':
    main()
