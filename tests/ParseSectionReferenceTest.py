# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseSectionReferenceTest(DuralexTestCase):
    def test_the_section_order(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_section_reference,
                "la section 2"
            ),
            {'children':[
                {
                    'type': u'section-reference',
                    'order': 2
                }
            ]}
        )

    def test_of_the_section_order(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_section_reference,
                "de la section 2"
            ),
            {'children':[
                {
                    'type': u'section-reference',
                    'order': 2
                }
            ]}
        )
