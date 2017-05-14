# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseWordReferenceTest(DuralexTestCase):
    def test_single_word(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_word_reference,
                u"le mot : \"test\""
            ),
            {'children':[
                {
                    'type': u'word-reference',
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
                parser.parse_word_reference,
                u"les mots : \"ceci est un test\""
            ),
            {'children':[
                {
                    'type': u'word-reference',
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
                parser.parse_word_reference,
                u"la référence : \"L. 321-5\""
            ),
            {'children':[
                {
                    'type': u'word-reference',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'L. 321-5'
                        }
                    ]
                }
            ]}
        )

    def test_references(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_word_reference,
                u"les références : \"ceci est un test\""
            ),
            {'children':[
                {
                    'type': u'word-reference',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est un test'
                        }
                    ]
                }
            ]}
        )

    def test_after_words(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_word_reference,
                u"après les mots : \"ceci est un test\""
            ),
            {'children':[
                {
                    'type': u'word-reference',
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

    def test_words_reference_position_in_article(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_word_reference,
                u"après les mots : \"aux dispositions de l'article L. 123-5\", la fin de l'article L. 112-3 du code de la recherche"
            ),
            {'children':[
                {
                    'type': u'word-reference',
                    'position': u'after',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'aux dispositions de l\'article L. 123-5'
                        },
                        {
                            'type': u'article-reference',
                            'position': u'end',
                            'id': u'L. 112-3',
                            'children': [
                                {
                                    'type': u'code-reference',
                                    'id': u'code de la recherche'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_alinea_ref_word_ref(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_reference,
                u"au deuxième alinéa, le mot : \"test\""
            ),
            {'children':[
                {
                    'type': u'alinea-reference',
                    'order': 2,
                    'children': [
                        {
                            'type': u'word-reference',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'test'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_alinea_ref_article_ref_word_ref(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_reference,
                u"au deuxième alinéa de l'article L. 42, le mot : \"test\""
            ),
            {'children':[
                {
                    'type': u'alinea-reference',
                    'order': 2,
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'L. 42',
                            'children': [
                                {
                                    'type': u'word-reference',
                                    'children': [
                                        {
                                            'type': u'quote',
                                            'words': u'test'
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_alinea_ref_article_ref_law_ref_word_ref(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_reference,
                u"au deuxième alinéa de l'article L. 42 de la loi n° 77-729, le mot : \"test\""
            ),
            {'children':[
                {
                    'type': u'alinea-reference',
                    'order': 2,
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'L. 42',
                            'children': [
                                {
                                    'type': u'law-reference',
                                    'id': u'77-729',
                                    'children': [
                                        {
                                            'type': u'word-reference',
                                            'children': [
                                                {
                                                    'type': u'quote',
                                                    'words': u'test'
                                                }
                                            ]
                                        }
                                    ]

                                }
                            ]
                        }
                    ]
                }
            ]}
        )
