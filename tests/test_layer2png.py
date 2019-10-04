from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

from layer2png import ExportSlices

class Layer2PNGTest(#ComparisonMixin,
                    InkscapeExtensionTestMixin, TestCase):
    
    effect_class = ExportSlices
    compare_file = 'svg/slicer.svg'

    def test_get_layers(self):
        basic_svg = self.data_file('svg', 'slicer.svg')
        args = [basic_svg, '-l' 'slices']
        self.effect = Layer2PNGTest.effect_class()
        self.effect.options = self.effect.arg_parser.parse_args(args)
        self.effect.options.input_file = basic_svg
        self.effect.load_raw()
        nodes = self.effect.get_layer_nodes('slices')
        assert len(nodes) == 1
        assert nodes[0].tag == '{http://www.w3.org/2000/svg}rect'


    def test_bad_slice_layer(self):
        basic_svg = self.data_file('svg', 'slicer.svg')
        args = [basic_svg, '-l' 'slices']
        self.effect = Layer2PNGTest.effect_class()
        self.effect.options = self.effect.arg_parser.parse_args(args)
        self.effect.options.input_file = basic_svg
        self.effect.load_raw()
        nodes = self.effect.get_layer_nodes('badslices')
        assert nodes is None


    def test_color(self):
        basic_svg = self.data_file('svg', 'slicer.svg')
        args = [basic_svg, '-l' 'slices']
        self.effect = Layer2PNGTest.effect_class()
        self.effect.options = self.effect.arg_parser.parse_args(args)
        self.effect.options.input_file = basic_svg
        self.effect.load_raw()
        nodes = self.effect.get_layer_nodes('slices')
        color, kwargs = self.effect.get_color_and_command_kwargs(nodes[0])
        assert color == self.effect.GREEN
        assert kwargs['export-id'] == 'slice1'

