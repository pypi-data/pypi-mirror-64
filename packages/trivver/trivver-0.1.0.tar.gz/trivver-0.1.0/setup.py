#!/usr/bin/env python
#
# Copyright (c) 2020  Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
"""Setup configuration for the trivial version comparison module."""

import io
import re

from typing import Text, cast

import setuptools  # type: ignore


RE_VERSION = re.compile(
    r"""^
    \s* VERSION \s* = \s* "
    (?P<version>
           (?: 0 | [1-9][0-9]* )    # major
        \. (?: 0 | [1-9][0-9]* )    # minor
        \. (?: 0 | [1-9][0-9]* )    # patchlevel
    (?: \. [a-zA-Z0-9]+ )?          # optional addendum (dev1, beta3, etc.)
    )
    " \s*
    $""",
    re.X,
)


def get_version():
    # type: () -> Text
    """ Get the version string from the module's __init__ file. """
    with io.open("trivver/__init__.py", encoding="UTF-8") as init:
        found = [
            match.group("version")
            for match in (RE_VERSION.match(cast(Text, line)) for line in init)
            if match
        ]

    assert len(found) == 1
    return found[0]


def get_long_description():
    # type: () -> Text
    """Read the long description from the README file."""
    with io.open("README.md", mode="r", encoding="UTF-8") as readme:
        return cast(Text, readme.read())


setuptools.setup(
    name="trivver",
    version=get_version(),
    packages=("trivver",),
    author="Peter Pentchev",
    author_email="roam@ringlet.net",
    description="A library for comparing version strings",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    keywords="version",
    url="https://gitlab.com/ppentchev/python-trivver",
    setup_requires=["typing"],
    install_requires=["typing"],
    package_data={"trivver": ["py.typed"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: DFSG approved",
        "License :: Freely Distributable",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=True,
)
