# -*- coding=utf-8 -*-

from duralex.AbstractVisitor import AbstractVisitor

import duralex.tree as tree

# If an edit reference does not feature a code-reference or law-reference node, we won't be able to find the actual
# original text to apply the edits to. To fix this, this visitor will :
# - target only article-reference nodes with no law-reference and code-reference ancestor/descendant,
# - find, copy and insert as it's own child the first previous law-reference or code-reference (whichever comes first) in
#   reversed traversal 
class FixMissingCodeOrLawReferenceVisitor(AbstractVisitor):
    def __init__(self):
        self.law_or_code_ref = None
        super(FixMissingCodeOrLawReferenceVisitor, self).__init__()

    def visit_law_reference_node(self, node, post):
        if post:
            return
        self.law_or_code_ref = node

    def visit_code_reference_node(self, node, post):
        if post:
            return
        self.law_or_code_ref = node

    def visit_article_reference_node(self, node, post):
        if post:
            return
        ancestor_refs = [n for n in tree.get_node_ancestors(node) + tree.get_node_descendants(node) if
            not tree.is_root(n) and n['type'] in [tree.TYPE_CODE_REFERENCE, tree.TYPE_LAW_REFERENCE]
        ]
        # if we've found no reference
        if len(ancestor_refs) == 0:
            # we find the leaf in this subtree
            while len(node['children']) != 0:
                node = node['children'][0]
            if self.law_or_code_ref:
                tree.push_node(node, tree.copy_node(self.law_or_code_ref, False))
