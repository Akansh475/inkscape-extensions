# coding=utf-8

from gcodetools import Gcodetools
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentBytes

class TestGcodetoolsBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = Gcodetools
    comparisons = [(
        '--id=p1', '--active-tab="area"', '--max-area-curves=100',
        '--area-inkscape-radius=-10', '--area-tool-overlap=0',
        '--area-fill-angle=0', '--area-fill-shift=0', '--area-fill-method=0',
        '--area-fill-method=0', '--area-find-artefacts-diameter=5',
        '--area-find-artefacts-action=mark with an arrow',
        '--biarc-tolerance=1', '--biarc-max-split-depth=4',
        '--path-to-gcode-order=subpath by subpath',
        '--path-to-gcode-depth-function=d',
        '--path-to-gcode-sort-paths=false', '--Zscale=1', '--Zoffset=0',
        '--auto_select_paths=true', '--min-arc-radius=0.05000000074505806',
        '--comment-gcode-from-properties=false', '--filename=output.ngc',
        '--add-numeric-suffix-to-filename=true', '--directory=/home',
        '--Zsafe=5', '--unit=G21 (All units in mm)', '--postprocessor= ',
        '--create-log=false')]
    compare_filters = [CompareOrderIndependentBytes()]
