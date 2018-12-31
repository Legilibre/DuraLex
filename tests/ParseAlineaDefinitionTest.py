# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase, main

import duralex.alinea_parser as parser

class ParseAlineaDefinitionTest(DuralexTestCase):
    def test_one_alinea_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_definition,
                ("un alinéa ainsi rédigé : \n"
                "\"alinéa 1\"")
            ),
            {'children': [
                {
                    'type': 'alinea-definition',
                    'count': 1,
                    'children': [
                        {
                            'type': 'quote',
                            'words': 'alinéa 1'
                        }
                    ],
                }
            ]}
        )

    def test_one_alinea_with_french_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_definition,
                ("un alinéa ainsi rédigé : \n"
                "« alinéa 1 »")
            ),
            {'children': [
                {
                    'type': 'alinea-definition',
                    'count': 1,
                    'children': [
                        {
                            'type': 'quote',
                            'words': 'alinéa 1'
                        }
                    ],
                }
            ]}
        )

    def test_n_alineas_with_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_definition,
                ("deux alinéas ainsi rédigés : \n"
                "\"alinéa 1\n"
                "\"alinéa 2\"")
            ),
            {'children': [
                {
                    'type': 'alinea-definition',
                    'count': 2,
                    'children': [
                        {
                            'type': 'quote',
                            'words': 'alinéa 1\nalinéa 2'
                        }
                    ],
                }
            ]}
        )

    def test_n_alineas_with_french_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_definition,
                ("deux alinéas ainsi rédigés : \n"
                "« alinéa 1\n"
                "« alinéa 2 »")
            ),
            {'children': [
                {
                    'type': 'alinea-definition',
                    'count': 2,
                    'children': [
                        {
                            'type': 'quote',
                            'words': 'alinéa 1\nalinéa 2'
                        }
                    ],
                }
            ]}
        )

    def test_n_alineas_with_n_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_definition,
                ("quatre alinéas ainsi rédigés : \n"
                "\"alinéa 1\"\n"
                "\"alinéa 2\"\n"
                "\"alinéa 3\"\n"
                "\"alinéa 4\"")
            ),
            {'children': [
                {
                    'type': 'alinea-definition',
                    'count': 4,
                    'children': [
                        {
                            'type': 'quote',
                            'words': 'alinéa 1'
                        },
                        {
                            'type': 'quote',
                            'words': 'alinéa 2'
                        },
                        {
                            'type': 'quote',
                            'words': 'alinéa 3'
                        },
                        {
                            'type': 'quote',
                            'words': 'alinéa 4'
                        }
                    ],
                }
            ]}
        )

if __name__ == '__main__':
    main()

# vim: set ts=4 sw=4 sts=4 et:
