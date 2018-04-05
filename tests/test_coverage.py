#
# Copyright (C) 2018 Martin Owens
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110, USA.
#
"""
Test how well we cover the code with tests.
"""

import os

from tests.base import TestCase, test_support

class ScriptCoverageTest(TestCase):
    """Does each effect have a basic test"""
    def test_basic_tests(self):
        """Check each extension has a test suite"""
        mods = []
        tests = []
        for path, _, files in os.walk(self.root_dir):
            if '.git' in path or path.endswith('__pycache__'):
                continue
            path = path[len(self.root_dir)+1:]
            for fname in files:
                if not fname.endswith('.py') or '__' in fname or fname == 'setup.py':
                    continue
                if fname.startswith('test_'):
                    tests.append(fname[5:-3].lower())
                else:
                    name = fname[:-3]
                    if path:
                        name = path.replace('/', '_') + '_' + name
                    mods.append(name.lower())

        not_tested = sorted(list(set(mods) - set(tests)))
        not_matched = sorted(list(set(tests) - set(mods) - set(['coverage'])))

        print(set(mods) & set(tests))
        self.assertFalse(
            bool(not_tested), "Found {:d} not tested modules: {}\n{} ".format(
                len(not_tested), '\n - '.join(not_tested), '\n + '.join(not_matched)))

if __name__ == '__main__':
    test_support.run_unittest(ScriptCoverageTest)

