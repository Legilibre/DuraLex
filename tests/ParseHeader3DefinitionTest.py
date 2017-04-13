# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseHeader3DefinitionTest(DuralexTestCase):
    def test_header3(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header3_definition,
                ("un a")
            ),
            {'children': [
                {
                    'type': u'header3',
                    'order': 1
                }
            ]}
        )

    def test_header3_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header3_definition,
                ("un e")
            ),
            {'children': [
                {
                    'type': u'header3',
                    'order': 5
                }
            ]}
        )

    def test_scope_with_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header3_definition,
                (u"des c à e ainsi rédigés :\n"
                u"\"ceci est le contenu du header3 3\"\n"
                u"\"ceci est le contenu du header3 4\"\n"
                u"\"ceci est le contenu du header3 5\"")
            ),
            {'children': [
                {
                    'type': u'header3',
                    'order': 3,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du header3 3'
                        }
                    ],
                },
                {
                    'type': u'header3',
                    'order': 4,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du header3 4'
                        }
                    ],
                },
                {
                    'type': u'header3',
                    'order': 5,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du header3 5'
                        }
                    ],
                }
            ]}
        )
