# -*- coding: utf-8 -*-

from duralex.AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *

class ResolveLookbackReferencesVisitor(AbstractVisitor):
    def visit_lookback_reference_node(self, node, post):
        if post:
            return

        if len(node['children']) > 0:
            refs = filter_nodes(
                get_root(node),
                lambda n: compare_nodes(n, node) or 'type' in n and n['type'] == node['children'][0]['type']
            )
        else:
            refs = filter_nodes(get_root(node), is_reference)

        for i in range(0, len(refs)):
            if compare_nodes(refs[i], node):
                return self.resolve(node, copy_node(refs[i - 1]))

    def resolve(self, node, resolved_ref):
        if len(node['children']) > 0:
            for child in node['children'][0]['children']:
                push_node(resolved_ref, child)
        push_node(node['parent'], resolved_ref)
        remove_node(node['parent'], node)
