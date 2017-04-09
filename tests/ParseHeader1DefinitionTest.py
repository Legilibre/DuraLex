# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseHeader1DefinitionTest(DuralexTestCase):
    def test_header1(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header1_definition,
                ("un I")
            ),
            {'children': [
                {
                    'type': u'header1',
                    'order': 1
                }
            ]}
        )

    def test_header1_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header1_definition,
                ("un IV")
            ),
            {'children': [
                {
                    'type': u'header1',
                    'order': 4
                }
            ]}
        )

    def test_header1_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header1_definition,
                ("un III ainsi rédigé :\n"
                "\"ceci est le contenu du header1\"")
            ),
            {'children': [
                {
                    'type': u'header1',
                    'order': 3,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du header1'
                        }
                    ],
                }
            ]}
        )
