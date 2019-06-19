import pytest
from inkex.command import is_inkscape_available

requires_inkscape = pytest.mark.skipif(not is_inkscape_available(),
                                       reason="Test requires inkscape, but it's not available")