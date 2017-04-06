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
