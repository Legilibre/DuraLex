from duralex.AbstractVisitor import AbstractVisitor

import duralex.tree as tree

class SwapDefinitionAndReferenceVisitor(AbstractVisitor):
    def visit_edit_node(self, node, post):
        defs = filter(lambda n: tree.is_definition(n), node['children'])

        for d in defs:
            tree.remove_node(node, d)
            tree.push_node(node, d)
