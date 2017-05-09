# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

from duralex.ResolveFullyQualifiedReferencesVisitor import ResolveFullyQualifiedReferencesVisitor

class ResolveFullyQualifiedReferencesVisitorTest(DuralexTestCase):
    def test_code_danling_reference(self):
        self.assertEqualAST(
            self.call_visitor(ResolveFullyQualifiedReferencesVisitor, self.make_tree({'children': [
                {
                    'editType': u'edit',
                    'type': u'edit',
                    'children': [
                        {
                            'codeName': u'code de l\'éducation',
                            'type': u'code-reference'
                        }
                    ]
                },
                {
                    'editType': u'replace',
                    'type': u'edit',
                    'children': [
                        {
                            'type': u'word-definition',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'mots de remplacement'
                                }
                            ]
                        },
                        {
                            'type': u'word-reference',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'mots d\'origine'
                                }
                            ]
                        }
                    ]
                }
            ]})),
            {'children': [
                {
                    'editType': u'replace',
                    'type': u'edit',
                    'children': [
                        {
                            'codeName': u'code de l\'éducation',
                            'type': u'code-reference',
                            'children': [
                                {
                                    'type': u'word-reference',
                                    'children': [
                                        {
                                            'type': u'quote',
                                            'words': u'mots d\'origine'
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'type': u'word-definition',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'mots de remplacement'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_code_danling_reference_2(self):
        self.assertEqualAST(
            self.call_visitor(ResolveFullyQualifiedReferencesVisitor, self.make_tree({'children': [
                {
                    'editType': u'edit',
                    'type': u'edit',
                    'children': [
                        {
                            'id': u'L. 42',
                            'type': u'article-reference',
                            'children': [
                                {
                                    'codeName': u'code de l\'éducation',
                                    'type': u'code-reference'
                                }
                            ]
                        }
                    ]
                },
                {
                    'editType': u'replace',
                    'type': u'edit',
                    'children': [
                        {
                            'type': u'word-definition',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'mots de remplacement'
                                }
                            ]
                        },
                        {
                            'type': u'word-reference',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'mots d\'origine'
                                }
                            ]
                        }
                    ]
                }
            ]})),
            {'children': [
                {
                    'editType': u'replace',
                    'type': u'edit',
                    'children': [
                        {
                            'codeName': u'code de l\'éducation',
                            'type': u'code-reference',
                            'children': [
                                {
                                    'id': u'L. 42',
                                    'type': u'article-reference',
                                    'children': [
                                        {
                                            'type': u'word-reference',
                                            'children': [
                                                {
                                                    'type': u'quote',
                                                    'words': u'mots d\'origine'
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'type': u'word-definition',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'mots de remplacement'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_code_danling_reference_3(self):
        self.assertEqualAST(
            self.call_visitor(ResolveFullyQualifiedReferencesVisitor, self.make_tree({'children': [
                {
                    'type': u'header1-definition',
                    'order': 1,
                    'children': [
                        {
                            'editType': u'edit',
                            'type': u'edit',
                            'children': [
                                {
                                    'id': u'L. 42',
                                    'type': u'article-reference'
                                }
                            ]
                        },
                        {
                            'type': u'header2-definition',
                            'order': 1,
                            'children': [
                                {
                                    'editType': u'edit',
                                    'type': u'edit',
                                    'children': [
                                        {
                                            'order': 42,
                                            'type': u'alinea-reference'
                                        }
                                    ]
                                },
                                {
                                    'type': u'header3-definition',
                                    'order': 1,
                                    'children': [
                                        {
                                            'editType': u'replace',
                                            'type': u'edit',
                                            'children': [
                                                {
                                                    'type': u'word-definition',
                                                    'children': [
                                                        {
                                                            'type': u'quote',
                                                            'words': u'mots de remplacement'
                                                        }
                                                    ]
                                                },
                                                {
                                                    'type': u'word-reference',
                                                    'children': [
                                                        {
                                                            'type': u'quote',
                                                            'words': u'mots d\'origine'
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]})),
            {'children': [
                {
                    'type': u'header1-definition',
                    'order': 1,
                    'children': [
                        {
                            'type': u'header2-definition',
                            'order': 1,
                            'children': [
                                {
                                    'type': u'header3-definition',
                                    'order': 1,
                                    'children': [
                                        {
                                            'editType': u'replace',
                                            'type': u'edit',
                                            'children': [
                                                {
                                                    'id': u'L. 42',
                                                    'type': u'article-reference',
                                                    'children': [
                                                        {
                                                            'order': 42,
                                                            'type': u'alinea-reference',
                                                            'children': [
                                                                {
                                                                    'type': u'word-reference',
                                                                    'children': [
                                                                        {
                                                                            'type': u'quote',
                                                                            'words': u'mots d\'origine'
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    'type': u'word-definition',
                                                    'children': [
                                                        {
                                                            'type': u'quote',
                                                            'words': u'mots de remplacement'
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_do_nothing_when_no_nested_edits(self):
        self.assertEqualAST(
            self.call_visitor(ResolveFullyQualifiedReferencesVisitor, self.make_tree({'children': [
                {
                    'children': [
                        {
                            'children': [
                                {
                                    'children': [
                                        {
                                            'children': [
                                                {
                                                    'type': u'quote',
                                                    'words': u'Art. 4. - Le territoire de la République forme une circonscription unique.'
                                                }
                                            ],
                                            'type': u'word-definition'
                                        },
                                        {
                                            'children': [
                                                {
                                                    'id': u'4',
                                                    'type': u'article-reference'
                                                }
                                            ],
                                            'lawDate': u'1977-7-7',
                                            'lawId': u'77-729',
                                            'type': u'law-reference'
                                        }
                                    ],
                                    'editType': u'edit',
                                    'type': u'edit'
                                }
                            ],
                            'order': 1,
                            'type': u'header1-definition'
                        }
                    ],
                    'isNew': False,
                    'order': 2,
                    'type': u'article-definition'
                }
            ]})),
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
                                                    'type': u'quote',
                                                    'words': u'Art. 4. - Le territoire de la République forme une circonscription unique.'
                                                }
                                            ],
                                            'type': u'word-definition'
                                        },
                                        {
                                            'children': [
                                                {
                                                    'id': u'4',
                                                    'type': u'article-reference'
                                                }
                                            ],
                                            'lawDate': u'1977-7-7',
                                            'lawId': u'77-729',
                                            'type': u'law-reference'
                                        }
                                    ],
                                    'editType': u'edit',
                                    'type': u'edit'
                                }
                            ],
                            'order': 1,
                            'type': u'header1-definition'
                        }
                    ],
                    'isNew': False,
                    'order': 2,
                    'type': u'article-definition'
                }
            ]}
        )
