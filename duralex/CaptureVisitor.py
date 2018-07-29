# -*- coding: utf-8 -*-

import parsimonious


class CaptureVisitor(parsimonious.NodeVisitor):

    """
    Capture some rules from a Parsimonious syntactic tree.
    """

    __slots__ = ['table', 'captures']

    def __init__( self, table ):
        """
        :param table:
            (dict|list|set) List of Parsimonious rule names to be captured.
        """
        self.table = table
        self.captures = {}

    def generic_visit( self, node, visited_children ):

        if node.expr_name in self.table:

            rule_name = node.expr_name
            self.captures[rule_name] = node.text

# vim: set ts=4 sw=4 sts=4 et:
