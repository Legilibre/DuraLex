import duralex.tree as tree

class AbstractVisitor(object):
    def __init__(self):
        self.visitors = {
            tree.TYPE_EDIT: self.visit_edit_node,
            tree.TYPE_CODE_REFERENCE: self.visit_code_reference_node,
            tree.TYPE_BOOK_REFERENCE: self.visit_book_reference_node,
            tree.TYPE_LAW_REFERENCE: self.visit_law_reference_node,
            tree.TYPE_TITLE_REFERENCE: self.visit_title_reference_node,
            tree.TYPE_ARTICLE_REFERENCE: self.visit_article_reference_node,
            tree.TYPE_HEADER1_REFERENCE: self.visit_header1_reference_node,
            tree.TYPE_HEADER2_REFERENCE: self.visit_header2_reference_node,
            tree.TYPE_HEADER3_REFERENCE: self.visit_header3_reference_node,
            tree.TYPE_ALINEA_REFERENCE: self.visit_alinea_reference_node,
            tree.TYPE_SENTENCE_REFERENCE: self.visit_sentence_reference_node,
            tree.TYPE_WORD_REFERENCE: self.visit_words_reference_node,
            tree.TYPE_WORD_DEFINITION: self.visit_words_definition_node,
            tree.TYPE_ARTICLE_DEFINITION: self.visit_article_definition_node,
            tree.TYPE_QUOTE: self.visit_quote_node,
            tree.TYPE_BILL_ARTICLE_REFERENCE: self.visit_bill_article_reference_node,
            tree.TYPE_BILL_ARTICLE: self.visit_bill_article_node,
        }

    def visit_code_reference_node(self, node, post):
        pass

    def visit_book_reference_node(self, node, post):
        pass

    def visit_law_reference_node(self, node, post):
        pass

    def visit_title_reference_node(self, node, post):
        pass

    def visit_article_reference_node(self, node, post):
        pass

    def visit_header1_reference_node(self, node, post):
        pass

    def visit_header2_reference_node(self, node, post):
        pass

    def visit_header3_reference_node(self, node, post):
        pass

    def visit_alinea_reference_node(self, node, post):
        pass

    def visit_sentence_reference_node(self, node, post):
        pass

    def visit_words_reference_node(self, node, post):
        pass

    def visit_edit_node(self, node, post):
        pass

    def visit_words_definition_node(self, node, post):
        pass

    def visit_article_definition_node(self, node, post):
        pass

    def visit_quote_node(self, node, post):
        pass

    def visit_bill_article_reference_node(self, node, post):
        pass

    def visit_bill_article_node(self, node, post):
        pass

    def visit_node(self, node):
        if 'type' in node and node['type'] in self.visitors:
            self.visitors[node['type']](node, False)

        if 'children' in node:
            for child in node['children']:
                self.visit_node(child)

        if 'type' in node and node['type'] in self.visitors:
            self.visitors[node['type']](node, True)

    def visit(self, node):
        self.visit_node(node)
