from AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *

import node_type

class ForkEditVisitor(AbstractVisitor):
    def visit_node(self, node):
        if 'type' in node and node['type'] == 'edit' and 'children' in node and len(node['children']) > 1:
            ref_nodes = filter(lambda n: node_type.is_reference(n), node['children'])
            def_nodes = filter(lambda n: node_type.is_definition(n), node['children'])
            edit_node = copy_node(node, recursive=False)
            parent = node['parent']
            remove_node(parent, node)
            for ref_node in ref_nodes:
                if len(def_nodes) > 0:
                    for def_node in def_nodes:
                        ref_node = copy_node(ref_node)
                        def_node = copy_node(def_node)
                        fork = copy_node(edit_node)
                        push_node(fork, ref_node)
                        push_node(fork, def_node)
                        push_node(parent, fork)
                else:
                    ref_node = copy_node(ref_node)
                    fork = copy_node(edit_node)
                    push_node(fork, ref_node)
                    push_node(parent, fork)
        else:
            super(ForkEditVisitor, self).visit_node(node)
