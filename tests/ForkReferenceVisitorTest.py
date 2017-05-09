# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

from duralex.ForkReferenceVisitor import ForkReferenceVisitor

class ForkReferenceVisitorTest(DuralexTestCase):
    def test(self):
        self.assertEqualAST(
            self.call_visitor(ForkReferenceVisitor, self.make_tree({'children': [
                {
                    'type': u'alinea-reference',
                    'order': 3,
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'2'
                        },
                        {
                            'type': u'article-reference',
                            'id': u'3'
                        }
                    ]
                }
            ]})),
            {'children': [
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
            ]}
        )
