"""Compare package versions in all their varied glory.

This module provides the `compare()` function which compares two
version strings and returns a negative value, zero, or a positive
value depending on whether the first string represents a version
number lower than, equal to, or higher than the second one, and
the `key_compare()` function which may be used as a key for e.g.
`sorted()`.

This module does not strive for completeness in the formats of
version strings that it supports. Some version strings sorted by
its rules are:
- 0.1.0
- 0.2.alpha
- 0.2
- 0.2.1
- 0.2a
- 0.2a.1
- 0.2p3
- 1.0.beta
- 1.0.beta.2
- 1.0
"""

import functools
import re

from typing import List, Optional, Text, Union


RE_COMPONENT = re.compile(
    r""" ^
    (?P<num> [0-9]+ )? (?P<rest> .+ )?
$ """,
    re.X,
)

VERSION = "0.1.0"


def cmp_strings(first, second):
    # type: (Optional[Text], Optional[Text]) -> int
    """Compare two strings, possibly undefined."""
    if first is not None:
        if second is not None:
            if first == second:
                return 0
            if first > second:
                return 1
            return -1

        return 1

    if second is not None:
        return -1

    return 0


def cmp_components(first, second):
    # type: (Text, Text) -> int
    """Compare a single pair of version components.

    - alpha4 < beta
    - alpha4 < 1
    - 1 < 1sp2
    - 1 < 2"""
    a_m = RE_COMPONENT.match(first)
    assert a_m
    a_num = a_m.groupdict()["num"]
    a_rest = a_m.groupdict()["rest"]

    b_m = RE_COMPONENT.match(second)
    assert b_m
    b_num = b_m.groupdict()["num"]
    b_rest = b_m.groupdict()["rest"]

    if a_num is not None:
        if b_num is not None:
            if a_num != b_num:
                return int(a_num) - int(b_num)
            return cmp_strings(a_rest, b_rest)

        return 1

    if b_num is not None:
        return -1

    return cmp_strings(a_rest, b_rest)


def cmp_examine_extra(a_first):
    # type: (Text) -> int
    """Does the version component start with a digit?

    In other words, is it an alpha/beta version or not?"""
    a_m = RE_COMPONENT.match(a_first)
    assert a_m
    if a_m.groupdict()["num"] is not None:
        return 1
    return -1


def cmp_extra(first, second):
    # type: (List[Text], List[Text]) -> int
    """Check for alpha versions in the longer list's additional components.

    Does one of the lists:
    - have more components than the other, and
    - the first extra component starts with a digit, not a letter?
    (if it starts with a letter, it's an alpha/beta/pre-release version)"""
    a_len = len(first)
    b_len = len(second)
    if a_len == b_len:
        return 0

    if a_len > b_len:
        a_first = first[b_len]
        return cmp_examine_extra(a_first)

    b_first = second[a_len]
    return -cmp_examine_extra(b_first)


def cmp_dot_components(first, second):
    # type: (Text, Text) -> int
    """Split versions number no dots, compare them component by component."""
    a_dot = first.split(".")
    b_dot = second.split(".")
    for a_comp, b_comp in zip(a_dot, b_dot):
        res = cmp_components(a_comp, b_comp)
        if res != 0:
            return res

    # Does one of them have more dot-delimited components than the other?
    return cmp_extra(a_dot, b_dot)


# Split a version number on dashes, compare them component by component
def compare(first, second):
    # type: (Union[Text, str], Union[Text, str]) -> int
    """Compare two full versions strings."""
    a_dash = Text(first).split("-")
    b_dash = Text(second).split("-")
    for a_comp, b_comp in zip(a_dash, b_dash):
        res = cmp_dot_components(a_comp, b_comp)
        if res != 0:
            return res

    # Does one of them have more dash-delimited components than the other?
    # (don't check for beta versions in this case)
    return len(a_dash) - len(b_dash)


key_compare = functools.cmp_to_key(compare)  # pylint: disable=invalid-name

__all__ = ("VERSION", "compare", "key_compare")
