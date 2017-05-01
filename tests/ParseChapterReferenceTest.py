# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseChapterReferenceTest(DuralexTestCase):
    def test_chapter(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_chapter_reference,
                u"le chapitre IV"
            ),
            {'children': [
                {
                    'type': u'chapter-reference',
                    'order': 4
                }
            ]}
        )

    def test_chapter_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_chapter_reference,
                u"du chapitre IV"
            ),
            {'children': [
                {
                    'type': u'chapter-reference',
                    'order': 4
                }
            ]}
        )
