# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseAlineaReferenceTest(DuralexTestCase):
    def test_alinea(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"l'alinéa"
            ),
            {'children': [
                {
                    'type': u'alinea-reference'
                }
            ]}
        )

    def test_alinea_number(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"alinéa 3"
            ),
            {'children': [
                {
                    'order': 3,
                    'type': u'alinea-reference'
                }
            ]}
        )

    def test_last_alinea(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"du dernier alinéa"
            ),
            {'children': [
                {
                    'order': -1,
                    'type': u'alinea-reference'
                }
            ]}
        )

    def test_last_alinea_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"au dernier alinéa"
            ),
            {'children': [
                {
                    'order': -1,
                    'type': u'alinea-reference'
                }
            ]}
        )

    def test_last_alinea_3(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"le dernier alinéa"
            ),
            {'children': [
                {
                    'order': -1,
                    'type': u'alinea-reference'
                }
            ]}
        )

    def test_before_last_alinea(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"à l'avant dernier alinéa"
            ),
            {'children': [
                {
                    'order': -2,
                    'type': u'alinea-reference'
                }
            ]}
        )

    def test_before_last_alinea_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"l'avant-dernier alinéa"
            ),
            {'children': [
                {
                    'order': -2,
                    'type': u'alinea-reference'
                }
            ]}
        )

    def test_before_last_alinea_3(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"à l'avant-dernier alinéa"
            ),
            {'children': [
                {
                    'order': -2,
                    'type': u'alinea-reference'
                }
            ]}
        )

    def test_number_word_alinea(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"au premier alinéa"
            ),
            {'children': [
                {
                    'order': 1,
                    'type': u'alinea-reference'
                }
            ]}
        )

    def test_number_word_alinea_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"le second alinéa"
            ),
            {'children': [
                {
                    'order': 2,
                    'type': u'alinea-reference'
                }
            ]}
        )

    def test_number_word_alinea_3(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"du troisième alinéa"
            ),
            {'children': [
                {
                    'order': 3,
                    'type': u'alinea-reference'
                }
            ]}
        )

    def test_number_word_alinea_article_id(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"le deuxième alinéa de l'article L. 121-3"
            ),
            {'children': [
                {
                    'order': 2,
                    'type': u'alinea-reference',
                    'children': [
                        {
                            'id': u'L. 121-3',
                            'type': u'article-reference'
                        }
                    ]
                }
            ]}
        )

    def test_number_word_alinea_header1_article_id(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"le premier alinéa du II de l'article L. 121-3"
            ),
            {'children': [
                {
                    'order': 1,
                    'type': u'alinea-reference',
                    'children': [
                        {
                            'order': 2,
                            'type': u'header1-reference',
                            'children': [
                                {
                                    'id': u'L. 121-3',
                                    'type': u'article-reference'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_number_word_alinea_header1_article_id_code(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"le premier alinéa du II de l'article L. 121-3 du code de l'éducation"
            ),
            {'children': [
                {
                    'order': 1,
                    'type': u'alinea-reference',
                    'children': [
                        {
                            'order': 2,
                            'type': u'header1-reference',
                            'children': [
                                {
                                    'id': u'L. 121-3',
                                    'type': u'article-reference',
                                    'children': [
                                        {
                                            'codeName': u'code de l\'éducation',
                                            'type': u'code-reference'
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_the_same_alinea(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"le même alinéa",
                {'children':[
                    {
                        'type': u'alinea-reference',
                        'order': 42
                    }
                ]}
            ),
            {'children':[
                {
                    'type': u'alinea-reference',
                    'order': 42
                },
                {
                    'type': u'alinea-reference',
                    'order': 42
                }
            ]}
        )

    def test_before_the_last_alinea_article_ref(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_reference,
                u"avant le dernier alinéa"
            ),
            {'children':[
                {
                    'type': u'alinea-reference',
                    'position': u'before',
                    'order': -1
                }
            ]}
        )
