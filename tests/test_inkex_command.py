# coding=utf-8
"""
Test Inkex command launching functionality.
"""

from tests.base import TestCase
from inkex.command import which, write_svg, to_arg, to_args, call, inkscape, inkscape_command, take_snapshot

class CommandTest(TestCase):
    """Test command API"""
    def ignore_command_mock(self, program, arglst):
        return True

    def test_binary_call(self):
        """Calls should allow binary stdin"""
        # https://gitlab.com/inkscape/extensions/commit/2e504f2a3f6bb627f17b267c5623a71005d7234d#note_164780678
        binary = b'\x1f\x8b\x08\x00eh\xc3\\\x02\xffK\xcb\xcf\x07\x00!es\x8c\x03\x00\x00\x00'
        stdout = call('gunzip', stdin=binary)

