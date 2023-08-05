"""Test the version comparison routines."""

import unittest

from typing import NamedTuple

import ddt  # type: ignore

import trivver


VersionSet = NamedTuple(  # pylint: disable=invalid-name
    "VersionSet", [("first", str), ("second", str), ("expected", int),]
)


VERSIONS = [
    VersionSet(first="1.0", second="2.0", expected=-1),
    VersionSet(first="1.0", second="1.0.1", expected=-1),
    VersionSet(first="1.0", second="1.0a", expected=-1),
    VersionSet(first="1.0", second="1.0", expected=0),
    VersionSet(first="1.0a", second="1.0a", expected=0),
    VersionSet(first="0.1.0.b", second="0.1.0", expected=-1),
    VersionSet(
        first="3.10.0-1062.1.1.el7.x86_64",
        second="3.10.0-983.13.1.el7.x86_64",
        expected=1,
    ),
    VersionSet(
        first="3.10.0-1062.1.1.el7.x86_64",
        second="3.10.0-1062.1.1.el6.x86_64",
        expected=1,
    ),
]

UNSORTED = [
    "3.10.0-1062.1.1.el7.x86_64",
    "1.0a",
    "0.1.0.b",
    "1.0",
    "3.10.0-983.13.1.el7.x86_64",
    "0.1.0",
    "1.0.1",
    "2.0",
    "3.10.0-1062.1.1.el6.x86_64",
]
SORTED = [
    "0.1.0.b",
    "0.1.0",
    "1.0",
    "1.0.1",
    "1.0a",
    "2.0",
    "3.10.0-983.13.1.el7.x86_64",
    "3.10.0-1062.1.1.el6.x86_64",
    "3.10.0-1062.1.1.el7.x86_64",
]


def sign(value):
    # type: (int) -> int
    """Return the sign of an integer."""
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


@ddt.ddt
class TestVersions(unittest.TestCase):
    """Test the version comparison routines."""

    # pylint: disable=no-self-use

    @ddt.data(*VERSIONS)
    @ddt.unpack
    def test_compare(self, first, second, expected):
        # type: (TestVersions, str, str, int) -> None
        """Compare a single pair of versions."""
        assert sign(trivver.compare(first, second)) == sign(expected)
        assert sign(
            trivver.compare(  # pylint: disable=arguments-out-of-order
                second, first
            )
        ) == sign(-expected)

    def test_sort(self):
        # type: (TestVersions) -> None
        """Sort a list of versions."""
        assert sorted(UNSORTED, key=trivver.key_compare) == SORTED
