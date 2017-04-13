# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseLawReferenceTest(DuralexTestCase):
    def test_ordonnance_with_id(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_law_reference,
                u"l'ordonnance n° 2008-1305 du 11 décembre 2008"
            ),
            {'children':[
                {
                    'type': u'law-reference',
                    'lawId': u'2008-1305',
                    'lawDate': u'2008-12-11',
                    'lawType': u'ordonnance'
                }
            ]}
        )

    def test_ordonnance_with_id_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_law_reference,
                u"de l'ordonnance n° 2008-1305 du 11 décembre 2008"
            ),
            {'children':[
                {
                    'type': u'law-reference',
                    'lawId': u'2008-1305',
                    'lawDate': u'2008-12-11',
                    'lawType': u'ordonnance'
                }
            ]}
        )

    def test_law_with_id(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_law_reference,
                u"la loi n° 2007-1199"
            ),
            {'children':[
                {
                    'type': u'law-reference',
                    'lawId': u'2007-1199'
                }
            ]}
        )

    def test_law_with_id_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_law_reference,
                u"de la loi n° 2007-1199"
            ),
            {'children':[
                {
                    'type': u'law-reference',
                    'lawId': u'2007-1199'
                }
            ]}
        )

    def test_law_with_id_and_date(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_law_reference,
                u"la loi n° 2007-1199 du 10 août 2007"
            ),
            {'children':[
                {
                    'type': u'law-reference',
                    'lawId': u'2007-1199',
                    'lawDate': u'2007-8-10'
                }
            ]}
        )

    def test_law_with_id_and_date_2(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_law_reference,
                u"de la loi n° 2007-1199 du 10 août 2007"
            ),
            {'children':[
                {
                    'type': u'law-reference',
                    'lawId': u'2007-1199',
                    'lawDate': u'2007-8-10'
                }
            ]}
        )

    def test_law_with_id_and_code_name(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_law_reference,
                u"l'ordonnance n° 2008-1305 du 11 décembre 2008 modifiant la partie législative du code de la recherche"
            ),
            {'children':[
                {
                    'type': u'law-reference',
                    'lawType': u'ordonnance',
                    'lawId': u'2008-1305',
                    'lawDate': u'2008-12-11',
                    'children': [
                        {
                            'type': u'code-reference',
                            'codeName': u'code de la recherche'
                        }
                    ]
                }
            ]}
        )
