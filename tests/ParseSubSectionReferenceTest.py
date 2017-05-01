# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseSubSectionReferenceTest(DuralexTestCase):
    def test_the_subsection_order(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_subsection_reference,
                "la sous-section 2"
            ),
            {'children':[
                {
                    'type': u'subsection-reference',
                    'order': 2
                }
            ]}
        )

    def test_of_the_subsection_order(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_subsection_reference,
                "de la sous-section 2"
            ),
            {'children':[
                {
                    'type': u'subsection-reference',
                    'order': 2
                }
            ]}
        )
