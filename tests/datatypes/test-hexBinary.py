# -*- coding: utf-8 -*-
import logging
if __name__ == '__main__':
    logging.basicConfig()
_log = logging.getLogger(__name__)
from pyxb.exceptions_ import *
import unittest
import pyxb.binding.datatypes as xsd
import binascii

class Test_hexBinary (unittest.TestCase):
    def testValues (self):
        data_values = [ '\x01', '\x00', '\x01\x23', '\x12\x34' ]
        for dt in data_values:
            dd = dt.encode('utf-8')
            v = xsd.hexBinary(dd)
            self.assertEqual(v, dd)

    def testStrings (self):
        encoded_values = [ u'01', u'00', u'ab', u'Ab', u'AB12' ]
        for et in encoded_values:
            ed = et.encode('utf-8')
            v = xsd.hexBinary.Factory(ed)
            self.assertEqual(v, ed)
            v = xsd.hexBinary.Factory(et, _from_xml=True)
            self.assertEqual(len(et)//2, len(v))
            self.assertEqual(et.upper(), v.xsdLiteral())

    def testBadStrings (self):
        self.assertRaises(SimpleTypeValueError, xsd.hexBinary.Factory, u'0', _from_xml=True)
        self.assertRaises(SimpleTypeValueError, xsd.hexBinary.Factory, u'012', _from_xml=True)
        self.assertRaises(SimpleTypeValueError, xsd.hexBinary.Factory, u'01s', _from_xml=True)
        self.assertRaises(SimpleTypeValueError, xsd.hexBinary.Factory, u'sb', _from_xml=True)

    def testLiteralization (self):
        self.assertEqual('', xsd.hexBinary(''.encode('utf-8')).xsdLiteral())


if __name__ == '__main__':
    unittest.main()
