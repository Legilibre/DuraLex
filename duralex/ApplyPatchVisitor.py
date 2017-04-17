# -*- coding: utf-8 -*-

from AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *

import subprocess
import os

class ApplyPatchVisitor(AbstractVisitor):
    def visit_edit_node(self, node, post):
        if post:
            return

        if 'diff' in node:
            process = subprocess.Popen(
                'patch -p0 --remove-empty-files --ignore-whitespace',
                shell=True,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            out, err = process.communicate(input=node['diff'].encode('utf-8') + '\n')
