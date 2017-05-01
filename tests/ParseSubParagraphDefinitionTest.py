# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseSubParagraphDefinitionTest(DuralexTestCase):
    def test_one_subparagraph_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_subparagraph_definition,
                ("un sous-paragraphe ainsi rédigé : \n"
                "\"sous-paragraphe 1\"")
            ),
            {'children': [
                {
                    'type': u'subparagraph',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'sous-paragraphe 1'
                        }
                    ],
                }
            ]}
        )

    def test_one_subparagraph_order_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_subparagraph_definition,
                ("un sous-paragraphe 3 ainsi rédigé : \n"
                "\"sous-paragraphe 1\"")
            ),
            {'children': [
                {
                    'type': u'subparagraph',
                    'order': 3,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'sous-paragraphe 1'
                        }
                    ],
                }
            ]}
        )
