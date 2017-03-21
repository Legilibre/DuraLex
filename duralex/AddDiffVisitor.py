# -*- coding: utf-8 -*-

import codecs
import re
import difflib
import parser
import sys

from AbstractVisitor import AbstractVisitor

class AddDiffVisitor(AbstractVisitor):
    REGEXP = {
        'header1-reference': r'(?=((\n|^)#\w(.|\n)*?)(\n#\w|$))',
        'header2-reference': r'(?=((\n|^)##\w(.|\n)*?)(\n#{1,2}\w|$))',
        'header3-reference': r'(?=((\n|^)###\w(.|\n)*?\n)(\n#{1,3}\w|$))',
        'alinea-reference' : r'(?=(\n\n[^#].*?(\n\n|$)))',
        'sentence-reference' : r'([A-ZÀÀÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏ].*?\.)',
        'words-reference' : r'(\b\w.*?\b)'
    }

    def __init__(self):
        self.filename = ''
        self.content = {}
        self.begin = 0;
        self.end = -1;
        super(AddDiffVisitor, self).__init__()

    def visit_sentence_reference_node(self, node, post):
        if post:
            return

        match = re.finditer(re.compile(AddDiffVisitor.REGEXP['sentence-reference'], re.UNICODE), self.content[self.filename][self.begin:self.end])
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
            input_file = codecs.open(self.filename, mode="r", encoding="utf-8")
            self.content[self.filename] = input_file.read()
        self.begin = 0;
        self.end = len(self.content[self.filename]) - 1

    def visit_edit_node(self, node, post):
        if not post:
            self.begin = 0
            self.end = -1
            return

        old_content = self.content[self.filename]
        new_content = old_content

        if node['editType'] == 'replace':
            # FIXME: properly detect we're supposed to replace words
            defNode = parser.filter_nodes(node, lambda x: x['type'] == 'words')[-1]
            new_content = old_content[0:self.begin] + defNode['children'][0]['words'] + old_content[self.end:]

        diff = difflib.unified_diff(
            old_content.splitlines(),
            new_content.splitlines(),
            tofile='\"' + self.filename + '\"',
            fromfile='\"' + self.filename + '\"'
        )
        diff = [unicode(d[0:-1], 'utf-8') if isinstance(d, str) else d for d in diff]
        node['diff'] = "\n".join(diff)

        self.content[self.filename] = new_content
