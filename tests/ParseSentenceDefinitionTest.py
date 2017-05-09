# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseSentenceDefinitionTest(DuralexTestCase):
    def test_one_sentence_with_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_sentence_definition,
                ("une phrase ainsi rédigée :\n"
                "\"phrase 1\"\n")
            ),
            {'children':[
                {
                    'children': [
                        {
                            'type': 'quote',
                            'words': 'phrase 1'
                        }
                    ],
                    'type': 'sentence-definition'
                }
            ]}
        )

    def test_three_sentences_with_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_sentence_definition,
                ("trois phrases ainsi rédigées :\n"
                "\"phrase 1\"\n"
                "\"phrase 2\"\n"
                "\"phrase 3\"\n")
            ),
            {'children':[
                {
                    'children': [
                        {
                            'type': 'quote',
                            'words': 'phrase 1'
                        }
                    ],
                    'type': 'sentence-definition'
                },
                {
                    'children': [
                        {
                            'type': 'quote',
                            'words': 'phrase 2'
                        }
                    ],
                    'type': 'sentence-definition'
                },
                {
                    'children': [
                        {
                            'type': 'quote',
                            'words': 'phrase 3'
                        }
                    ],
                    'type': 'sentence-definition'
                }
            ]}
        )
