# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseBillHeader2Test(DuralexTestCase):
    def test_header2_raw_content(self):
        self.assertEqualAST(
            self.call_parse_func(
                parser.parse_bill_header2,
                u"42° Ceci est un header2."
            ),
            {'children':[
                {
                    'type': u'bill-header2',
                    'order': 42,
                    'children': [
                        {

                        }
                    ]
                }
            ]}
        )
