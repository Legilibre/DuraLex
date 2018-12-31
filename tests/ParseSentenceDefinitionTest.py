# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase, main

import duralex.alinea_parser as parser

class ParseSentenceDefinitionTest(DuralexTestCase):
    def test_one_sentence_with_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_definition,
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
                parser.parse_definition,
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
                        },
                        {
                            'type': 'quote',
                            'words': 'phrase 2'
                        },
                        {
                            'type': 'quote',
                            'words': 'phrase 3'
                        }
                    ],
                    'count': 3,
                    'type': 'sentence-definition'
                }
            ]}
        )

if __name__ == '__main__':
    main()

# vim: set ts=4 sw=4 sts=4 et:
