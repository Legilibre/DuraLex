# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseAlineaDefinitionTest(DuralexTestCase):
    def test_one_alinea_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_definition,
                ("un alinéa ainsi rédigé : \n"
                "\"alinéa 1\"")
            ),
            {'children': [
                {
                    'type': u'alinea',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 1'
                        }
                    ],
                }
            ]}
        )

    def test_n_alineas_with_n_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_alinea_definition,
                ("quatre alinéas ainsi rédigés : \n"
                "\"alinéa 1\"\n"
                "\"alinéa 2\"\n"
                "\"alinéa 3\"\n"
                "\"alinéa 4\"")
            ),
            {'children': [
                {
                    'type': u'alinea',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 1'
                        }
                    ],
                },
                {
                    'type': u'alinea',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 2'
                        }
                    ],
                },
                {
                    'type': u'alinea',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 3'
                        }
                    ],
                },
                {
                    'type': u'alinea',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 4'
                        }
                    ],
                }
            ]}
        )
