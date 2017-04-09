# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseEditTest(DuralexTestCase):
    def test_delete_article(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                "l'article 42 est abrogé"
            ),
            {'children':[
                {
                    'type': u'edit',
                    'editType': u'delete',
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'42'
                        }
                    ]
                }
            ]}
        )

    def test_edit_article(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                "l'article 42 est ainsi rédigé"
            ),
            {'children':[
                {
                    'type': u'edit',
                    'editType': u'edit',
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'42'
                        }
                    ]
                }
            ]}
        )

    def test_edit_article_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                "l'article 42 est ainsi rédigé :\n\"ceci est un test\""
            ),
            {'children':[
                {
                    'type': u'edit',
                    'editType': u'edit',
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'42'
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

    def test_article_completed_by_alinea_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                "l'article 42 est complété par un alinéa ainsi rédigé: \"ceci est un test\""
            ),
            {'children': [
                {
                    'type': u'edit',
                    'editType': u'add',
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'42'
                        },
                        {
                            'type': u'alinea',
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

    def test_words_replaced_by_words(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                "les mots : \"mots d'origine\" sont remplacés par les mots : \"mots de remplacement\""
            ),
            {'children': [
                {
                    'type': u'edit',
                    'editType': u'replace',
                    'children': [
                        {
                            'type': u'words-reference',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'mots d\'origine'
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

    def test_before_header2_add_header2_suborder(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                "avant le 1°, il est ajouté un 1° A"
            ),
            {'children': [
                {
                    'type': u'edit',
                    'editType': u'add',
                    'children': [
                        {
                            'type': u'header2-reference',
                            'order': 1,
                            'position': u'before'
                        },
                        {
                            'type': u'header2',
                            'order': 1,
                            'subOrder': u'A'
                        }
                    ]
                }
            ]}
        )

    def test_dangling_code_reference(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                u"Le code de l'éducation est ainsi modifié"
            ),
            {'children':[
                {
                    'editType': u'edit',
                    'type': u'edit',
                    'children': [
                        {
                            'codeName': u'code de l\'éducation',
                            'type': u'code-reference'
                        }
                    ]
                }
            ]}
        )

    def test_insert_two_alineas_with_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                (u"Avant le dernier alinéa, sont insérés deux alinéas ainsi rédigés :\n"
                u"\"alinéa 1\"\n"
                u"\"alinéa 2\"\n")
            ),
            {'children':[
                {
                    'editType': u'add',
                    'type': u'edit',
                    'children': [
                        {
                            'type': u'alinea-reference',
                            'position': u'before',
                            'order': -1
                        },
                        {
                            'type': u'alinea',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'alinéa 1'
                                }
                            ]
                        },
                        {
                            'type': 'alinea',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'alinéa 2'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )
