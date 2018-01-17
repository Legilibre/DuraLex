# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseHeader3Test(DuralexTestCase):
    def test_header3_raw_content(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_header3,
                u"b) Ceci est un header3."
            ),
            {'children':[
                {
                    'type': u'header3',
                    'order': 2,
                    'children': [
                        {
                            'type': u'raw-content',
                            'content': u'Ceci est un header3.'
                        }
                    ]
                }
            ]}
        )
