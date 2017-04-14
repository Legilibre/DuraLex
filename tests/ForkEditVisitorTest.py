# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

from duralex.ForkEditVisitor import ForkEditVisitor

class ForkEditVisitorTest(DuralexTestCase):
    def test(self):
        self.assertEqualAST(
            self.call_visitor(ForkEditVisitor, self.make_ast({'children': [
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
            ]})),
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

    def test_2(self):
        self.assertEqualAST(
            self.call_visitor(ForkEditVisitor, self.make_ast({'children': [
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
                        },
                        {
                            'order': 4,
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
            ]})),
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
                },
                {
                    'type': 'edit',
                    'children': [
                        {
                            'order': 4,
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

    def test(self):
        self.assertEqualAST(
            self.call_visitor(ForkEditVisitor, self.make_ast({'children': [
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
                        },
                        {
                            'type': u'words',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'ceci est un test'
                                }
                            ]
                        }
                    ]
                }
            ]})),
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
                        },
                        {
                            'type': u'words',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'ceci est un test'
                                }
                            ]
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
                        },
                        {
                            'type': u'words',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'ceci est un test'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )
