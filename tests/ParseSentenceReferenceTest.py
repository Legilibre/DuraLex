# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseSentenceReferenceTest(DuralexTestCase):
    def test_position_sentence(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_sentence_reference,
                u"la première phrase"
            ),
            {'children':[
                {
                    'type': u'sentence-reference',
                    'order': 1
                }
            ]}
        )

    def test_position_sentence_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_sentence_reference,
                u"à la première phrase"
            ),
            {'children':[
                {
                    'type': u'sentence-reference',
                    'order': 1
                }
            ]}
        )

    def test_position_sentence_article_id_code_name(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_sentence_reference,
                u"la première phrase de l'article L. 114-5"
            ),
            {'children':[
                {
                    'type': u'sentence-reference',
                    'order': 1,
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'L. 114-5'
                        }
                    ]
                }
            ]}
        )

    def test_position_sentence_article_id_code_name(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_sentence_reference,
                u"la première phrase de l'article L. 114-5 du code de la recherche"
            ),
            {'children':[
                {
                    'type': u'sentence-reference',
                    'order': 1,
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'L. 114-5',
                            'children': [
                                {
                                    'type': u'code-reference',
                                    'codeName': u'code de la recherche'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )
