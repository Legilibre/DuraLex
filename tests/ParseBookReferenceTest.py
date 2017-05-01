# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseBookReferenceTest(DuralexTestCase):
    def test_book(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_book_reference,
                u"le livre III"
            ),
            {'children': [
                {
                    'type': u'book-reference',
                    'order': 3
                }
            ]}
        )

    def test_book_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_book_reference,
                u"du livre V"
            ),
            {'children': [
                {
                    'type': u'book-reference',
                    'order': 5
                }
            ]}
        )
