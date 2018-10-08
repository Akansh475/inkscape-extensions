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
import sys
import inspect

from inkex.effect import Effect
from inkex.utils import DependencyError

from tests.base import TestCase, test_support
from tests.base.mock import replace_function

class NoMainError(Exception):
    """Many effects try and call affect without even checking if they are running
    as a script or being loaded as modules. We invite them to the fail couch."""


class ExitedError(Exception):
    """Prevent modules from calling sys.exit, which they shouldn't be doing."""


class ScriptCoverageTest(TestCase):
    """Does each effect have a basic test"""
    _current_result = None

    def test_basic_tests(self):
        """Check each extension has a test suite and list ones that don't.

        It will also attempt to run any effect it can find with the default test and
        cause multiple failures or errors. This is a meta-test pattern and shouldn't
        be copied unless you know why it's being used.
        """
        mods, tests = self.get_mod_list()
        not_tested = sorted(list(set(mods) - set(tests)))
        not_matched = sorted(list(set(tests) - set(mods) - set(['coverage'])))

        # We catch any known effects that use inkex and test them with the minimum runner
        for module in list(not_tested):
            if os.path.isfile(module + '.py'):
                if self.auto_test_effect(module):
                    # We remove this effect from the list of 'not-tested' not this
                    # doesn't mean the effect has no errors.
                    not_tested.remove(module)
            else:
                print("File {}.py doesn't exist?".format(module))

        # Usually this will contain non-effect modules that are untested
        self.assertFalse(
            bool(not_tested), "Found {:d} not tested modules: {}\n{} ".format(
                len(not_tested), '\n - '.join(not_tested), '\n + '.join(not_matched)))

    @replace_function(Effect, 'affect', NoMainError("{1}.py calls affect outside of __main__"))
    def get_effect_module(self, module):
        """Returns the module for use, catching issues"""
        try:
            return __import__(module, fromlist=[])
        except DependencyError as err:
            addSkip = getattr(self._current_result, 'addSkip', None)
            if addSkip is not None:
                addSkip(self, str(err))
        except ImportError as err:
            if module in str(err):
                return False
            self._current_result.addError(self, sys.exc_info())
        except Exception: # pylint: disable=broad-except
            self._current_result.addError(self, sys.exc_info())

    @replace_function(os, 'chdir', IOError("Hell no you cn't do that!"))
    @replace_function(sys, 'exit', ExitedError("Tried to sys.exit(), don't do that!"))
    def auto_test_effect(self, module):
        """Take an effect module and test it.

        Returns:
          - True   - module was tested (failure or success).
          - False  - the module isn't an effect or doesn't exist.

        """
        mod = self.get_effect_module(module)
        if not mod:
            # Failure to import doesn't mean we got to test anything.
            return False

        mod_result = None
        for value in list(mod.__dict__.values()):
            mod_result = True
            if inspect.isclass(value) and issubclass(value, Effect) and value != Effect:
                try:
                    self.assertEffectEmpty(value)
                    self._current_result.addSuccess(self)
                except self.failureException:
                    self._current_result.addFailure(self, sys.exc_info())
                except Exception: #pylint: disable=broad-except
                    self._current_result.addError(self, sys.exc_info())

        return mod_result is not None

    def get_mod_list(self):
        """Gets a list of python files that may be effects or modules

        Returns three lists:
          - mods   - List of modules, folders separated by '.'
          - tests  - List of tests found

        """
        mods, tests, alls = [], [], []
        for path, _, files in os.walk(self.root_dir):
            if '.git' in path or path.endswith('__pycache__'):
                continue
            path = path[len(self.root_dir)+1:]
            for fname in files:
                if not fname.endswith('.py') or '__' in fname or fname == 'setup.py':
                    continue
                if fname == 'inkex.py':
                    # legacy compatibility module
                    continue
                if fname.startswith('test_'):
                    if fname.endswith('_all.py'):
                        alls.append(fname[5:-7].lower())
                    else:
                        tests.append(fname[5:-3].lower())
                else:
                    name = fname[:-3]
                    if path:
                        name = os.path.join(path, name).replace('/', '_')
                    mods.append(name.lower())

        # Alls are a list of test suites that cover multiple modules. So our matching
        # must be set to {name}_* to cover this case.
        for aull in alls:
            for mod in mods:
                if mod.startswith(aull):
                    tests.append(mod)

        return mods, tests

    def __call__(self, result=None, **kw):
        """Wrapper for TestCase run to insert multiple errors (sub-errors)"""
        self._current_result = result if result is not None else self.defaultTestResult()
        super(ScriptCoverageTest, self).__call__(result=result, **kw)


if __name__ == '__main__':
    test_support.run_unittest(ScriptCoverageTest)

