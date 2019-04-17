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

def text_compare(test1, test2):
    """
    Compare two text strings while allowing for '*' to match
    anything on either lhs or rhs.
    """
    if not test1 and not test2:
        return True
    if test1 == '*' or test2 == '*':
        return True
    return (test1 or '').strip() == (test2 or '').strip()


def xmldiff(xml1, xml2):
    """Create an xml difference, will modify the first xml structure with a diff"""
    clean = True
    #if reporter is None:
    #    reporter = print_reporter
    if xml1.tag != xml2.tag:
        xml1.tag = '{}XXX{}'.format(xml1.tag, xml2.tag)
        clean = False
        #reporter('Tags do not match: %s and %s' % (xml1.tag, xml2.tag))
    for name, value in xml1.attrib.items():
        if name not in xml2.attrib:
            xml1.attrib[name] += "XXX"
            clean = False
        elif xml2.attrib.get(name) != value:
            xml1.attrib[name] = "{}XXX{}".format(xml1.attrib.get(name), xml2.attrib.get(name))
            clean = False
            #return reporter('Attributes do not match: %s=%r, %s=%r'
            #             % (name, value, name, xml2.attrib.get(name)))
    for name, value in xml2.attrib.items():
        if name not in xml1.attrib:
            xml1.attrib[name] = "XXX" + value
            clean = False
            #return reporter('xml2 has an attribute xml1 is missing: %s'
            #             % name)
    if not text_compare(xml1.text, xml2.text):
        xml1.text = "{}XXX{}".format(xml1.text, xml2.text)
        clean = False
        #return reporter('text: %r != %r' % (xml1.text, xml2.text))
    if not text_compare(xml1.tail, xml2.tail):
        xml1.tail = "{}XXX{}".format(xml1.tail, xml2.tail)
        clean = False
        #return reporter('tail: %r != %r' % (xml1.tail, xml2.tail))

    # Get children and pad with nulls
    children_a = list(xml1)
    children_b = list(xml2)
    children_a += [None] * (len(children_a) - len(children_b))
    children_b += [None] * (len(children_b) - len(children_a))

    for child_a, child_b in zip(children_a, children_b):
        if child_a is None: # child_b exists
            child_c = child_b.clone()
            child_c.tag = 'XXX' + child_c.tag
            xml1.append(child_c)
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
