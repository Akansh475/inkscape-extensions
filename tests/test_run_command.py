# coding=utf-8
from run_command import run


class TestRunCommand(object):
    def test_basic_run(self):
        # Make sure a benign command doesn't raise any exceptions
        assert run("touch %s", 'touch') is None
