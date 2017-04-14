# -*- coding: utf-8 -*-

import unittest
import sys
import os
import json
import difflib
import uuid

sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), '..'))

import duralex.alinea_parser as parser
import duralex.alinea_lexer as lexer

from duralex.DeleteEmptyChildrenVisitor import DeleteEmptyChildrenVisitor
from duralex.DeleteParentVisitor import DeleteParentVisitor
from duralex.DeleteUUIDVisitor import DeleteUUIDVisitor

from colorama import init, Fore

init()

class DuralexTestCase(unittest.TestCase):
    def pretty_diff_output(self, lines):
        out = '\n'

        for line in lines:
            if line[0] == '-':
                out += Fore.RED + line
            elif line[0] == '+':
                out += Fore.GREEN + line
            else:
                out += Fore.RESET + line
            out = out + Fore.RESET + '\n'

        return out

    def call_parse_func(self, fn, data, ast=None):
        if not ast:
            ast = {'children':[]}
        fn(lexer.tokenize(data), 0, ast)
        # default_visitors(ast)
        return ast

    def add_parent(self, ast):
        if 'children' in ast:
            for child in ast['children']:
                if 'parent' not in child:
                    child['parent'] = ast
                self.add_parent(child)
        return ast

    def add_children(self, ast):
        if 'children' not in ast:
            ast['children'] = []
        for child in ast['children']:
            self.add_children(child)
        return ast

    def add_uuid(self, ast):
        if 'uuid' not in ast:
            ast['uuid'] = str(uuid.uuid4())
        for child in ast['children']:
            self.add_uuid(child)
        return ast

    def make_ast(self, ast):
        ast = self.add_parent(ast)
        ast = self.add_children(ast)
        ast = self.add_uuid(ast)
        return ast

    def call_visitor(self, visitor, ast):
        ast = self.make_ast(ast)
        visitor().visit(ast)
        return ast

    def assertEqualAST(self, a, b):
        DeleteParentVisitor().visit(a)
        DeleteEmptyChildrenVisitor().visit(a)
        DeleteUUIDVisitor().visit(a)
        DeleteParentVisitor().visit(b)
        DeleteEmptyChildrenVisitor().visit(b)
        DeleteUUIDVisitor().visit(b)

        a = json.dumps(a, sort_keys=True, indent=2, ensure_ascii=False).encode('utf-8')
        b = json.dumps(b, sort_keys=True, indent=2, ensure_ascii=False).encode('utf-8')

        diff = difflib.unified_diff(a.splitlines(), b.splitlines(), fromfile='computed', tofile='expected')
        diff_lines = list(diff)
        self.assertEqual(len(diff_lines), 0, '\n' + a + self.pretty_diff_output(diff_lines))
