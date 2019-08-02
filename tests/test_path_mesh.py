# coding=utf-8

from path_mesh_m2p import MeshToPath
from path_mesh_p2m import PathToMesh

from inkex.tester import ComparisonMixin, TestCase

class PathToMeshTest(ComparisonMixin, TestCase):
    """Test path to mesh with comparisons"""
    effect_class = PathToMesh
    comparisons = [('--id=path1', '--id=path9'),]
    compare_file = 'svg/mesh.svg'
