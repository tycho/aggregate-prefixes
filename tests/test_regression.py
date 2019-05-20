# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Regression tests for package aggregate-prefixes
"""

import io
import sys
import unittest

from mock import patch

from aggregate_prefixes import aggregate_prefixes
from aggregate_prefixes.cli import main as cli_main


def stub_stdin(testcase_inst, inputs):
    stdin = sys.stdin

    def cleanup():
        sys.stdin = stdin

    testcase_inst.addCleanup(cleanup)
    sys.stdin = StringIO(inputs)


def stub_stdouts(testcase_inst):
    stderr = sys.stderr
    stdout = sys.stdout

    def cleanup():
        sys.stderr = stderr
        sys.stdout = stdout

    testcase_inst.addCleanup(cleanup)
    sys.stderr = StringIO()
    sys.stdout = StringIO()


class TestAggregatePrefixes(unittest.TestCase):
    """
    Provide regression tests for package aggregate-prefixes
    """
    def test_00__default_wins(self):
        """Test if default covers all the other prefixes"""
        self.assertEqual(list(aggregate_prefixes(["0.0.0.0/0", "10.0.0.0/16"])),
                         ["0.0.0.0/0"])

    def test_01__join_two(self):
        """Test if contigous prefixes get aggregated"""
        self.assertEqual(list(aggregate_prefixes(["10.0.0.0/8", "11.0.0.0/8"])),
                         ["10.0.0.0/7"])

    def test_02__mix_v4_v6_default(self):
        """Test if error is raised when mixing IPv4 and IPv6"""
        with self.assertRaises(Exception) as context:
            list(aggregate_prefixes(["0.0.0.0/0", "::/0"]))
        self.assertTrue("are not of the same version" in str(context.exception))

    def test_03__lot_of_ipv4(self):
        """Test if all the IPv4 /8s get aggreagated to 0.0.0.0/8"""
        pfxs = []
        for i in range(0, 256):
            pfxs.append("{}.0.0.0/8".format(i))
        self.assertEqual(list(aggregate_prefixes(pfxs)), ["0.0.0.0/0"])

    def test_04__lot_of_ipv4_holes(self):
        """Test if non contigous IPv4 prefixes are handled correctly"""
        pfxs = []
        for i in range(5, 200):
            pfxs.append("{}.0.0.0/8".format(i))
        outcome = ["5.0.0.0/8", "6.0.0.0/7", "8.0.0.0/5", "16.0.0.0/4",
                   "32.0.0.0/3", "64.0.0.0/2", "128.0.0.0/2", "192.0.0.0/5"]
        self.assertEqual(list(aggregate_prefixes(pfxs)), outcome)

    def test_05__reduce_dups(self):
        """Test if duplicates are removed"""
        self.assertEqual(list(aggregate_prefixes(["2001:db8::/32", "2001:db8::/32"])),
                         ["2001:db8::/32"])

    def test_06__non_ip_input(self):
        """Test if error is raised with non IP input"""
        stub_stdouts(self)
        with self.assertRaises(Exception) as context:
            list(aggregate_prefixes(["this_is_no_prefix", "10.0.0.0/24"]))
        self.assertTrue(
            "'this_is_no_prefix' does not appear to be an IPv4 or IPv6 network" \
            in str(context.exception)
        )

    def test_07__main(self):
        """Test if it can handle empty lines, spaces and comments"""
        stub_stdin(self, '1.1.1.24/29\n1.1.1.0/24\n#this_is_no_prefix\n1.1.1.1/32 1.1.0.0/24\n\n')
        stub_stdouts(self)
        with patch.object(sys, 'argv', ["prog.py", "-"]):
            cli_main()
        self.assertEqual(sys.stdout.getvalue(), '1.1.0.0/23\n')

    def test_08__maxlength(self):
        """Test if max-length is handled correctly"""
        stub_stdin(self, '10.0.0.0/24\n10.0.1.0/25\n10.0.1.128/25\n')
        stub_stdouts(self)
        with patch.object(sys, 'argv', ["prog.py", "-m", "24", "-"]):
            cli_main()
        self.assertEqual(sys.stdout.getvalue(), '10.0.0.0/24\n')


class StringIO(io.StringIO):
    """A "safely" wrapped version of StringIO"""
    def __init__(self, value=''):
        value = value.encode('utf8', 'backslashreplace').decode('utf8')
        io.StringIO.__init__(self, value)

    def write(self, msg):
        io.StringIO.write(self, msg.encode(
            'utf8', 'backslashreplace').decode('utf8'))


def main():
    """Run unittest"""
    unittest.main()


if __name__ == '__main__':
    main()
