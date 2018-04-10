#
# Copyright (C) 2018 Martin Owens
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110, USA.
#
"""
Any mocking utilities required by testing. Mocking is when you need the test
to exercise a piece of code, but that code may or does call on something
outside of the target code that either takes too long to run, isn't available
during the test running process or simply shouldn't be running at all.
"""

def replace_function(owner, name, new=None):
    """Replace the named function with the new function for mocking"""
    def _outer(caller):
        def _inner(*args, **kwargs):
            try:
                old = getattr(owner, name)
                if isinstance(new, Exception):
                    def _error_function(*args2, **kw2): # pylint: disable=unused-argument
                        raise type(new)(new.message.format(*args, **kwargs))
                    setattr(owner, name, _error_function)
                elif new is None or isinstance(new, (str, int, float, list, tuple)):
                    def _empty_function(*args, **kw): # pylint: disable=unused-argument
                        return new
                    setattr(owner, name, _empty_function)
                else:
                    setattr(owner, name, new)
                result = caller(*args, **kwargs)
            finally:
                setattr(owner, name, old)
            return result
        _inner.__name__ = '{}_replaced'.format(caller.__name__)
        return _inner
    return _outer
