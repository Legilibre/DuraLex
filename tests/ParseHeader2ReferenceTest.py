# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseHeader2ReferenceTest(DuralexTestCase):
    def test_header2_number(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header2_reference,
                "au 42°"
            ),
            {'children':[
                {
                    'type': u'header2-reference',
                    'order': 42
                }
            ]}
        )

    def test_before_header2_number(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header2_reference,
                "avant le 1°"
            ),
            {'children':[
                {
                    'type': u'header2-reference',
                    'position': u'before',
                    'order': 1
                }
            ]}
        )

    def test_header2_order_letter_adverb_article_code(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header2_reference,
                "le 3° de l'article L. 711-2 du code de l'éducation"
            ),
            {'children': [
                {
                    'order': 3,
                    'type': u'header2-reference',
                    'children': [
                        {
                            'children': [
                                {
                                    'codeName': u'code de l\'éducation',
                                    'type': u'code-reference'
                                }
                            ],
                            'id': u'L. 711-2',
                            'type': u'article-reference'
                        }
                    ],
                }
            ]}
        )
