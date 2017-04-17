class AbstractVisitor(object):
    def __init__(self):
        self.visitors = {
            'edit': self.visit_edit_node,
            'code-reference': self.visit_code_reference_node,
            'book-reference': self.visit_book_reference_node,
            'law-reference': self.visit_law_reference_node,
            'title-reference': self.visit_title_reference_node,
            'article-reference': self.visit_article_reference_node,
            'header1-reference': self.visit_header1_reference_node,
            'header2-reference': self.visit_header2_reference_node,
            'header3-reference': self.visit_header3_reference_node,
            'alinea-reference': self.visit_alinea_reference_node,
            'sentence-reference': self.visit_sentence_reference_node,
            'words-reference': self.visit_words_reference_node,
            'words': self.visit_words_definition_node,
            'quote': self.visit_quote_node
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

    def visit_quote_node(self, node, post):
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
