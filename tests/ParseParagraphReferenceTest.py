# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseParagraphReferenceTest(DuralexTestCase):
    def test_paragraph(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_paragraph_reference,
                u"le paragraphe 42"
            ),
            {'children': [
                {
                    'type': u'paragraph-reference',
                    'order': 42
                }
            ]}
        )

    def test_paragraph_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_paragraph_reference,
                u"du paragraphe 42"
            ),
            {'children': [
                {
                    'type': u'paragraph-reference',
                    'order': 42
                }
            ]}
        )
