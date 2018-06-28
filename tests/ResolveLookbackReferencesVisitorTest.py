# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

from duralex.tree import *

from duralex.ResolveLookbackReferencesVisitor import ResolveLookbackReferencesVisitor

class ResolveLookbackReferencesVisitorTest(DuralexTestCase):
    def test_2_code_loockback_reference(self):
        self.assertEqualAST(
            self.call_visitor(ResolveLookbackReferencesVisitor, self.make_tree({'children': [
                {
                    'type': u'law-reference',
                    'id': u'77-729'
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'law-reference',
                        }
                    ]
                }
            ]})),
            {'children': [
                {
                    'type': u'law-reference',
                    'id': u'77-729'
                },
                {
                    'type': u'law-reference',
                    'id': u'77-729'
                }
            ]}
        )

    def test_1_code_loockback_reference(self):
        self.assertEqualAST(
            self.call_visitor(ResolveLookbackReferencesVisitor, self.make_tree({'children': [
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ]
                }
            ]})),
            {'children': [
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                }
            ]}
        )
    
    def test_2_code_loockback_references(self):
        self.assertEqualAST(
            self.call_visitor(ResolveLookbackReferencesVisitor, self.make_tree({'children': [
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ]
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ]
                }
            ]})),
            {'children': [
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                }
            ]}
        )

    def test_3_code_loockback_references(self):
        self.assertEqualAST(
            self.call_visitor(ResolveLookbackReferencesVisitor, self.make_tree({'children': [
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ],
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ]
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ]
                }
            ]})),
            {'children': [
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                }
            ]}
        )
    
    def test_4_code_loockback_references(self):
        self.assertEqualAST(
            self.call_visitor(ResolveLookbackReferencesVisitor, self.make_tree({'children': [
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ],
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ]
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ]
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ]
                }
            ]})),
            {'children': [
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                }
            ]}
        )
    
    def test_5_code_loockback_references(self):
        self.assertEqualAST(
            self.call_visitor(ResolveLookbackReferencesVisitor, self.make_tree({'children': [
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ],
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ]
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ]
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ]
                },
                {
                    'type': TYPE_LOOKBACK_REFERENCE,
                    'children': [
                        {
                            'type': u'code-reference',
                        }
                    ]
                }
            ]})),
            {'children': [
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                },
                {
                    'type': u'code-reference',
                    'id': u'code de l\'éducation'
                }
            ]}
        )
