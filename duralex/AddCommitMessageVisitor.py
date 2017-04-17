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
    def visit_edit_node(self, node, post):
        if post:
            return

        messages = []
        ancestors = get_node_ancestors(node)
        for ancestor in ancestors:
            if 'type' not in ancestor:
                continue;

            if ancestor['type'] == 'article':
                messages.append('Article ' + str(ancestor['order']))
            if ancestor['type'] == 'bill-header1':
                messages.append(int_to_roman(ancestor['order']))
            if ancestor['type'] == 'bill-header2':
                messages.append(unicode(ancestor['order']) + u'°')

        node['commitMessage'] = ', '.join(messages[::-1])
