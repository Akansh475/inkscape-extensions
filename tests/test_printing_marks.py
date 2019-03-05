# coding=utf-8
from printing_marks import PrintingMarks
from tests.base import InkscapeExtensionTestMixin, TestCase


class PrintingMarksBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = PrintingMarks
        self.e = self.effect()
