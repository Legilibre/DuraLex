# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseArticleHeader1Test(DuralexTestCase):
    def test_header1_incomplete_edit_header2_edit(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_header1,
                (u"L'article L. 123-5 du code de l'éducation est ainsi modifié :\n"
                u"1° À la première phrase, les mots : \"mots d'origine\" sont remplacés par les mots : \"mots de remplacement\".")
            ),
            {'children':[
                {
                    'type': u'header1',
                    'order': 1,
                    'children': [
                        {
                            'editType': u'edit',
                            'type': u'edit',
                            'children': [
                                {
                                    'id': u'L. 123-5',
                                    'type': u'article-reference',
                                    'children': [
                                        {
                                            'type': u'code-reference',
                                            'codeName': u'code de l\'éducation'
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'type': u'header2',
                            'order': 1,
                            'children': [
                                {
                                    'editType': u'replace',
                                    'type': u'edit',
                                    'children': [
                                        {
                                            'type': u'sentence-reference',
                                            'order': 1,
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
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_header1_incomplete_edit_header2_incomplete_edit_header3_edit(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_article_header1,
                (u"L'article L. 123-5 du code de l'éducation est ainsi modifié :\n"
                u"1° L'avant-dernier alinéa est ainsi modifié :\n"
                u"a) À la première phrase, les mots : \"mots d'origine\" sont remplacés par les mots : \"mots de remplacement\".")
            ),
            {'children':[
                {
                    'type': u'header1',
                    'order': 1,
                    'children': [
                        {
                            'editType': u'edit',
                            'type': u'edit',
                            'children': [
                                {
                                    'id': u'L. 123-5',
                                    'type': u'article-reference',
                                    'children': [
                                        {
                                            'type': u'code-reference',
                                            'codeName': u'code de l\'éducation'
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'type': u'header2',
                            'order': 1,
                            'children': [
                                {
                                    'editType': u'edit',
                                    'type': u'edit',
                                    'children': [
                                        {
                                            'order': -2,
                                            'type': u'alinea-reference'
                                        }
                                    ]
                                },
                                {
                                    'type': u'header3',
                                    'order': 1,
                                    'children': [
                                        {
                                            'editType': u'replace',
                                            'type': u'edit',
                                            'children': [
                                                {
                                                    'type': u'sentence-reference',
                                                    'order': 1,
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
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]}
        )
