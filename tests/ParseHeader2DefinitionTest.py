# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseHeader2DefinitionTest(DuralexTestCase):
    def test_header2_number_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header2_definition,
                "un 1° ainsi rédigé : \n\"ceci est un test\""
            ),
            {'children': [
                {
                    'type': u'header2',
                    'order': 1,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est un test'
                        }
                    ],
                }
            ]}
        )
