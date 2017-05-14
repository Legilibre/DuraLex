# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseHeader3ReferenceTest(DuralexTestCase):
    def test_header3(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header3_reference,
                "au e"
            ),
            {'children':[
                {
                    'type': u'header3-reference',
                    'order': 5
                }
            ]}
        )

    def test_before_header3(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header3_reference,
                "avant le d"
            ),
            {'children':[
                {
                    'type': u'header3-reference',
                    'position': u'before',
                    'order': 4
                }
            ]}
        )

    def test_header3_header2_article_code(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header3_reference,
                "le b du 3° de l'article L. 711-2 du code de l'éducation"
            ),
            {'children': [
                {
                    'order': 2,
                    'type': u'header3-reference',
                    'children': [
                        {
                            'order': 3,
                            'type': u'header2-reference',
                            'children': [
                                {
                                    'children': [
                                        {
                                            'id': u'code de l\'éducation',
                                            'type': u'code-reference'
                                        }
                                    ],
                                    'id': u'L. 711-2',
                                    'type': u'article-reference'
                                }
                            ],
                        }
                    ]
                }
            ]}
        )
