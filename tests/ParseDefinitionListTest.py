# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseDefinitionListTest(DuralexTestCase):
    def test_n_sentences_and_n_alineas_with_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_definition_list,
                (u"cinq phrases et cinq alinéas ainsi rédigés : \n"
                u"\"alinéa 1\"\n"
                u"\"alinéa 2\"\n"
                u"\"alinéa 3\"\n"
                u"\"alinéa 4\"\n"
                u"\"alinéa 5\"\n")
            ),
            {'children': [
                {
                    'count': 5,
                    'type': u'sentence'
                },
                {
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 1'
                        }
                    ],
                    'type': u'alinea'
                },
                {
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 2'
                        }
                    ],
                    'type': u'alinea'
                },
                {
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 3'
                        }
                    ],
                    'type': u'alinea'
                },
                {
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 4'
                        }
                    ],
                    'type': u'alinea'
                },
                {
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 5'
                        }
                    ],
                    'type': u'alinea'
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
                    'type': u'header1',
                    'order': 3,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du premier header1'
                        }
                    ],
                },
                {
                    'type': u'header1',
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
                    'type': u'header2',
                    'order': 2,
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le contenu du premier header2'
                        }
                    ],
                },
                {
                    'type': u'header2',
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
                (u"trois alinéas ainsi rédigés : \n"
                u"\"alinéa 1\"\n"
                u"\"alinéa 2\"\n"
                u"\"alinéa 3\"")
            ),
            {'children': [
                {
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 1'
                        }
                    ],
                    'type': u'alinea'
                },
                {
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 2'
                        }
                    ],
                    'type': u'alinea'
                },
                {
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'alinéa 3'
                        }
                    ],
                    'type': u'alinea'
                }
            ]}
        )
