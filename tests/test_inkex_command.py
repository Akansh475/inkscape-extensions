# coding=utf-8
"""
Test Inkex command launching functionality.
"""
import os
import tempfile
import pytest
import sys
from inkex.tester import BaseCase, TestCase
from inkex.command import (
    ProgramRunError,
    which,
    write_svg,
    to_arg,
    to_args,
    call,
    inkscape,
    inkscape_command,
    take_snapshot,
)
from pathlib import Path


class CommandTest(BaseCase):
    """Test command API"""

    @pytest.mark.skipif(
        sys.platform == "win32", reason="gunzip doesn't exist on windows"
    )
    def test_binary_call(self):
        """Calls should allow binary stdin"""
        # https://gitlab.com/inkscape/extensions/-/commit/2e504f2a3f6bb627f17b267c5623a71005d7234d#note_164780678
        binary = (
            b"\x1f\x8b\x08\x00eh\xc3\\\x02\xffK\xcb\xcf\x07\x00!es\x8c\x03\x00\x00\x00"
        )
        stdout = call("gunzip", stdin=binary)

    def test_command_error(self):
        """Call to test ProgramRunError"""

        with self.assertRaises(ProgramRunError) as cm:
            call("python", "nonexistent_file")
        exc = cm.exception
        self.assertIsInstance(exc, ProgramRunError)
        self.assertEqual(exc.returncode, 2)
        self.assertIn("can't open file", exc.stderr.decode("utf8"))
        self.assertEqual("", exc.stdout.decode("utf8"))
        self.assertIn("can't open file", str(exc))


class InkscapeCommandTest(TestCase):
    def test_long_action_string(self):
        """Test for https://gitlab.com/inkscape/extensions/-/issues/482 (export)"""

        tmpfile = Path(self.tempdir) / "test.png"
        args = {
            "actions": (
                "select-clear;" * 1000
                + f"export-id:r1;export-filename:{tmpfile};export-do;"
            )
        }
        out = inkscape("tests/data/svg/shapes.svg", **args)

        self.assertEqual(out.strip(), "")
        self.assertTrue(os.path.isfile(tmpfile))

    def test_long_action_string_stdout(self):
        """Test for https://gitlab.com/inkscape/extensions/-/issues/482 with stdout"""
        args = {"actions": "select-clear;" * 1000 + "select-by-id:r1;query-x;query-y;"}
        # Need to provide a different svg so the call IDs are unique
        out = inkscape("tests/data/svg/shapes_no_text.svg", **args)

        self.assertEqual(out.splitlines()[0], "100")
        self.assertEqual(out.splitlines()[1], "200")
