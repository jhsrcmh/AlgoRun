#!/usr/bin/python 
#encoding=utf-8

'''
Authored by jhsrcmh in NCI

-----------------------------

  <strong> Wolf's MIS</strong>
-----------------------------

'''

import unittest
import codecs
from suffix_tree import SuffixTree


class SuffixTreeTest(unittest.TestCase):
    def test_empty_string(self):
        st = SuffixTree('')
        self.assertEqual(st.find_substring('not there'), -1)
        self.assertEqual(st.find_substring(''), -1)
        self.assertFalse(st.has_substring('not there'))
        self.assertFalse(st.has_substring(''))
        
    def test_repeated_string(self):
        st = SuffixTree("aaa")
        self.assertEqual(st.find_substring('a'), 0)
        self.assertEqual(st.find_substring('aa'), 0)
        self.assertEqual(st.find_substring('aaa'), 0)
        self.assertEqual(st.find_substring('b'), -1)
        self.assertTrue(st.has_substring('a'))
        self.assertTrue(st.has_substring('aa'))
        self.assertTrue(st.has_substring('aaa'))

    def test_text_string(self):
	f = codecs.open("test.txt", encoding='utf-8')
	st = SuffixTree(f.read())
	self.assertTrue(st.has_substring(u'谢'))

    def test_chinese_string(self):
	st = SuffixTree(u"才高八斗")
	self.assertTrue(st.has_substring(u'高'))
	self.assertFalse(st.has_substring(u'豆豆'))

    def test_chinese_text(self):
	
	st = SuffixTree(codecs.open("test.txt", encoding="utf-8").read())
	self.assertTrue(st.find_substring(u'概括性总结'))
if __name__ == '__main__':
    unittest.main()

