# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseArticleDefinitionTest(DuralexTestCase):
    def test_an_article(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_definition,
                "un article"
            ),
            {'children':[
                {
                    'type': u'article'
                }
            ]}
        )

    def test_an_article_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_definition,
                "l'article"
            ),
            {'children':[
                {
                    'type': u'article'
                }
            ]}
        )

    def test_an_article_with_id(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_definition,
                "un article 42"
            ),
            {'children':[
                {
                    'type': u'article',
                    'id': u'42'
                }
            ]}
        )

    def test_an_article_with_id_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_definition,
                "l'article 42"
            ),
            {'children':[
                {
                    'type': u'article',
                    'id': u'42'
                }
            ]}
        )
