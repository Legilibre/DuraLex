from duralex.alinea_parser import *

from AbstractVisitor import AbstractVisitor

class ResolveFullyQualifiedReferencesVisitor(AbstractVisitor):
    def __init__(self):
        self.ctx = []
        super(ResolveFullyQualifiedReferencesVisitor, self).__init__()

    def visit_node(self, node):
        if not self.resolve_fully_qualified_references(node):
            super(ResolveFullyQualifiedReferencesVisitor, self).visit_node(node)

    def resolve_fully_qualified_references(self, node):
        # If we are on an edit node that has edit ancestors
        # if 'type' in node and len(filter(lambda x : x['type'] == 'edit', get_node_ancestors(node))) > 0:
        #     # FIXME
        #     None

        # If we have an 'edit' node in an 'edit' node, the parent gives its
        # context to its descendants.
        if (not duralex.tree.is_reference(node) and len(node['children']) >= 1 and node['children'][0]['type'] == 'edit'
            and node['children'][0]['editType'] == 'edit'
            and len(filter_nodes(node, lambda n: 'type' in n and n['type'] == 'edit')) > 1):
            context = node['children'][0]['children'][0]
            remove_node(node, node['children'][0])
            self.ctx.append([copy_node(ctx_node, False) for ctx_node in filter_nodes(context, lambda x: duralex.tree.is_reference(x))])
            for child in node['children']:
                self.visit_node(child)
            self.ctx.pop()
            return True
        # If we have a context and there is no ref type at all and we're not on a 'swap' edit
        elif len(self.ctx) > 0 and node['type'] == 'edit' and len(filter_nodes(node, lambda x : duralex.tree.is_reference(x))) == 0:
            n = [copy_node(item) for sublist in self.ctx for item in sublist]
            n = sorted(n, key=lambda x : duralex.tree.TYPE_REFERENCE.index(x['type']))
            unshift_node(node, n[0])
            for i in range(1, len(n)):
                unshift_node(n[i - 1], n[i])
            return True
        # If we have a context and we're on root ref type
        elif len(self.ctx) > 0 and duralex.tree.is_reference(node) and not duralex.tree.is_reference(node['parent']):
            n = [copy_node(item) for sublist in self.ctx for item in sublist]
            n = sorted(n, key=lambda x : duralex.tree.TYPE_REFERENCE.index(x['type']))
            unshift_node(node['parent'], n[0])
            for i in range(1, len(n)):
                unshift_node(n[i - 1], n[i])
            remove_node(node['parent'], node)
            if node['type'] == 'incomplete-reference':
                if 'position' in node:
                    n[len(n) - 1]['position'] = node['position']
            else:
                unshift_node(n[len(n) - 1], node)
            return True

        return False
