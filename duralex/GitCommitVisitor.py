# -*- coding: utf-8 -*-

from AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *

import duralex.node_type

import subprocess
import os

class GitCommitVisitor(AbstractVisitor):
    def visit_article_reference_node(self, node, post):
        if self.commitMessage and self.repository:
            process = subprocess.Popen(
                [
                    'git',
                    '-C', self.repository,
                    'commit',
                    os.path.basename(node['filename']),
                    '-m', self.commitMessage,
                    '--author="DuraLex <duralex@legilibre.fr>"'
                ],
                # shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            out, err = process.communicate()
            print(''.join(out))

    def visit_node(self, node):
        if 'repository' in node:
            self.repository = node['repository'];
        super(GitCommitVisitor, self).visit_node(node)

    def visit_edit_node(self, node, post):
        if post:
            return

        if 'commitMessage' in node:
            self.commitMessage = node['commitMessage']
        else:
            self.commitMessage = ''

        if 'diff' in node:
            process = subprocess.Popen(
                'patch -p0',
                shell=True,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            out, err = process.communicate(input=node['diff'].encode('utf-8') + '\n')
