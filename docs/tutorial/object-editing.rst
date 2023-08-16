Accessing and editing attributes
================================

In inkex, every SVG element is an ``etree.Element`` object. As such, the usual methods
are avaliable for accessing and writing data, in particular 
:func:`~inkex.elements._base.BaseElement.get` and 
:func:`~inkex.elements._base.BaseElement.set` to read and write an arbitrary attribute::

    rectangle.set("width", 10)
    rectangle.get("width") # returns 10

    # sets the label attribute in the Inkscape namespace
    rectangle.set("inkscape:label", "my-rectangle") 
    rectangle.get("inkscape:label") # returns "my-rectangle"

Inkscape hands these values more or less unchanged to the XAML (simplifying the way the 
namespace is specified). The only exception is the `id` attribute: when it is set, 
inkex needs to check whether it is unique in the document.  

For an increasing number of attributes, inkex provides additional functionality for 
reading and editing; they are often Python properties and further described in the API.

In general, **if those attributes return mutable types** (such as ``List`` or ``Dict``, 
or other elements of the document such as an href), any
changes made to them are directly written back into the document tree, you don't need
to set them again.** The notable exception to this rule is 
:attr:`ShapeElement.path <inkex.elements._base.ShapeElement.path>` due to performance 
reasons.

``style``, ``class`` and ``transform``
--------------------------------------

Accessing these attributes returns :attr:`~inkex.styles.Style`, 
:attr:`~inkex.styles.Classes` and :attr:`~inkex.transforms.Transform`, respectively,
giving high-level access to them.

All of them are defined in 
:attr:`BaseElement.WRAPPED_ATTRS <inkex.elements._base.BaseElement.WRAPPED_ATTRS>`.

``style``
^^^^^^^^^

For styles, you will want to either query the inline style attribute of an element 
(:attr:`element.style <inkex.elements._base.BaseElement.style>`) or the effective style 
(:attr:`element.specified_style() <inkex.elements._base.BaseElement.specified_style()>`
), taking into
account presentation attributes, parent style, CSS declarations, shorthand attributes 
and ``!important`` styles (and finally, if nothing is found, the default for this 
particular attribute) - i.e. the "final style" the element has in the user agent. 
Both return :class:`~inkex.styles.Style` objects. However, only the changes made
to the first are written back to the document, as we wouldn't know where to write them
(especially if there are ``!important`` styles present in the document, they will
override changes made even to the element's inline style!)

Styles have a :func:`~inkex.styles.Style.__call__` override that returns a parsed value.
If this value is a mutable datatype, changing it will immediately permeate back to the
document. Examples::

    _ = el.style("fill") # returns inkex.Color value (solid fill)

    # Attaches the linear gradient to the document's defs, and sets the id as href 
    # on the fill
    el.style["fill"] = inkex.LinearGradient.new(inkex.Stop.new(...))

    # Query the elements style: either using __getitem__ or __call__
    el.style["fill"] # returns "url(#linearGradient572)"
    grad = el.style("fill")  # returns LinearGradient instance

    # Modify the underlying gradient 
    grad.add(inkex.Stop.new(...))

    # The changes go back into the document
    len(el.style("fill"))  # returns 2

    # For filters, we accept single filters or a list for writing:
    el.style["filter"] = "url(#filter123)"
    # but reading the parsed value always returns a list
    el.style("filter")  # returns [Filter instance], or [] if #filter123 doesn't exist

    # Modifying this list modifies the document
    second = inkex.Filter.new(inkex.Filter.GaussianBlur.new(stdDeviation=1))
    el.style("filter").append(second)

    el.style("filter")  # returns a list of 2 filters 
    el.style("filter").clear()
    el.style("filter")  # returns []

The parsed value is a best-faith interpretation of the value. If the value references
other elements in the document, they are returned. Percentage values are returned as
float, opacity values clipped between 0 and 1, values with unit are converted to user
units, `currentColor` is replaced with the actual color, enum values are validated and 
so on. If a string is returned for a particular attribute, a parsed version may be added
in a future major version.

``transform``
^^^^^^^^^^^^^

``:attr:`element.transform <inkex.elements._base.BaseElement.transform>`.`` is also mutable through its public methods, 
like :func:`~inkex.element.transform.add_matrix`, 
:func:`~inkex.element.transform.add_translate`, and its operators, e.g.::
    
    element.transform @= inkex.Transform(scale=2)

which directly updates the ``transform`` attribute of ``element``.






