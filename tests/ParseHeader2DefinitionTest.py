# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseHeader2DefinitionTest(DuralexTestCase):
    def test_header2_order_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header2_definition,
                "un 1° ainsi rédigé : \n\"ceci est un test\""
            ),
            {'children': [
                {
                    'type': u'header2-definition',
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

    def test_header2_ellipsis_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header2_definition,
                "un ... ° ainsi rédigé : \n\"ceci est un test\""
            ),
            {'children': [
                {
                    'type': u'header2-definition',
                    'order': '...',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est un test'
                        }
                    ],
                }
            ]}
        )

    def test_header2_order_suborder(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header2_definition,
                "un 1° A bis"
            ),
            {'children': [
                {
                    'type': u'header2-definition',
                    'order': 1,
                    'isBis': True,
                    'subOrder': 'A'
                }
            ]}
        )

    def test_scope_with_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header2_definition,
                (u"des 5° à 8° ainsi rédigés :\n"
                u"\"ceci est le contenu du header2 5\"\n"
                u"\"ceci est le contenu du header2 6\"\n"
                u"\"ceci est le contenu du header2 7\"\n"
                u"\"ceci est le contenu du header2 8\"")
            ),
            {'children': [
                {
                    'type': u'header2-definition',
                    'order': 5,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du header2 5'
                        }
                    ],
                },
                {
                    'type': u'header2-definition',
                    'order': 6,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du header2 6'
                        }
                    ],
                },
                {
                    'type': u'header2-definition',
                    'order': 7,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du header2 7'
                        }
                    ],
                },
                {
                    'type': u'header2-definition',
                    'order': 8,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du header2 8'
                        }
                    ],
                },
            ]}
        )
