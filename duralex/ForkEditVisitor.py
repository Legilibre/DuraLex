from AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *

class ForkEditVisitor(AbstractVisitor):
    def visit_node(self, node):
        if ('type' in node and node['type'] == 'edit' and 'children' in node
            and len(filter(lambda n: n['type'].endswith('-reference'), node['children'])) > 1):
            for i in range(1, len(node['children'])):
                ref = node['children'][i]
                fork = copy_node(node, recursive=False)
                remove_node(node, ref)
                push_node(fork, ref)
                push_node(node['parent'], fork)

        super(ForkEditVisitor, self).visit_node(node)
