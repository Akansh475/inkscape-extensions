# coding=utf-8
import pytest

from prepare_file_save_as import PrepareFileSave
from tests.base import InkscapeExtensionTestMixin, TestCase

@pytest.mark.skip("This uses Popen")
class TestPrepareFileSaveBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = PrepareFileSave
