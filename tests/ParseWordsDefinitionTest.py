# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseWordsDefinitionTest(DuralexTestCase):
    def test_the_word(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_words_definition,
                ("le mot \"test\"")
            ),
            {'children':[
                {
                    'type': u'words',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'test'
                        }
                    ]
                }
            ]}
        )

    def test_the_words(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_words_definition,
                ("les mots \"ceci est un test\"")
            ),
            {'children':[
                {
                    'type': u'words',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est un test'
                        }
                    ]
                }
            ]}
        )

    def test_the_number(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_words_definition,
                ("le nombre \"42\"")
            ),
            {'children':[
                {
                    'type': u'words',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'42'
                        }
                    ]
                }
            ]}
        )

    def test_the_figure(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_words_definition,
                ("le nombre \"4\"")
            ),
            {'children':[
                {
                    'type': u'words',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'4'
                        }
                    ]
                }
            ]}
        )

    def test_the_reference(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_words_definition,
                ("la référence \"ceci est une référence\"")
            ),
            {'children':[
                {
                    'type': u'words',
                    'children': [
                        {
                            'type': u'quote',
                            'words': u'ceci est une référence'
                        }
                    ]
                }
            ]}
        )
