# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase, main

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
                            'type': u'word-definition',
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

    def test_edit_article_law_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                u"l'article 42 de la loi n° 77‑729 est ainsi rédigé :\n\"ceci est un test\""
            ),
            {'children':[
                {
                    'type': u'edit',
                    'editType': u'edit',
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'42',
                            'children': [
                                {
                                    'type': u'law-reference',
                                    'id': u'77‑729',
                                    'lawType': u'loi'
                                }
                            ]
                        },
                        {
                            'type': u'word-definition',
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

    def test_edit_article_with_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                (u"l'article 42 est ainsi rédigé :\n"
                u"\"ceci est la 1ère phrase\"\n"
                u"\"ceci est la 2nde phrase\"")
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
                            'type': u'word-definition',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'ceci est la 1ère phrase'
                                },
                                {
                                    'type': u'quote',
                                    'words': u'ceci est la 2nde phrase'
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
                    'type': 'edit',
                    'editType': 'add',
                    'children': [
                        {
                            'type': 'article-reference',
                            'id': '42'
                        },
                        {
                            'type': 'alinea-definition',
                            'count': 1,
                            'children': [
                                {
                                    'type': 'quote',
                                    'words': 'ceci est un test'
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
                            'type': u'word-reference',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'mots d\'origine'
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

    def test_single_word_replaced_by_single_word(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                "le mot : \"original\" est remplacé par le mot : \"remplacement\""
            ),
            {'children': [
                {
                    'type': u'edit',
                    'editType': u'replace',
                    'children': [
                        {
                            'type': u'word-reference',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'original'
                                }
                            ]
                        },
                        {
                            'type': u'word-definition',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'remplacement'
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
                            'type': u'header2-definition',
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
                            'id': u'code de l\'éducation',
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
                ("Avant le dernier alinéa, sont insérés deux alinéas ainsi rédigés :\n"
                "\"alinéa 1\"\n"
                "\"alinéa 2\"\n")
            ),
            {'children':[
                {
                    'type': 'edit',
                    'editType': 'add',
                    'children': [
                        {
                            'type': 'alinea-reference',
                            'position': 'before',
                            'order': -1
                        },
                        {
                            'type': 'alinea-definition',
                            'count': 2,
                            'children': [
                                {
                                    'type': 'quote',
                                    'words': 'alinéa 1'
                                },
                                {
                                    'type': 'quote',
                                    'words': 'alinéa 2'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_insert_n_sentences_with_n_quotes(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                ("à l'article 42 sont insérées deux phrases ainsi rédigées :\n"
                "\"phrase 1\"\n"
                "\"phrase 2\"\n")
            ),
            {'children':[
                {
                    'type': 'edit',
                    'editType': 'add',
                    'children': [
                        {
                            'type': 'article-reference',
                            'id': '42'
                        },
                        {
                            'type': 'sentence-definition',
                            'count': 2,
                            'children': [
                                {
                                    'type': 'quote',
                                    'words': 'phrase 1'
                                },
                                {
                                    'type': 'quote',
                                    'words': 'phrase 2'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_the_nth_sentence_redacted_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                (u"la deuxième phrase est ainsi rédigée :\n"
                u"\"ceci est un test\"")
            ),
            {'children':[
                {
                    'editType': u'edit',
                    'type': u'edit',
                    'children': [
                        {
                            'type': u'sentence-reference',
                            'order': 2
                        },
                        {
                            'type': u'word-definition',
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

    def test_is_inserted(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                u"Est ajoutée une phrase"
            ),
            {'children':[
                {
                    'editType': u'add',
                    'type': u'edit',
                    'children': [
                        {
                            'type': u'sentence-definition',
                            'count': 1
                        }
                    ]
                }
            ]}
        )

    def test_is_inserted_with_quote(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                ("Est ajoutée une phrase ainsi rédigée :\n"
                "\"ceci est une phrase\"")
            ),
            {'children':[
                {
                    'type': 'edit',
                    'editType': 'add',
                    'children': [
                        {
                            'type': 'sentence-definition',
                            'count': 1,
                            'children': [
                                {
                                    'type': 'quote',
                                    'words': 'ceci est une phrase'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_is_ratified(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                "l'article 42 est ratifié"
            ),
            {'children':[
                {
                    'type': u'edit',
                    'editType': u'ratified',
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'42'
                        }
                    ]
                }
            ]}
        )

    def test_reference_replaced_by_reference(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                u"la référence : \"L. 321-5\" est remplacée par la référence : \"L. 313-1\""
            ),
            {'children':[
                {
                    'type': u'edit',
                    'editType': u'replace',
                    'children': [
                        {
                            'type': u'word-reference',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'L. 321-5'
                                }
                            ]
                        },
                        {
                            'type': u'word-definition',
                            'children': [
                                {
                                    'type': u'quote',
                                    'words': u'L. 313-1'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_rename_article(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                u"l'article L. 123-4-1 devient l'article L. 123-4-2"
            ),
            {'children':[
                {
                    'type': u'edit',
                    'editType': u'rename',
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'L. 123-4-1'
                        },
                        {
                            'type': u'article-definition',
                            'id': u'L. 123-4-2'
                        }
                    ]
                }
            ]}
        )

    def test_restore_article(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                u"l'article L. 123-4-1 est ainsi rétabli"
            ),
            {'children':[
                {
                    'type': u'edit',
                    'editType': u'add',
                    'children': [
                        {
                            'type': u'article-reference',
                            'id': u'L. 123-4-1'
                        }
                    ]
                }
            ]}
        )

    def test_delete_alinea(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                u"le troisième alinéa est supprimé"
            ),
            {'children':[
                {
                    'type': u'edit',
                    'editType': u'delete',
                    'children': [
                        {
                            'type': u'alinea-reference',
                            'order': 3
                        }
                    ]
                }
            ]}
        )

    def test_delete_end_of_last_sentence_after_word(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_edit,
                u"Après le mot : \"candidats\", la fin de la première phrase du quatrième alinéa est supprimée."
            ),
            {'children':[
                {
                    'editType': 'delete',
                    'type': 'edit',
                    'children': [
                        {
                            'position': 'after',
                            'type': 'word-reference',
                            'children': [
                                {
                                    'type': 'quote',
                                    'words': 'candidats'
                                },
                                {
                                    'order': 1,
                                    'scope': 'end',
                                    'type': 'sentence-reference',
                                    'children': [
                                        {
                                            'order': 4,
                                            'type': 'alinea-reference'
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

if __name__ == '__main__':
    main()

# vim: set ts=4 sw=4 sts=4 et:
