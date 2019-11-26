# coding=utf-8
import os
import tarfile
from guillotine import Guillotine
from inkex.tester import ComparisonMixin, TestCase

class TestGuillotineBasic(ComparisonMixin, TestCase):
    """Test the Guillotine extension"""
    effect_class = Guillotine
    compare_file = 'svg/guides.svg'
    comparisons = [
        ('--image=f{}oo',),
        ('--ignore=true',),
    ]

    def test_all_comparisons(self):
        """Images are extracted to a file directory"""
        for args in self.comparisons:
            # Create a landing directory for generated images
            outdir = os.path.join(self.tempdir, 'img')
            args += ('--directory={}/'.format(outdir),)

            # But also set this directory into the compare file
            compare_file = os.path.join(self.tempdir, 'compare_file.svg')
            with open(self.data_file(self.compare_file), 'rb') as rhl:
                with open(compare_file, 'wb') as whl:
                    whl.write(rhl.read().replace(b'{tempdir}', outdir.encode('utf8')))

            self.assertEffect(compare_file, args=args)
            self.assertTrue(os.path.isdir(outdir))

            # We make a tar archive so we can test it.
            tarname = os.path.join(self.tempdir, 'img.tar')
            tar = tarfile.open(tarname, 'w|')

            for name in sorted(os.listdir(outdir)):
                with open(os.path.join(outdir, name), 'rb') as fhl:
                    fhl.seek(0, 2)
                    info = tarfile.TarInfo(name)
                    info.size = fhl.tell()
                    fhl.seek(0)
                    tar.addfile(info, fhl)
            tar.close()

            with open(tarname, 'rb') as fhl:
                data_a = fhl.read()

            outfile = self.get_compare_outfile(args)
            if os.environ.get('EXPORT_COMPARE', False):
                # This copy is because of cross-device link error
                with open(tarname, 'rb') as rhl:
                    with open(outfile + '.export', 'wb') as whl:
                        whl.write(rhl.read())
                print("Written output: {}.export".format(outfile))

            with open(outfile, 'rb') as fhl:
                self.assertEqual(data_a, fhl.read())
