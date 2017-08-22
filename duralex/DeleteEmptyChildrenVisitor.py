from duralex.AbstractVisitor import AbstractVisitor

class DeleteEmptyChildrenVisitor(AbstractVisitor):
    def visit_node(self, node):
        if 'children' in node and len(node['children']) == 0:
            del node['children']

        super(DeleteEmptyChildrenVisitor, self).visit_node(node)
