import pyxb
import pyxb.binding.datatypes as xs
import trac26
import unittest

# By default skip the "tests" which actually emit the exception
# backtrace.  Sometimes though it's good to see those, since they're
# what the user will normally see first.
DisplayException = False
#DisplayException = True

class TestAbstractElementError (unittest.TestCase):
    Good_xmls = '<eCardinals><eConcCardCymru>un</eConcCardCymru><eConcCardEnglish>three</eConcCardEnglish></eCardinals>'

    Bad_xmls = '<eCardinals><eConcCardCymru>un</eConcCardCymru><eAbstractCard>three</eAbstractCard></eCardinals>'

    def testSchemaSupport (self):
        cym1 = trac26.eConcCardCymru('un')
        eng3 = trac26.eConcCardEnglish('three')

        # Incremental through owning element
        instance = trac26.eCardinals()
        self.assertEqual(0, len(instance.eAbstractCard))
        instance.append(cym1)
        self.assertEqual(1, len(instance.eAbstractCard))
        self.assertTrue(isinstance(instance.eAbstractCard[0], trac26.tCardCymru))
        instance.append(eng3)
        self.assertEqual(2, len(instance.eAbstractCard))
        self.assertTrue(isinstance(instance.eAbstractCard[1], trac26.tCardEnglish))
        self.assertTrue(instance.validateBinding())
        xmls = instance.toxml('utf-8', root_only=True)
        self.assertEqual(xmls, self.Good_xmls)

        # Incremental through construtor element
        instance = trac26.eCardinals(cym1, eng3)
        self.assertEqual(2, len(instance.eAbstractCard))
        self.assertTrue(isinstance(instance.eAbstractCard[0], trac26.tCardCymru))
        self.assertTrue(isinstance(instance.eAbstractCard[1], trac26.tCardEnglish))
        self.assertTrue(instance.validateBinding())
        xmls = instance.toxml('utf-8', root_only=True)
        self.assertEqual(xmls, self.Good_xmls)

        # Through parsing
        instance = trac26.CreateFromDocument(self.Good_xmls)
        self.assertEqual(2, len(instance.eAbstractCard))
        self.assertTrue(isinstance(instance.eAbstractCard[0], trac26.tCardCymru))
        self.assertTrue(isinstance(instance.eAbstractCard[1], trac26.tCardEnglish))
        self.assertTrue(instance.validateBinding())

    def testException (self):
        instance = None
        with self.assertRaises(pyxb.AbstractElementError) as cm:
            instance = trac26.eAbstractCard('un')
        e = cm.exception
        self.assertTrue(instance is None)
        self.assertEqual(e.element, trac26.eAbstractCard)
        self.assertEqual(e.value, ('un',))
        self.assertEqual(str(e), 'Cannot instantiate abstract element eAbstractCard directly')

    def testFromDocument (self):
        instance = None
        with self.assertRaises(pyxb.AbstractElementError) as cm:
            instance = trac26.CreateFromDocument(self.Bad_xmls)
        e = cm.exception
        self.assertFalse(e.location is None)
        self.assertEqual(1, e.location.lineNumber)
        self.assertEqual(47, e.location.columnNumber)

    def testDisplayException (self):
        if DisplayException:
            trac26.eAbstractCard('un')

    def testIncremental (self):
        # Without type information, incremental does not work.  The content
        # model fails to recognize it, and it looks like mixed content.
        instance = trac26.eCardinals()
        self.assertEqual(0, len(instance.eAbstractCard))
        self.assertRaises(pyxb.MixedContentError, instance.append, 'un')

class TestAbstractInstantiationError (unittest.TestCase):

    Good_xmls = '<eUseAbstract xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><eAbstract xsi:type="tConcSubCymru"><welsh>un</welsh></eAbstract></eUseAbstract>'

    Bad_xmls = '<eUseAbstract xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><eAbstract><welsh>un</welsh></eAbstract></eUseAbstract>'

    def testSchemaSupport (self):
        cym1 = trac26.tConcSubCymru('un')
        eng3 = trac26.tConcSubEnglish('three')
        # Direct generation works
        instance = trac26.eUseAbstract(cym1)
        # So does from documents with xsi:type
        i2 = trac26.CreateFromDocument(self.Good_xmls)
        self.assertTrue(isinstance(i2.eAbstract, trac26.tConcSubCymru))

    def testException (self):
        scym1 = trac26.tCardCymru('un')
        instance = None
        with self.assertRaises(pyxb.AbstractInstantiationError) as cm:
            instance = trac26.eAbstract(scym1)
        e = cm.exception
        self.assertTrue(instance is None)
        self.assertEqual(str(e), 'Cannot instantiate abstract type tAbstract directly')

    def testFromDocument (self):
        instance = None
        with self.assertRaises(pyxb.AbstractInstantiationError) as cm:
            instance = trac26.CreateFromDocument(self.Bad_xmls)
        e = cm.exception
        self.assertTrue(instance is None)
        # Location within Bad_xmls where error occurred
        self.assertFalse(e.location is None)
        self.assertEqual(1, e.location.lineNumber)
        self.assertEqual(68, e.location.columnNumber)

    def testDisplayException (self):
        if DisplayException:
            scym1 = trac26.tCardCymru('un')
            trac26.eAbstract(scym1)

    def testDisplayExceptionDoc (self):
        if DisplayException:
            instance = trac26.CreateFromDocument(self.Bad_xmls)

if __name__ == '__main__':
    unittest.main()