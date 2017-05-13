from duralex.alinea_parser import *

from AbstractVisitor import AbstractVisitor

import duralex.tree

class SortReferencesVisitor(AbstractVisitor):
    def visit_node(self, node):
        if not self.sort_references(node):
            super(SortReferencesVisitor, self).visit_node(node)

    def sort_references(self, node):
        root_refs = filter_nodes(node, lambda n: duralex.tree.is_reference(n) and 'parent' in n and (not duralex.tree.is_reference(n['parent'])))

        if len(root_refs) == 0:
            return False

        for root_ref in root_refs:
            root_ref_parent = root_ref['parent']
            refs = filter_nodes(root_ref, lambda n: duralex.tree.is_reference(n))
            sorted_refs = sorted(refs, key=lambda r: duralex.tree.TYPE_REFERENCE.index(r['type']))
            filtered_refs = [sorted_refs[0]]
            for ref in sorted_refs:
                if 'parent' in ref:
                    remove_node(ref['parent'], ref)
                    # the deepest *-reference of the same type wins
                    # FIXME: should we raise because we're not supposed to have the same *-reference twice?
                    if ref['type'] == filtered_refs[-1]['type']:
                        filtered_refs.pop()
                    filtered_refs.append(ref)
            for i in range(0, len(filtered_refs)):
                ref = filtered_refs[i]
                if i == 0:
                    push_node(root_ref_parent, ref)
                else:
                    push_node(filtered_refs[i - 1], ref)

        return True
