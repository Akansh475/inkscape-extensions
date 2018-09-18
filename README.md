# Inkscape Extensions

This folder contains the stock Inkscape extensions, i.e. the scripts that
implement some commands that you can use from within Inkscape. Most of
these commands are in the Extensions menu.

## Installation

These scripts should be installed with an Inkscape package already (if you have 
installed Inkscape). For packagers or people testing newer releases, you can 
install the files into /usr/share/inkscape/extensions or 
~/.config/inkscape/extensions .

## Testing

These extensions are designed to have good test coverage as well as python 2.7 
and python 3.5 support.  
Testing can be run using the setup.py command:

    python3 setup.py test

## Extension description

Each *.inx file describes an extension, listing its name, purpose,
prerequisites, location within the menu, etc. These files are read by
Inkscape on launch. Other files are the scripts themselves (Perl,
Python, and Ruby are supported, as well as shell scripts).

## Building Docs

You may wish to compile to docs for use outside of the Inkscape docs, this can 
be done with these commands:

    sphinx-apidoc -F -o source inkex
    ./setup.py build_sphinx -s source
    firefox ./build/sphinx/html/inkex.html

All documentation should be included INSIDE of each python module.

## License Requirements

Only include extensions here which are GPL-compatible.  This includes
Apache-2, MPL 1.1, certain Creative Commons licenses, and more.  See
https://www.gnu.org/licenses/license-list.html for guidance.
