# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

from duralex.SortReferencesVisitor import SortReferencesVisitor

class SortReferencesVisitorTest(DuralexTestCase):
    def test_law_article(self):
        self.assertEqualAST(
            self.call_visitor(SortReferencesVisitor, {'children': [
                {
                    'lawDate': u'1978-7-17',
                    'lawId': u'78-753',
                    'type': u'law-reference',
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'11',
                        }
                    ]
                }
            ]}),
            {'children': [
                {
                    'lawDate': u'1978-7-17',
                    'lawId': u'78-753',
                    'type': u'law-reference',
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'11'
                        }
                    ]
                }
            ]}
        )

    def test_article_law(self):
        self.assertEqualAST(
            self.call_visitor(SortReferencesVisitor, {'children': [
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
            ]}),
            {'children': [
                {
                    'lawDate': u'1978-7-17',
                    'lawId': u'78-753',
                    'type': u'law-reference',
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'11'
                        }
                    ]
                }
            ]}
        )
