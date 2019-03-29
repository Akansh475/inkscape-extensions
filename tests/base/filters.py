#
# Copyright (C) 2019 Thomas Holder
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# pylint: disable=too-few-public-methods
#
"""
Comparison filters for use with the ComparisonMixin.

Each filter should be initialised in the list of
filters that are being used.

compare_filters = [
    CompareNumericFuzzy(),
    CompareOrderIndependentLines(option=yes),
]
"""

import re

class Compare(object):
    def __init__(self, **options):
        self.options = options

    def __call__(self, content):
        return self.filter(content)

    @staticmethod
    def filter(contents):
        return contents

class CompareNumericFuzzy(Compare):
    @staticmethod
    def filter(contents):
        func = lambda m: b'%.3f' % (float(m.group(0)))
        contents = re.sub(br'\d+\.\d+', func, contents)             # 1.2345678 -> 1.2346
        contents = re.sub(br'(\d\.\d+?)0+\b', br'\1', contents)     # 1.2300 -> 1.23, 50.0000 -> 50.0
        contents = re.sub(br'(\d)\.0+(?=\D|\b)', br'\1', contents)  # 50.0 -> 50
        return contents

class CompareWithPathSpace(Compare):
    """Make sure that path segment commands have spaces around them"""
    @staticmethod
    def filter(contents):
        def func(match):
            """We've found a path command, process it"""
            new = re.sub(br'\s*([LZMHVCSQTAatqscvhmzl])\s*', br' \1 ', match.group(1))
            return b' d="' + new + b'"'
        return re.sub(br' d="([^"]*)"', func, contents)

class CompareRandomDigits(Compare):
    @staticmethod
    def filter(contents):
        return re.sub(br'\d+', b'0', contents)    # 123 -> 0

class CompareSize(Compare):
    @staticmethod
    def filter(contents):
        return len(contents)

class CompareOrderIndependentBytes(Compare):
    @staticmethod
    def filter(contents):
        return sorted(contents)

class CompareOrderIndependentLines(Compare):
    @staticmethod
    def filter(contents):
        return sorted(contents.splitlines())

class CompareOrderIndependentStyle(Compare):
    @staticmethod
    def filter(contents):
        contents = CompareNumericFuzzy.filter(contents)
        def func(m):
            sty = b';'.join(sorted(m.group(1).split(b';')))
            return b'style="%s"' % (sty,)
        return re.sub(br'style="([^"]*)"', func, contents)

class CompareOrderIndependentStyleAndPath(Compare):
    @staticmethod
    def filter(contents):
        contents = CompareOrderIndependentStyle.filter(contents)
        def func(m):
            d = b'X'.join(sorted(re.split(br'[A-Z]', m.group(1))))
            return b'd="%s"' % (d,)
        return re.sub(br'\bd="([^"]*)"', func, contents)

class CompareOrderIndependentTags(Compare):
    @staticmethod
    def filter(contents):
        return sorted(re.split(br'>\s*<', contents))

