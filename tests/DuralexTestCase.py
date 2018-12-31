# -*- coding: utf-8 -*-

import unittest
import sys
import os
import json
import difflib
import uuid

sys.path.insert(0, os.path.join(os.path.realpath(os.path.dirname(__file__)), '..'))

import duralex.alinea_parser as parser
import duralex.alinea_lexer as lexer
import duralex.tree

from duralex.DeleteEmptyChildrenVisitor import DeleteEmptyChildrenVisitor
from duralex.DeleteParentVisitor import DeleteParentVisitor
from duralex.DeleteUUIDVisitor import DeleteUUIDVisitor
from duralex.AddParentVisitor import AddParentVisitor
from duralex.ResolveLookbackReferencesVisitor import ResolveLookbackReferencesVisitor

from unittest import main
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

    def call_parse_func(self, fn, data, tree=None):
        if not tree:
            tree = duralex.tree.create_node(None, {})
        fn(lexer.tokenize(data), 0, tree)
        return tree

    def add_parent(self, tree):
        AddParentVisitor().visit(tree)
        return tree

    def add_children(self, tree):
        if 'children' not in tree:
            tree['children'] = []
        for child in tree['children']:
            self.add_children(child)
        return tree

    def add_uuid(self, tree):
        if 'uuid' not in tree:
            tree['uuid'] = str(uuid.uuid4())
        for child in tree['children']:
            self.add_uuid(child)
        return tree

    def make_tree(self, tree):
        tree = self.add_parent(tree)
        tree = self.add_children(tree)
        tree = self.add_uuid(tree)
        return tree

    def call_visitor(self, visitor, tree):
        tree = self.make_tree(tree)
        visitor().visit(tree)
        return tree

    def assertEqualAST(self, a, b):
        ResolveLookbackReferencesVisitor().visit(a)
        DeleteParentVisitor().visit(a)
        DeleteEmptyChildrenVisitor().visit(a)
        DeleteUUIDVisitor().visit(a)
        ResolveLookbackReferencesVisitor().visit(b)
        DeleteParentVisitor().visit(b)
        DeleteEmptyChildrenVisitor().visit(b)
        DeleteUUIDVisitor().visit(b)

        a = json.dumps(a, sort_keys=True, indent=2, ensure_ascii=False)
        b = json.dumps(b, sort_keys=True, indent=2, ensure_ascii=False)

        diff = difflib.unified_diff(a.splitlines(), b.splitlines(), fromfile='computed', tofile='expected')
        diff_lines = list(diff)
        self.assertEqual(len(diff_lines), 0, '\n' + a + self.pretty_diff_output(diff_lines))

# vim: set ts=4 sw=4 sts=4 et:
