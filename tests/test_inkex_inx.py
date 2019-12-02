#!/usr/bin/env python
# coding=utf-8
"""
Test elements extra logic from svg xml lxml custom classes.
"""

import os
from glob import glob

from inkex.utils import PY3
from inkex.inx import InxFile
from inkex.tester import TestCase

class InxTestCase(TestCase):
    """Test INX files"""
    def test_inx_files(self):
        """Get all inx files and test each of them"""
        if not PY3:
            self.skipTest("No INX testing in python2")
            return
        for inx_file in glob(os.path.join(self._testdir(), '..', '*.inx')):
            inx = InxFile(inx_file)
            if 'help' in inx.ident or inx.script.get('interpreter', None) != 'python':
                continue
            cls = inx.extension_class
            # Check class can be matched in python file
            self.assertTrue(cls, 'Can not find class for {}'.format(inx.filename))
            # Check name is reasonable for the class
            if not cls.multi_inx:
                self.assertEqual(
                    cls.__name__, inx.slug,
                    "Name of extension class {}.{} is different from ident {}".format(
                        cls.__module__, cls.__name__, inx.slug))

            self.assertParams(inx, cls())

    def assertParams(self, inx, cls): # pylint: disable=invalid-name
        """Confirm the params in the inx match the python script"""
        params = inx.params
