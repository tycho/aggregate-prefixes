# -*- coding: utf-8 -*-

"""
Aggregates IPv4 or IPv6 prefixes.

Core method is aggrega_prefixes in module aggregate_prefixes.
It gets an unsorted list IPv4 or IPv6 prefixes and returns a sorted list of aggregates.

Example:
	>>> from aggregate_prefixes.aggregate_prefixes import aggregate_prefixes
	>>>
	>>> prefixes = ["192.0.2.1/32", "192.0.2.3/32", "192.0.2.2/32"]
	>>> print aggregate_prefixes(prefixes)
	['192.0.2.1/32', '192.0.2.2/31']
	>>>
"""

__version__ = "0.5"
__author__ = "Marco Marzetti"
__author_email__ = "marco@lamehost.it"
__maintainer__ = "Steven Noonan"
__maintainer_email__ = "steven@uplinklabs.net"
__url__ = "https://github.com/tycho/aggregate-prefixes"
__description__ = "Fast IPv4 and IPv6 prefix aggregator written in Python."
__license__ = "MIT"
__classifiers__ = [
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Networking',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
],
