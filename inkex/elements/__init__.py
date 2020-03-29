"""
Element based interface provides the bulk of features that allow you to
interact directly with the SVG xml interface.

See the documentation for each of the elements for details on how it works.
"""

from .primitives import SVG_PARSER, load_svg, ShapeElement, BaseElement
from .svg import SvgDocumentElement
from .groups import Group, Layer, Anchor, Marker, ClipPath
from .polygons import PathElement, Polyline, Polygon, Line, Rectangle, Circle, Ellipse
from .text import FlowRegion, FlowRoot, FlowPara, FlowDiv, FlowSpan, TextElement, \
    TextPath, Tspan, SVGfont, FontFace, Glyph, MissingGlyph
from .use import Symbol, Use
from .meta import Defs, StyleElement, Script, Desc, Title, NamedView, Guide, \
    Metadata, ForeignObject, Switch, Grid
from .filters import Filter, Pattern, Gradient, LinearGradient, RadialGradient, PathEffect
from .image import Image
