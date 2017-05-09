from AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *

import duralex.tree

class ForkReferenceVisitor(AbstractVisitor):
    def visit_node(self, node):
        if duralex.tree.is_reference(node) and 'children' in node and len(node['children']) > 1:
            ref_nodes = filter(lambda n: duralex.tree.is_reference(n), node['children'])
            for i in range(1, len(ref_nodes)):
                ref = ref_nodes[i]
                fork = copy_node(node, recursive=False)
                remove_node(node, ref)
                push_node(fork, ref)
                push_node(node['parent'], fork)

        super(ForkReferenceVisitor, self).visit_node(node)
