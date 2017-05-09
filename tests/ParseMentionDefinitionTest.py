# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseMentionDefinitionTest(DuralexTestCase):
    def test_mention_with_single_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_mention_definition,
                ("la mention : \"ceci est une mention\"")
            ),
            {'children': [
                {
                    'type': u'mention-definition',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est une mention'
                        }
                    ]
                }
            ]}
        )

    def test_mention_with_n_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_mention_definition,
                ("la mention : \n"
                "\"ceci est le début de la mention\"\n"
                "\"ceci est la suite de la mention\"")
            ),
            {'children': [
                {
                    'type': u'mention-definition',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est le début de la mention'
                        },
                        {
                            'type': u'quote',
                            'words': u'ceci est la suite de la mention'
                        }
                    ]
                }
            ]}
        )
