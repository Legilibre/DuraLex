# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseArticleReferenceTest(DuralexTestCase):
    def test_article_number(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_reference,
                "l'article 3"
            ),
            {'children':[
                {
                    'type': u'article-reference',
                    'id': u'3'
                }
            ]}
        )

    def test_article_id(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_reference,
                "l'article L. 121-3"
            ),
            {'children':[
                {
                    'type': u'article-reference',
                    'id': u'L. 121-3'
                }
            ]}
        )

    def test_article_id_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_reference,
                "à l'article L. 121-3"
            ),
            {'children':[
                {
                    'type': u'article-reference',
                    'id': u'L. 121-3'
                }
            ]}
        )

    def test_article_id_law_id(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_reference,
                u"l'article 11 de la loi n° 78-753"
            ),
            {'children':[
                {
                    'type': u'article-reference',
                    'id': u'11',
                    'children': [
                        {
                            'lawId': u'78-753',
                            'type': u'law-reference',
                        }
                    ]
                }
            ]}
        )

    def test_article_id_law_id_law_date(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_reference,
                u"l'article 11 de la loi n° 78-753 du 17 juillet 1978"
            ),
            {'children':[
                {
                    'type': u'article-reference',
                    'id': u'11',
                    'children': [
                        {
                            'lawDate': u'1978-7-17',
                            'lawId': u'78-753',
                            'type': u'law-reference',
                        }
                    ]
                }
            ]}
        )

    def test_article_id_code_name(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_reference,
                u"l'article L. 111-5 du code de l'éducation"
            ),
            {'children': [
                {
                    'id': u'L. 111-5',
                    'type': u'article-reference',
                    'children': [
                        {
                            'codeName': u'code de l\'éducation',
                            'type': u'code-reference'
                        }
                    ]
                }
            ]}
        )

    def test_the_same_article(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_reference,
                u"le même article",
                {'children':[
                    {
                        'id': u'L. 111-5',
                        'type': u'article-reference'
                    }
                ]}
            ),
            {'children':[
                {
                    'id': u'L. 111-5',
                    'type': u'article-reference'
                },
                {
                    'id': u'L. 111-5',
                    'type': u'article-reference'
                }
            ]}
        )
