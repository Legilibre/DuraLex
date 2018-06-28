# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseLookbackReferenceTest(DuralexTestCase):
    def test(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_lookback_reference,
                "Il",
                {'children':[
                    {
                        'id': u'code de l\'éducation',
                        'type': u'code-reference'
                    }
                ]}
            ),
            {'children':[
                {
                    'id': u'code de l\'éducation',
                    'type': u'code-reference'
                },
                {
                    'id': u'code de l\'éducation',
                    'type': u'code-reference'
                }
            ]}
        )
