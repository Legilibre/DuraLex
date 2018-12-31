# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase, main

import duralex.alinea_parser as parser

class ParseDefinitionListTest(DuralexTestCase):
    def test_n_sentences_and_n_alineas_with_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_definition_list,
                ("cinq phrases et cinq alinéas ainsi rédigés : \n"
                "\"alinéa 1\"\n"
                "\"alinéa 2\"\n"
                "\"alinéa 3\"\n"
                "\"alinéa 4\"\n"
                "\"alinéa 5\"\n")
            ),
            {'children': [
                {
                    'type': 'sentence-definition',
                    'count': 5
                },
                {
                    'type': 'alinea-definition',
                    'count': 5,
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
                        },
                        {
                            'type': 'quote',
                            'words': 'alinéa 5'
                        }
                    ]
                }
            ]}
        )

    def test_n_header1_with_n_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_definition_list,
                ("un III et un IV ainsi rédigés :\n"
                "\"ceci est le contenu du premier header1\"\n"
                "\"ceci est le contenu du second header1\"")
            ),
            {'children': [
                {
                    'type': u'header1-definition',
                    'order': 3,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du premier header1'
                        }
                    ],
                },
                {
                    'type': u'header1-definition',
                    'order': 4,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du second header1'
                        }
                    ],
                }
            ]}
        )

    def test_n_header2_with_n_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_definition_list,
                ("un 2° et un 3° ainsi rédigés :\n"
                "\"ceci est le contenu du premier header2\"\n"
                "\"ceci est le contenu du second header2\"")
            ),
            {'children': [
                {
                    'type': u'header2-definition',
                    'order': 2,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du premier header2'
                        }
                    ],
                },
                {
                    'type': u'header2-definition',
                    'order': 3,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du second header2'
                        }
                    ],
                }
            ]}
        )

    def test_n_alineas_with_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_definition_list,
                ("trois alinéas ainsi rédigés : \n"
                "\"alinéa 1\"\n"
                "\"alinéa 2\"\n"
                "\"alinéa 3\"")
            ),
            {'children': [
                {
                    'type': 'alinea-definition',
                    'count': 3,
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
                        }
                    ],
                }
            ]}
        )

if __name__ == '__main__':
    main()

# vim: set ts=4 sw=4 sts=4 et:
