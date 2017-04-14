from duralex.alinea_parser import *

from AbstractVisitor import AbstractVisitor

import node_type

class SortReferencesVisitor(AbstractVisitor):
    def visit_node(self, node):
        if not self.sort_references(node):
            super(SortReferencesVisitor, self).visit_node(node)

    def sort_references(self, node):
        root_refs = filter_nodes(node, lambda n: node_type.is_reference(n) and 'parent' in n and (not node_type.is_reference(n['parent'])))

        if len(root_refs) == 0:
            return False

        for root_ref in root_refs:
            root_ref_parent = root_ref['parent']
            refs = filter_nodes(root_ref, lambda n: node_type.is_reference(n))
            sorted_refs = sorted(refs, key=lambda r: node_type.REFERENCE.index(r['type']))
            filtered_refs = [sorted_refs[0]]
            for ref in sorted_refs:
                if 'parent' in ref:
                    remove_node(ref['parent'], ref)
                    if ref['type'] != filtered_refs[-1]['type']:
                        filtered_refs.append(ref)
            for i in range(0, len(filtered_refs)):
                ref = filtered_refs[i]
                if i == 0:
                    push_node(root_ref_parent, ref)
                else:
                    push_node(filtered_refs[i - 1], ref)

        return True
