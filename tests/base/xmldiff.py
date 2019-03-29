#
# Copyright 2011 (c) Ian Bicking <ianb@colorstudy.com>
#           2019 (c) Martin Owens <doctormo@gmail.com>
#
# Taken from http://formencode.org under the GPL compatible PSF License.
# Modified to produce more output as a diff.
#
"""
Allow two xml files/lxml etrees to be compared, returning their differences.
"""

def text_compare(t1, t2):
    """
    Compare two text strings while allowing for '*' to match
    anything on either lhs or rhs.
    """
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()


def xmldiff(x1, x2):
    clean = True
    #if reporter is None:
    #    reporter = print_reporter
    if x1.tag != x2.tag:
        x1.tag = '{}XXX{}'.format(x1.tag, x2.tag)
        clean = False
        #reporter('Tags do not match: %s and %s' % (x1.tag, x2.tag))
    for name, value in x1.attrib.items():
        if name not in x2.attrib:
            x1.attrib[name] += "XXX"
            clean = False
        elif x2.attrib.get(name) != value:
            x1.attrib[name] = "{}XXX{}".format(x1.attrib.get(name), x2.attrib.get(name))
            clean = False
            #return reporter('Attributes do not match: %s=%r, %s=%r'
            #             % (name, value, name, x2.attrib.get(name)))
    for name, value in x2.attrib.items():
        if name not in x1.attrib:
            x1.attrib[name] = "XXX" + value
            clean = False
            #return reporter('x2 has an attribute x1 is missing: %s'
            #             % name)
    if not text_compare(x1.text, x2.text):
        x1.text = "{}XXX{}".format(x1.text, x2.text)
        clean = False
        #return reporter('text: %r != %r' % (x1.text, x2.text))
    if not text_compare(x1.tail, x2.tail):
        x1.tail = "{}XXX{}".format(x1.tail, x2.tail)
        clean = False
        #return reporter('tail: %r != %r' % (x1.tail, x2.tail))

    # Get children and pad with nulls
    children_a = list(x1)
    children_b = list(x2)
    children_a += [None] * (len(children_a) - len(children_b))
    children_b += [None] * (len(children_b) - len(children_a))

    for child_a, child_b in zip(children_a, children_b):
        if child_a is None: # child_b exists
            child_c = child_b.clone()
            child_c.tag = 'XXX' + child_c.tag
            x1.append(child_c)
            clean = False
        elif child_b is None: # child_a exists
            child_a.tag += 'XXX'
            clean = False
        else:
            clean = xmldiff(child_a, child_b) and clean
    return clean

if __name__ == '__main__':
    import sys
    import xml.etree.ElementTree as xml
    XMLA = xml.parse(sys.argv[1])
    XMLB = xml.parse(sys.argv[2])
    xmldiff(XMLA.getroot(), XMLB.getroot())
    print(xml.tostring(XMLA.getroot()).decode('utf-8'))
