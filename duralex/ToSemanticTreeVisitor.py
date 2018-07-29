# -*- coding: utf-8 -*-

import logging
import parsimonious

from duralex.tree import *

LOGGER = logging.getLogger('ToSemanticTreeVisitor')


class ToSemanticTreeVisitor(parsimonious.NodeVisitor):

    """
    Translate a Parsimonious tree into a DuraLex tree.

    This translation is described in the dict table, in which the keys are the
    rules names in Parsimonious and the values are dicts describing DuraLex
    nodes. When this dict has a key 'type', it is create a new DuraLex node,
    else the properties set are added to the parent DuraLex node. It can be
    set some property in DuraLex node with the key 'property' and the value
    the name of the property. The value of the property set is by default the
    text of the Parsimonious node, but it can be set some fixed text with the
    property 'value'. Some replacements on this text can be achived.

    The relative order of the DuraLex tree remains the same than the
    Parsimonious tree, i.e. if a node B is a child of node A in Parsimonious,
    the corresponding node of B in DuraLex tree will be a child of the
    corresponding node of A in DuraLex tree.

    Internally, nodes are created bottom-up and the parent declares its
    children as children. A side-effect is: some child nodes only contain
    properties whithout type: these nodes should be merged into the parent
    because properties are carried on the parent and then these nodes should
    be deleted.
    """

    def __init__(self, table):

        self.table = table

    def attach(self, dparent, ptree):

        dtree, properties = self.visit(ptree)
        dparent.update(properties)
        if dtree:
            push_node(dparent, dtree)

    def generic_visit(self, pnode, children):

        rule_name = pnode.expr_name

        dnode = None
        dchildren = [child[0] for child in children if child[0]]
        dproperties = {k: v for child in children for k, v in child[1].items()}

        if rule_name in self.table:

            rule = self.table[rule_name]

            text = pnode.text
            if 'value' in rule:
                text = rule['value']
            if 'replace' in rule:
                text = rule['replace'](text)
            if 'property' in rule:
                dproperties[rule['property']] = text

            if 'type' in rule:
                dproperties['type'] = rule['type']
                dnode = create_node(None, dproperties)
                for dchild in dchildren:
                    push_node(dnode, dchild)
                dproperties = {}

        elif len(dchildren) > 1:
            dnode = create_node(None, {})
            for dchild in dchildren:
                push_node(dnode, dchild)

        elif len(dchildren) == 1:
            dnode = dchildren[0]

        return (dnode, dproperties)

# vim: set ts=4 sw=4 sts=4 et:
