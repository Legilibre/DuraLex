from duralex.AbstractVisitor import AbstractVisitor

import duralex.tree as tree

class SwapDefinitionAndReferenceVisitor(AbstractVisitor):
    def visit_edit_node(self, node, post):
        if post:
            return
        
        defs = list(filter(tree.is_definition, node['children']))

        for d in defs:
            tree.remove_node(node, d)
            tree.push_node(node, d)

# vim: set ts=4 sw=4 sts=4 et:
