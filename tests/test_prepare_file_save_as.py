# coding=utf-8
import pytest

from tests.base import InkscapeExtensionTestMixin, TestCase


@pytest.mark.skip("This uses Popen")
class TestPrepareFileSaveBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        from prepare_file_save_as import PrepareFileSave
        self.effect = PrepareFileSave
        self.e = self.effect()
