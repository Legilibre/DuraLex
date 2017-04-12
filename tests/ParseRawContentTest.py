# -*- coding: utf-8 -*-

from DuralexTestCase import DuralexTestCase

import duralex.alinea_parser as parser

class ParseRawContentTest(DuralexTestCase):
    def test_header1_raw_content_header2_raw_content(self):
        self.assertEqualAST(
            self.call_parse_func(
                lambda tokens, i, parent: parser.parse_for_each(parser.parse_bill_header1, tokens, 0, parent),
                (u"I. - Contenu du header1 :\n"
                u"1° Contenu du header2.")
            ),
            {'children':[
                {
                    'order': 1,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'Contenu du header1 :',
                            'type': u'raw-content'
                        },
                        {
                            'type': u'bill-header2',
                            'order': 1,
                            'children': [
                                {
                                    'type': u'raw-content',
                                    'content': u'Contenu du header2.'
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_header1_raw_content_header2_raw_content_header3_raw_content(self):
        self.assertEqualAST(
            self.call_parse_func(
                lambda tokens, i, parent: parser.parse_for_each(parser.parse_bill_header1, tokens, 0, parent),
                (u"I. - Contenu du header1 :\n"
                u"1° Contenu du header2 :\n"
                u"a) Contenu du header3")
            ),
            {'children':[
                {
                    'order': 1,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'Contenu du header1 :',
                            'type': u'raw-content'
                        },
                        {
                            'type': u'bill-header2',
                            'order': 1,
                            'children': [
                                {
                                    'type': u'raw-content',
                                    'content': u'Contenu du header2 :'
                                },
                                {
                                    'order': 1,
                                    'type': u'bill-header3',
                                    'children': [
                                        {
                                            'content': u'Contenu du header3',
                                            'type': u'raw-content'
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]}
        )

    def test_n_header1_raw_content_n_header2_raw_content_n_header3_raw_content(self):
        self.assertEqualAST(
            self.call_parse_func(
                lambda tokens, i, parent: parser.parse_for_each(parser.parse_bill_header1, tokens, 0, parent),
                (u"I. - Contenu du grand 1 :\n"
                u"1° Contenu du grand 1 petit 1 :\n"
                u"a) Contenu du grand 1 petit 1 a\n"
                u"b) Contenu du grand 1 petit 1 b\n"
                u"2° Contenu du grand 1 petit 2.\n"
                u"II. - Contenu du grand 2 :\n"
                u"1° Contenu du grand 2 petit 1.\n"
                u"a) Contenu du grand 2 petit 1 a\n"
                u"b) Contenu du grand 2 petit 1 b\n"
                u"c) Contenu du grand 2 petit 1 c\n")
            ),
            {'children':[
                {
                    'order': 1,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'Contenu du grand 1 :',
                            'type': u'raw-content'
                        },
                        {
                            'order': 1,
                            'type': u'bill-header2',
                            'children': [
                                {
                                    'content': u'Contenu du grand 1 petit 1 :',
                                    'type': u'raw-content'
                                },
                                {
                                    'order': 1,
                                    'type': u'bill-header3',
                                    'children': [
                                        {
                                            'content': u'Contenu du grand 1 petit 1 a',
                                            'type': u'raw-content'
                                        }
                                    ]
                                },
                                {
                                    'order': 2,
                                    'type': u'bill-header3',
                                    'children': [
                                        {
                                            'content': u'Contenu du grand 1 petit 1 b',
                                            'type': u'raw-content'
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'order': 2,
                            'type': u'bill-header2',
                            'children': [
                                {
                                    'content': u'Contenu du grand 1 petit 2.',
                                    'type': u'raw-content'
                                }
                            ]
                        }
                    ]
                },
                {
                    'order': 2,
                    'type': u'bill-header1',
                    'children': [
                        {
                            'content': u'Contenu du grand 2 :',
                            'type': u'raw-content'
                        },
                        {
                            'order': 1,
                            'type': u'bill-header2',
                            'children': [
                                {
                                    'content': u'Contenu du grand 2 petit 1.',
                                    'type': u'raw-content'
                                },
                                {
                                    'order': 1,
                                    'type': u'bill-header3',
                                    'children': [
                                        {
                                            'content': u'Contenu du grand 2 petit 1 a',
                                            'type': u'raw-content'
                                        }
                                    ]
                                },
                                {
                                    'order': 2,
                                    'type': u'bill-header3',
                                    'children': [
                                        {
                                            'content': u'Contenu du grand 2 petit 1 b',
                                            'type': u'raw-content'
                                        }
                                    ]
                                },
                                {
                                    'order': 3,
                                    'type': u'bill-header3',
                                    'children': [
                                        {
                                            'content': u'Contenu du grand 2 petit 1 c',
                                            'type': u'raw-content'
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]}
        )
