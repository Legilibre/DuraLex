# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseMultiplicativeAdverbTest(DuralexTestCase):
    def test_header2_bis(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header2_definition,
                "un 3° bis"
            ),
            {'children':[
                {
                    'type': u'header2',
                    'order': 3,
                    'isBis': True
                }
            ]}
        )

    def test_header2_ter(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header2_definition,
                "un 3° ter"
            ),
            {'children':[
                {
                    'type': u'header2',
                    'order': 3,
                    'isTer': True
                }
            ]}
        )

    def test_header2_quater(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header2_definition,
                "un 3° quater"
            ),
            {'children':[
                {
                    'type': u'header2',
                    'order': 3,
                    'isQuater': True
                }
            ]}
        )
