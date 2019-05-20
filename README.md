# aggregate-prefixes
[![Build Status](https://travis-ci.org/tycho/aggregate-prefixes.svg?branch=master)](https://travis-ci.org/tycho/aggregate-prefixes)

Fast IPv4 and IPv6 prefix aggregator written in Python.  

Gets a list of unsorted IPv4 or IPv6 prefixes from argument or stdin and
returns a sorted list of aggregates to stdout. Errors go to stderr.

## CLI Syntax for executable

```
usage: aggregate-prefixes [-h] [--max-length [LENGTH]] [--verbose] [--version]
                          prefixes

Aggregates IPv4 or IPv6 prefixes from file or STDIN

positional arguments:
  prefixes              Unsorted list of IPv4 or IPv6 prefixes. Use '-' for
                        STDIN.

optional arguments:
  -h, --help            show this help message and exit
  --max-length [LENGTH], -m [LENGTH]
                        Discard longer prefixes prior to processing
  --verbose, -v         Display verbose information about the optimisations
  --version, -V         show program's version number and exit

```

# Usage as module
```
$ python
Python 3.7.3 (default, Mar 26 2019, 21:43:19)
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> from aggregate_prefixes import aggregate_prefixes
>>> list(aggregate_prefixes(['192.0.2.0/32', '192.0.2.1/32', '192.0.2.2/32']))
['192.0.2.0/31', '192.0.2.2/32']
>>> 
```

# Python compatibility
Tested with:
 - Python 3.7.3
 - PyPy3 7.1.1 (Python 3.6.1 compatibility level)
