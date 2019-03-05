# coding=utf-8
#
# Revision history:
#  * 2012-01-28 (jazzynico): first working version (only checks the extension
#    with the default parameters).
#
from summersnight import Project
from tests.base import InkscapeExtensionTestMixin, TestCase


class EnvelopeBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Project
        self.e = self.effect()
