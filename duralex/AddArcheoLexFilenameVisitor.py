import os

from AbstractVisitor import AbstractVisitor

class AddArcheoLexFilenameVisitor(AbstractVisitor):
    @staticmethod
    def register(arg_parser):
        pass

    def __init__(self):
        self.base = 'data/'
        self.filename = ''
        self.path = ''

        super(AddArcheoLexFilenameVisitor, self).__init__()

    def visit_article_reference_node(self, node, post):
        if post:
            return

        self.path = os.path.join(self.path, 'Article_' + node['id'] + '.md')
        node['filename'] = self.path

    def visit_code_reference_node(self, node, post):
        if post:
            return

        self.path = os.path.join(self.path, node['codeName'])
        node['repository'] = self.path

    def visit_law_reference_node(self, node, post):
        if post:
            return

        self.path = os.path.join(self.path, 'loi_' + node['lawId'])
        node['repository'] = self.path

    def visit_node(self, node):
        if 'type' in node and node['type'] == 'edit':
            self.path = self.base;
        super(AddArcheoLexFilenameVisitor, self).visit_node(node)
