# coding=utf-8
from convert2dashes import Dashit
from inkex import NSS
from tests.base import InkscapeExtensionTestMixin, TestCase


class DashitBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Dashit
        self.e = self.effect()

    def test_basic(self):
        args = ['--id=dashme',
                self.data_file('svg', 'dash.svg')]
        self.e.run(args)
        old_dashes = self.e.original_document.xpath('//svg:path', namespaces=NSS)[0].path
        new_dashes = self.e.document.xpath('//svg:path', namespaces=NSS)[0].path
        assert len(new_dashes) > len(old_dashes)
