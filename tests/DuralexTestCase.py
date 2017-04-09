# -*- coding: utf-8 -*-

import unittest
import sys
import os
import json
import difflib

sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), '..'))

import duralex.alinea_parser as parser
import duralex.alinea_lexer as lexer

from duralex.DeleteEmptyChildrenVisitor import DeleteEmptyChildrenVisitor
from duralex.DeleteParentVisitor import DeleteParentVisitor

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
        if not 'children' in ast:
            ast['children'] = []
        for child in ast['children']:
            self.add_children(child)
        return ast

    def make_ast(self, ast):
        ast = self.add_parent(ast)
        ast = self.add_children(ast)
        return ast

    def call_visitor(self, visitor, ast):
        self.add_parent(ast)
        visitor().visit(ast)
        DeleteParentVisitor().visit(ast)
        return ast

    def assertEqualAST(self, a, b):
        DeleteParentVisitor().visit(a)
        DeleteEmptyChildrenVisitor().visit(a)
        DeleteParentVisitor().visit(b)
        DeleteEmptyChildrenVisitor().visit(b)

        a = json.dumps(a, sort_keys=True, indent=2, ensure_ascii=False).encode('utf-8')
        b = json.dumps(b, sort_keys=True, indent=2, ensure_ascii=False).encode('utf-8')

        diff = difflib.unified_diff(a.splitlines(), b.splitlines(), fromfile='computed', tofile='expected')
        diff_lines = list(diff)
        self.assertEqual(len(diff_lines), 0, self.pretty_diff_output(diff_lines))
