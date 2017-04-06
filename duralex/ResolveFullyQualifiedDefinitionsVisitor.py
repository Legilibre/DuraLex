from duralex.alinea_parser import *

from AbstractVisitor import AbstractVisitor

class ResolveFullyQualifiedDefinitionsVisitor(AbstractVisitor):
    def visit_node(self, node):
        self.resolve_fully_qualified_definitions(node)
        super(ResolveFullyQualifiedDefinitionsVisitor, self).visit_node(node)

    def resolve_fully_qualified_definitions(self, node):
        def_types = [
            'alinea',
            'sentence'
        ]

        if 'type' in node and node['type'] == 'edit':
            def_nodes = filter_nodes(node, lambda x : x['type'] in def_types)
            # if we have more than 1 definition in a single edit, we assume:
            # - they have different types
            # - the final type of definition is the combination of all those types
            if len(def_nodes) > 1:
                content_nodes = filter(lambda x : len(x['children']) > 0, def_nodes)
                type_nodes = filter(lambda x : len(x['children']) == 0, def_nodes)
                types = []
                for type_node in type_nodes:
                    remove_node(node, type_node)
                    types.append(type_node)
                    del type_node['count']
                    # if 'count' in type_node and type_node['count'] == len(content_nodes):
                    # FIXME: else we should issue a warning because the count doesn't match and the type qualifier cannot
                    # apply
                for content_node in content_nodes:
                    children = []
                    for child in content_node['children']:
                        children.append(child)
                        remove_node(content_node, child)
                    remove_node(node, content_node)
                    sorted_types = sorted(types + [content_node], key=lambda x : def_types.index(x['type']))
                    type_node = node
                    for sorted_type in sorted_types:
                        t = copy_node(sorted_type)
                        push_node(type_node, t)
                        type_node = t
                    for child in children:
                        push_node(type_node, child)
