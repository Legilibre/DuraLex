# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

from duralex.SortReferencesVisitor import SortReferencesVisitor

class SortReferencesVisitorTest(DuralexTestCase):
    def test_law_article(self):
        self.assertEqualAST(
            self.call_visitor(SortReferencesVisitor, {'children': [
                {
                    'lawDate': u'1978-7-17',
                    'id': u'78-753',
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
                    'id': u'78-753',
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
                            'id': u'78-753',
                            'type': u'law-reference',
                        }
                    ]
                }
            ]}),
            {'children': [
                {
                    'lawDate': u'1978-7-17',
                    'id': u'78-753',
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

    def test_paragraph_subsection_section_chapter_title_book(self):
        self.assertEqualAST(
            self.call_visitor(SortReferencesVisitor, {'children': [
                {
                    'children': [
                        {
                            'children': [
                                {
                                    'children': [
                                        {
                                            'children': [
                                                {
                                                    'children': [
                                                        {
                                                            'order': 1,
                                                            'type': u'book-reference'
                                                        }
                                                    ],
                                                    'order': 3,
                                                    'type': u'title-reference'
                                                }
                                            ],
                                            'order': 2,
                                            'type': u'chapter-reference'
                                        }
                                    ],
                                    'order': 2,
                                    'type': u'section-reference'
                                }
                            ],
                            'order': 2,
                            'type': u'subsection-reference'
                        }
                    ],
                    'order': 3,
                    'type': u'paragraph-reference'
                }
            ]}),
            {'children': [
                {
                    'children': [
                        {
                            'children': [
                                {
                                    'children': [
                                        {
                                            'children': [
                                                {
                                                    'children': [
                                                        {
                                                            'order': 3,
                                                            'type': u'paragraph-reference'
                                                        }
                                                    ],
                                                    'order': 2,
                                                    'type': u'subsection-reference'
                                                }
                                            ],
                                            'order': 2,
                                            'type': u'section-reference'
                                        }
                                    ],
                                    'order': 2,
                                    'type': u'chapter-reference'
                                }
                            ],
                            'order': 3,
                            'type': u'title-reference'
                        }
                    ],
                    'order': 1,
                    'type': u'book-reference'
                }
            ]}
        )

    def test_article_ref_article_ref(self):
        self.assertEqualAST(
            self.call_visitor(SortReferencesVisitor, {'children': [
                {
                    'type': u'article-reference',
                    'id': u'11',
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'42'
                        }
                    ]
                }
            ]}),
            {'children': [
                {
                    'type': u'article-reference',
                    'id': u'42'
                }
            ]}
        )
