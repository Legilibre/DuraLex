# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseRawContentTest(DuralexTestCase):
    def test_raw_content(self):
        self.assertEqualAST(
            self.call_parse_func(
                lambda tokens, i, parent: parser.parse_for_each(parser.parse_bill_header1, tokens, 0, parent),
                (u"I. - Dans les conditions prévues à l'article 38 de la Constitution, le Gouvernement est autorisé à modifier par ordonnance le code de la recherche afin :\n"
                u"1° D'adapter le code, à droit constant, afin d'y créer un nouveau livre relatif à la valorisation et au transfert de la recherche en direction du monde économique, des associations et fondations, reconnues d'utilité publique ;\n"
                u"2° De remédier aux éventuelles erreurs de codification ;\n"
                u"3° D'abroger les dispositions devenues sans objet ;\n"
                u"4° D'étendre, le cas échéant avec les adaptations nécessaires, l'application des dispositions du code de la recherche en Nouvelle-Calédonie, en Polynésie française, dans les îles Wallis et Futuna et dans les Terres australes et antarctiques françaises ainsi que de permettre les adaptations nécessaires à l'application de ces dispositions à Mayotte, à Saint-Barthélemy, à Saint-Martin et à Saint-Pierre-et-Miquelon.\n"
                u"II. - Dans les conditions prévues à l'article 38 de la Constitution, le Gouvernement est autorisé à modifier par ordonnance la partie législative du code de l'éducation afin :\n"
                u"1° D'adapter le code, afin, notamment, d'introduire des dispositions relatives aux études de maïeutique et de modifier celles relatives aux établissements d'enseignement supérieur spécialisés ;\n"
                u"2° De remédier aux éventuelles erreurs de codification ;\n"
                u"3° D'abroger les dispositions devenues sans objet ;\n"
                u"4° D'étendre, le cas échéant avec les adaptations nécessaires, l'application de ces dispositions du code de l'éducation à Mayotte, en Nouvelle-Calédonie, en Polynésie française et dans les îles Wallis et Futuna.\n"
                u"III. - Les ordonnances prévues aux I et II doivent être prises dans un délai d'un an à compter de la promulgation de la présente loi.\n"
                u"Pour chaque ordonnance, un projet de loi de ratification est déposé devant le Parlement dans un délai de six mois à compter de la publication de l'ordonnance.")
            ),
            {'children':[
                {
                    'order': 1,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'Dans les conditions prévues à l\'article 38 de la Constitution, le Gouvernement est autorisé à modifier par ordonnance le code de la recherche afin :',
                            'type': u'article-content'
                        }
                    ]
                },
                {
                    'order': 2,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'D\'adapter le code, à droit constant, afin d\'y créer un nouveau livre relatif à la valorisation et au transfert de la recherche en direction du monde économique, des associations et fondations, reconnues d\'utilité publique ;',
                            'type': u'article-content'
                        }
                    ]
                },
                {
                    'order': 3,
                    'type': u'bill-header1',
                    'children': [
                        {
                        'content': u'De remédier aux éventuelles erreurs de codification ;',
                        'type': u'article-content'
                        }
                    ]
                },
                {
                    'order': 4,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'D\'abroger les dispositions devenues sans objet ;',
                            'type': u'article-content'
                        }
                    ]
                },
                {
                    'order': 5,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'D\'étendre, le cas échéant avec les adaptations nécessaires, l\'application des dispositions du code de la recherche en Nouvelle-Calédonie, en Polynésie française, dans les îles Wallis et Futuna et dans les Terres australes et antarctiques françaises ainsi que de permettre les adaptations nécessaires à l\'application de ces dispositions à Mayotte, à Saint-Barthélemy, à Saint-Martin et à Saint-Pierre-et-Miquelon.',
                            'type': u'article-content'
                        }
                    ]
                },
                {
                    'order': 6,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'Dans les conditions prévues à l\'article 38 de la Constitution, le Gouvernement est autorisé à modifier par ordonnance la partie législative du code de l\'éducation afin :',
                            'type': u'article-content'
                        }
                    ]
                },
                {
                    'order': 7,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'D\'adapter le code, afin, notamment, d\'introduire des dispositions relatives aux études de maïeutique et de modifier celles relatives aux établissements d\'enseignement supérieur spécialisés ;',
                            'type': u'article-content'
                        }
                    ]
                },
                {
                    'order': 8,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'De remédier aux éventuelles erreurs de codification ;',
                            'type': u'article-content'
                        }
                    ]
                },
                {
                    'order': 9,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'D\'abroger les dispositions devenues sans objet ;',
                            'type': u'article-content'
                        }
                    ]
                },
                {
                    'order': 10,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'D\'étendre, le cas échéant avec les adaptations nécessaires, l\'application de ces dispositions du code de l\'éducation à Mayotte, en Nouvelle-Calédonie, en Polynésie française et dans les îles Wallis et Futuna.',
                            'type': u'article-content'
                        }
                    ]
                },
                {
                    'order': 11,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'Les ordonnances prévues aux I et II doivent être prises dans un délai d\'un an à compter de la promulgation de la présente loi.',
                            'type': u'article-content'
                        }
                    ]
                },
                {
                    'order': 12,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'Pour chaque ordonnance, un projet de loi de ratification est déposé devant le Parlement dans un délai de six mois à compter de la publication de l\'ordonnance.',
                            'type': u'article-content'
                        }
                    ]
                }
            ]}
        )
