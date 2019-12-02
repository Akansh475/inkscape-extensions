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

INTERNAL_ARGS = ('help', 'output', 'id', 'selected-nodes')
ARG_TYPES = {
    'Boolean': 'bool',
    'str': 'string',
    'int': 'integer',
}

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
                self.assertParams(inx, cls)

    def assertParams(self, inx, cls): # pylint: disable=invalid-name
        """Confirm the params in the inx match the python script"""
        params = dict([(param.name, self.parse_param(param)) for param in inx.params])
        args = dict(self.introspect_arg_parser(cls().arg_parser))
        mismatch_a = list(set(params) ^ set(args) & set(params))
        mismatch_b = list(set(args) ^ set(params) & set(args))
        self.assertFalse(mismatch_a, "{}: Inx params missing from arg parser".format(inx.filename))
        self.assertFalse(mismatch_b, "{}: Script args missing from inx xml".format(inx.filename))
        #print(f"{inx.ident} PARAMS {mismatch_a} {mismatch_b}")

    def introspect_arg_parser(self, arg_parser):
        """Pull apart the arg parser to find out what we have in it"""
        for action in arg_parser._optionals._actions: # pylint: disable=protected-access
            for opt in action.option_strings:
                # Ignore params internal to inkscape (thus not in the inx)
                if opt.startswith('--') and opt[2:] not in INTERNAL_ARGS:
                    yield (opt[2:], self.introspect_action(action))

    def introspect_action(self, action):
        """Pull apart a single action to get at the juicy insides"""
        return {
            'type': ARG_TYPES.get((action.type or str).__name__, 'string'),
            'default': action.default,
            'choices': action.choices,
            'help': action.help,
        }

    def parse_param(self, param):
        """Pull apart the param element in the inx file"""
        if param.param_type == 'optiongroup':
            return {
                'type': 'string',
                'choices': param.options,
                'default': param.options[0],
            }
        return {
            'type': param.param_type,
            'default': param.text,
            'choices': None,
        }
