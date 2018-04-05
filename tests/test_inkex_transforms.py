#!/usr/bin/env python

from tests.base import TestCase, test_support

from inkex.const import NSS
from inkex.effect import Effect
from inkex.transforms import computeBBox

class ComputeBBoxTest(TestCase):
    def setUp(self):
        args = [self.data_file('svg', 'simpletransform.test.svg')]
        self.e = Effect()
        self.e.affect(args, False)

    #def test_scaled_object(self):
    #    "Object in the defs with 50,50 scaled by 0.5 when used"
    #    bbox = computeBBox(self.e.document.xpath("//svg:g", namespaces=NSS))
    #    text_bbox = "{} {} {} {}".format(bbox[0], bbox[1], bbox[2], bbox[3])
    #    self.assertEqual("0.0 25.0 0.0 25.0", text_bbox)

if __name__ == '__main__':
    test_support.run_unittest(ComputeBBoxTest)
