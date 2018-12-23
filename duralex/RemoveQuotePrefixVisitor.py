# -*- coding: utf-8 -*-

from duralex.AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *

class RemoveQuotePrefixVisitor(AbstractVisitor):
    __slots__ = ['articleId']

    def visit_article_definition_node(self, node, post):
        self.articleId = None
        if not post and 'id' in node:
            self.articleId = node['id']

    def visit_quote_node(self, node, post):
        if post:
            return

        # Art. {articleId}. -
        s = re.match(r'^Art\. (.*?)\. +[-‐‑‒–—―] +', node['words'])
        if s == None or self.articleId == None:
            return

        if self.articleId == re.sub(r'[-‐‑‒–—―]', '-', s.group(1)):
            node['words'] = re.sub(r'^Art\. .*?\. +[-‐‑–—] +', '', node['words'])
        else:
            raise Exception('Prefix "Art. {articleId}. - " in text different than previously declared article n°{articleId}, sounds strange')
