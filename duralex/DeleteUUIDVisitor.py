from duralex.AbstractVisitor import AbstractVisitor

class DeleteUUIDVisitor(AbstractVisitor):
    def visit_node(self, node):
        if 'uuid' in node:
            del node['uuid']

        super(DeleteUUIDVisitor, self).visit_node(node)
