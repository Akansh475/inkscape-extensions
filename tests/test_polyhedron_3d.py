# coding=utf-8
from polyhedron_3d import Poly3D
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class Poly3DBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Poly3D
    comparisons = [('--id=r2', '--tab="common"', '--obj=cube',
        '--spec_file=great_rhombicuboct.obj', '--type=face',
        '--cw_wound=false', '--r1_ax=x', '--r1_ang=0', '--r2_ax=x',
        '--r2_ang=0', '--r3_ax=x', '--r3_ang=0', '--r4_ax=x', '--r4_ang=0',
        '--r5_ax=x', '--r5_ang=0', '--r6_ax=x', '--r6_ang=0', '--scl=100',
        '--f_r=255', '--f_g=0', '--f_b=0', '--f_opac=100', '--s_opac=100',
        '--th=2', '--shade=true', '--lv_x=1', '--lv_y=1', '--lv_z=-2',
        '--show=fce', '--back=false', '--z_sort=max')]
    compare_filters = [CompareOrderIndependentStyle()]
