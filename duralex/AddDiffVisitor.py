# -*- coding: utf-8 -*-

import codecs
import re
import difflib
import sys
import os

import alinea_parser as parser
import node_type
import diff

from AbstractVisitor import AbstractVisitor

class AddDiffVisitor(AbstractVisitor):
    REGEXP = {
        'header1-reference'     : re.compile(r'(?=((\n|^)#\w(.|\n)*?)(\n#\w|$))', re.UNICODE),
        'header2-reference'     : re.compile(r'(?=((\n|^)##\w(.|\n)*?)(\n#{1,2}\w|$))', re.UNICODE),
        'header3-reference'     : re.compile(r'(?=((\n|^)###\w(.|\n)*?\n)(\n#{1,3}\w|$))', re.UNICODE),
        'alinea-reference'      : re.compile(r'^(.+)$', re.UNICODE | re.MULTILINE),
        'sentence-reference'    : re.compile(r'([A-ZÀÀÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏ].*?\.)', re.UNICODE),
        'words-reference'       : re.compile(r'(\b\w.*?\b)', re.UNICODE)
    }

    def __init__(self):
        self.filename = ''
        self.content = {}
        self.begin = 0;
        self.end = -1;
        super(AddDiffVisitor, self).__init__()

    def visit_alinea_reference_node(self, node, post):
        if post:
            return

        match = re.finditer(AddDiffVisitor.REGEXP['alinea-reference'], self.content[self.filename][self.begin:self.end])
        match = list(match)[node['order'] - 1]
        self.begin = match.start()
        self.end = match.start() + len(match.group(1))

    def visit_sentence_reference_node(self, node, post):
        if post:
            return

        match = re.finditer(AddDiffVisitor.REGEXP['sentence-reference'], self.content[self.filename][self.begin:self.end])
        match = list(match)[node['order'] - 1]
        self.begin = match.start()
        self.end = match.start() + len(match.group(1))

    def visit_words_reference_node(self, node, post):
        if post:
            return

        if 'children' in node and node['children'][0]['type'] == 'quote':
            self.begin += self.content[self.filename][self.begin:self.end].find(node['children'][0]['words'])
            self.end = self.begin + len(node['children'][0]['words'])

    def visit_article_reference_node(self, node, post):
        if post:
            return

        self.filename = node['filename'].encode('utf-8')
        if self.filename not in self.content:
            if os.path.isfile(self.filename):
                input_file = codecs.open(self.filename, mode="r", encoding="utf-8")
                self.content[self.filename] = input_file.read()
            else:
                self.content[self.filename] = ''
        self.begin = 0;
        self.end = len(self.content[self.filename])

    def visit_edit_node(self, node, post):
        if not post:
            self.begin = 0
            self.end = -1
            return

        old_content = self.content[self.filename]
        new_content = old_content

        if node['editType'] == 'replace':
            # FIXME: properly detect we're supposed to replace words?
            def_node = parser.filter_nodes(node, lambda x: x['type'] == 'words')[-1]
            new_content = old_content[0:self.begin] + def_node['children'][0]['words'] + old_content[self.end:]
        elif node['editType'] == 'delete':
            ref_node = parser.filter_nodes(node, lambda x: node_type.is_reference(x))[-1]
            new_content = old_content[0:self.begin] + old_content[self.end:]
        elif node['editType'] == 'edit':
            def_node = parser.filter_nodes(node, lambda x: x['type'] == 'words')[-1]
            new_content = old_content[0:self.begin] + def_node['children'][0]['words'] + old_content[self.end:]

        unified_diff = difflib.unified_diff(
            old_content.splitlines(),
            new_content.splitlines() if new_content != '' else [],
            tofile='\"' + self.filename + '\"',
            fromfile='\"' + self.filename + '\"'
        )
        unified_diff = [unicode(d[0:-1], 'utf-8') if isinstance(d, str) else d for d in unified_diff]
        if len(unified_diff) > 0:
            node['diff'] = '\n'.join(unified_diff)
            node['htmlDiff'] = diff.make_html_rich_diff(old_content, new_content, self.filename)

        self.content[self.filename] = new_content
