# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

from duralex.ResolveFullyQualifiedReferencesVisitor import ResolveFullyQualifiedReferencesVisitor

class ResolveFullyQualifiedReferencesVisitorTest(DuralexTestCase):
    def test_code_danling_reference(self):
        self.assertEqualAST(
            self.call_visitor(ResolveFullyQualifiedReferencesVisitor, self.make_ast({'children': [
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
                            'type': u'words',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'mots de remplacement'
                                }
                            ]
                        },
                        {
                            'type': u'words-reference',
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
                                    'type': u'words-reference',
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
                            'type': u'words',
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
