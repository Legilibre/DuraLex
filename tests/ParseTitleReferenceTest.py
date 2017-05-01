# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseTitleReferenceTest(DuralexTestCase):
    def test_title(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_title_reference,
                u"le titre IV"
            ),
            {'children': [
                {
                    'type': u'title-reference',
                    'order': 4
                }
            ]}
        )

    def test_title_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_title_reference,
                u"du titre IV"
            ),
            {'children': [
                {
                    'type': u'title-reference',
                    'order': 4
                }
            ]}
        )
