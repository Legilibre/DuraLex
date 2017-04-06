# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseDefinitionListTest(DuralexTestCase):
    def test_n_sentences_and_n_alineas_with_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_definition_list,
                "cinq phrases et cinq alinéas ainsi rédigés : \n\"alinéa 1\"\n\"alinéa 2\"\n\"alinéa 3\"\n\"alinéa 4\""
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
                }
            ]}
        )
