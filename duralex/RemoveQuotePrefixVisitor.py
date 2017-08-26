# -*- coding: utf-8 -*-

from duralex.AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *

class RemoveQuotePrefixVisitor(AbstractVisitor):
    def visit_quote_node(self, node, post):
        if post:
            return

        # Art. {articleId}. -
        node['words'] = re.sub(r'^Art\. .*?\. - ', '', node['words'], 0, re.UNICODE | re.MULTILINE)
