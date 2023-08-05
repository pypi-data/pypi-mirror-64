# Compare package versions in all their varied glory.

## Description

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

## Contact

This module is [developed in a Gitlab repository][gitlab].
The author is [Peter Pentchev][roam].

## Version history

### 0.1.0

- first public release

[gitlab]: https://gitlab.com/ppentchev/python-trivver
[git]: https://gitlab.com/ppentchev/python-trivver.git
[roam]: mailto:roam@ringlet.net
