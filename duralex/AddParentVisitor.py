# -*- coding=utf-8 -*-

from AbstractVisitor import AbstractVisitor

class AddParentVisitor(AbstractVisitor):
    def __init__(self):
        self.parent = []

        super(AddParentVisitor, self).__init__()

    def visit_node(self, node):
        if 'parent' not in node and len(self.parent):
            node['parent'] = self.parent[-1]

        self.parent.append(node)

        super(AddParentVisitor, self).visit_node(node)

        del self.parent[-1]
