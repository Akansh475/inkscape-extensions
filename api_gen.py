"""
Generate list of direct API
"""

import textwrap
import types
import inspect
import inkex

output = open('api.md', 'w')

def get_mod(attr_name):
    """Return the module name for any attribute"""
    try:
        return getattr(inkex, attr_name).__module__
    except AttributeError:
        return '?'

for name in sorted(dir(inkex), key=get_mod):
    mod = get_mod(name)

    # skip private and builtin names
    if name.startswith('_'):
        continue

    value = getattr(inkex, name)

    # skip modules
    if isinstance(value, types.ModuleType):
        continue

    modname = getattr(value, '__module__', '')

    if modname:
        # skip non-inkex items
        if not modname.startswith('inkex'):
            continue
        # skip deprecated API
        if modname == 'inkex.deprecated':
            continue
        # skip private modules
        if modname.startswith('_'):
            continue

    # callable signature
    try:
        sig = inspect.signature(value)
    except: # pylint: disable=bare-except
        sig = ''

    output.write('```\n')
    output.write(f'inkex.{name}{sig}\n')
    print(f"{mod}.{name}{sig}")
    try:
        # don't print the type doc
        if value.__doc__ == type(value).__doc__:
            continue
        output.write(textwrap.indent(textwrap.dedent(value.__doc__), "    "))
        output.write("\n")
    except: # pylint: disable=bare-except
        pass
    finally:
        output.write('```\n')

output.close()
