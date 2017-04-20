# -*- coding: utf-8 -*-

from AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *

import duralex.node_type

def int_to_roman(integer):
    string = ''
    table = [
        ['M',1000], ['CM',900], ['D',500], ['CD',400], ['C',100], ['XC',90], ['L',50], ['XL',40], ['X',10], ['IX',9],
        ['V',5], ['IV',4], ['I',1]
    ]

    for pair in table:
        while integer - pair[1] >= 0:
            integer -= pair[1]
            string += pair[0]

    return string

class AddCommitMessageVisitor(AbstractVisitor):
    def __init__(self):
        self.ref_parts = []
        self.def_parts = []

        super(AddCommitMessageVisitor, self).__init__()

    def visit_law_reference_node(self, node, post):
        if post:
            return

        self.ref_parts.append(u'de la loi N°' + node['lawId'])

    def visit_article_reference_node(self, node, post):
        if post:
            return

        if len(node['children']) > 0:
            self.ref_parts.append(u'dans l\'article ' + node['id'])
        else:
            self.ref_parts.append(u'l\'article ' + node['id'])

    def visit_words_reference_node(self, node, post):
        if post:
            return

        quotes = filter_nodes(node, lambda n: n['type'] == 'quote')
        quotes = ''.join([n['words'] for n in quotes])

        self.ref_parts.append(u'les mots "' + quotes + '"')

    def visit_words_definition_node(self, node, post):
        if post:
            return

        quotes = filter_nodes(node, lambda n: n['type'] == 'quote')
        quotes = ''.join([n['words'] for n in quotes])

        self.def_parts.append(u'les mots "' + quotes + '"')

    def visit_edit_node(self, node, post):
        if not post:
            self.ref_parts = []
            self.def_parts = []
            return

        edit_desc = ''
        if node['editType'] == 'delete':
            edit_desc = 'supprimer ' + ' '.join(self.ref_parts[::-1])
        elif node['editType'] == 'edit':
            edit_desc = 'remplacer ' + ' '.join(self.ref_parts[::-1]) + ' par ' + ', '.join(self.def_parts)
        elif node['editType'] == 'add':
            edit_desc = 'ajouter ' + ' '.join(self.ref_parts[::-1])

        origin = []
        ancestors = get_node_ancestors(node)
        for ancestor in ancestors:
            if 'type' not in ancestor:
                continue;

            if ancestor['type'] == 'article':
                origin.append('Article ' + str(ancestor['order']))
            if ancestor['type'] == 'bill-header1' and 'implicit' not in ancestor:
                origin.append(int_to_roman(ancestor['order']))
            if ancestor['type'] == 'bill-header2':
                origin.append(unicode(ancestor['order']) + u'°')
        origin = ', '.join(origin[::-1])

        node['commitMessage'] = edit_desc[0].upper() + edit_desc[1:] + ' (' + origin + ').'
