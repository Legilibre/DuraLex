from duralex.AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *

import duralex.tree

# Turn a reference tree into two (or more) reference lists
class ForkReferenceVisitor(AbstractVisitor):
    def visit_node(self, node):
        if duralex.tree.is_reference(node) and 'children' in node and len(node['children']) > 1:
            ref_nodes = [n for n in node['children'] if duralex.tree.is_reference(n)]
            for i in range(1, len(ref_nodes)):
                ref = ref_nodes[i]
                fork = copy_node(node, recursive=False)
                remove_node(node, ref)
                push_node(fork, ref)
                push_node(node['parent'], fork)
                # Up to this point, we've forked only one node: we need to fork its parent,
                # and the parent of its parent, etc...
                # To make this easier, we simply recursively call the ForkReferenceVisitor:
                # the fork will bubble up to the root until the fork is complete.
                ForkReferenceVisitor().visit(get_root(fork))

        super(ForkReferenceVisitor, self).visit_node(node)
