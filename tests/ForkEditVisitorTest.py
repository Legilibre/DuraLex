# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

from duralex.ForkEditVisitor import ForkEditVisitor

class ForkEditVisitorTest(DuralexTestCase):
    def test_(self):
        self.assertEqualAST(
            self.call_visitor(ForkEditVisitor, {'children': [
                {
                    'type': 'edit',
                    'children': [
                        {
                            'type': u'alinea-reference',
                            'order': 3,
                            'children': [
                                {
                                    'id': u'2',
                                    'type': u'article-reference'
                                }
                            ],
                        },
                        {
                            'order': 3,
                            'type': u'alinea-reference',
                            'children': [
                                {
                                    'id': u'3',
                                    'type': u'article-reference'
                                }
                            ]
                        }
                    ]
                }
            ]}
        ),
        {'children': [
            {
                'type': 'edit',
                'children': [
                    {
                        'type': u'alinea-reference',
                        'order': 3,
                        'children': [
                            {
                                'id': u'2',
                                'type': u'article-reference'
                            }
                        ],
                    }
                ]
            },
            {
                'type': 'edit',
                'children': [
                    {
                        'order': 3,
                        'type': u'alinea-reference',
                        'children': [
                            {
                                'id': u'3',
                                'type': u'article-reference'
                            }
                        ]
                    }
                ]
            }
        ]}
    )
