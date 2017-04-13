# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseWordsReferenceTest(DuralexTestCase):
    def test_single_word(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_words_reference,
                u"le mot : \"test\""
            ),
            {'children':[
                {
                    'type': u'words-reference',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'test'
                        }
                    ]
                }
            ]}
        )

    def test_words(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_words_reference,
                u"les mots : \"ceci est un test\""
            ),
            {'children':[
                {
                    'type': u'words-reference',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est un test'
                        }
                    ]
                }
            ]}
        )

    def test_reference(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_words_reference,
                u"la référence : \"L. 321-5\""
            ),
            {'children':[
                {
                    'type': u'words-reference',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'L. 321-5'
                        }
                    ]
                }
            ]}
        )

    def test_after_words(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_words_reference,
                u"après les mots : \"ceci est un test\""
            ),
            {'children':[
                {
                    'type': u'words-reference',
                    'position': u'after',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est un test'
                        }
                    ]
                }
            ]}
        )
