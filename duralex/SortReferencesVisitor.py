from duralex.alinea_parser import *

from AbstractVisitor import AbstractVisitor

class SortReferencesVisitor(AbstractVisitor):
    def visit_node(self, node):
        if not self.sort_references(node):
            super(SortReferencesVisitor, self).visit_node(node)

    def sort_references(self, node):
        root_refs = filter_nodes(node, lambda n: 'type' in n and n['type'] in AbstractVisitor.REF_TYPES and 'parent' in n and ('type' not in n['parent'] or n['parent']['type'] not in AbstractVisitor.REF_TYPES))

        if len(root_refs) == 0:
            return False

        for root_ref in root_refs:
            root_ref_parent = root_ref['parent']
            refs = filter_nodes(root_ref, lambda n: 'type' in n and n['type'] in AbstractVisitor.REF_TYPES)
            sorted_refs = sorted(refs, key=lambda r: AbstractVisitor.REF_TYPES.index(r['type']))
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
