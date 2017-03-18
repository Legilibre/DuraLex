from AbstractVisitor import AbstractVisitor

class DeleteParentVisitor(AbstractVisitor):
    def visit_node(self, node):
        if 'parent' in node:
            del node['parent']

        super(DeleteParentVisitor, self).visit_node(node)
