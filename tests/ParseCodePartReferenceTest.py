# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseCodePartReferenceTest(DuralexTestCase):
    def test_code_part(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_code_part_reference,
                u"la troisième partie du code de l'éducation"
            ),
            {'children': [
                {
                    'type': u'code-part-reference',
                    'order': 3,
                    'children': [
                        {
                            'type': u'code-reference',
                            'id': u'code de l\'éducation'
                        }
                    ]
                }
            ]}
        )
