# -*- coding: utf-8 -*-

import logging
import parsimonious

from duralex import *

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

    WIP: the special key '_priority' is used to wrap some DuraLex instead of
    creating a list, e.g. for the expression "le deuxième alinéa et la
    troisième phrase du quatrième alinéa" where "troisième phrase" must be
    wrapped in "quatrième alinéa"; this specific case is (for now) triggered
    by a rule with key '_priority' (here "du" can carry such key).
    """

    def __init__(self, table):

        self.table = table

    def attach(self, dparent, ptree):

        """
        Main method to attach a new node in a DuraLex semantic tree when reading a Parsimonious syntactic tree.

        :param dparent:
            (dict) Parent DuraLex node where will be attached the new DuraLex node.
        :param ptree:
            (parsimonious.Node) Parsimonious tree; there should be some matching rules declared in the table.
        :returns:
            (dict|None) New DuraLex node if any, or None.
        """

        dtree, properties = self.visit(ptree)
        dparent.update(properties)
        if dtree:
            if 'type' in dtree and dtree['type'] == 'parsimonious-list-container':
                for dnode in list(dtree['children']):
                    push_node(dparent, dnode)
            else:
                push_node(dparent, dtree)
        return dtree

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
            if '_priority' in rule and rule['_priority'] == True:
                dproperties['_priority'] = True

            if 'type' in rule:
                dproperties['type'] = rule['type']
                dnode = create_node(None, dproperties)
                first = True
                hierarchical = False
                for dchild in dchildren:
                    if '_priority' in dchild:
                        if first:
                            raise Exception('hierarchical item without base item: unknown behaviour')
                        del dchild['_priority']
                        push_node(dchild, dnode)
                        dnode = dchild
                        hierarchical = True
                    else:
                        if hierarchical:
                            raise Exception('base item after a hierarchical item: unknown behaviour')
                        if 'type' in dchild and dchild['type'] == 'parsimonious-list-container':
                            for dsubchild in list(dchild['children']):
                                push_node(dnode, dsubchild)
                        else:
                            push_node(dnode, dchild)
                        first = False
                dproperties = {}

        elif len(dchildren) > 1:
            dnode = create_node(None, {'type': 'parsimonious-list-container'})
            first = True
            hierarchical = False
            for dchild in dchildren:
                if '_priority' in dchild and not first:
                    if first:
                        raise Exception('hierarchical item without base item: unknown behaviour')
                    del dchild['_priority']
                    push_node(dchild, dnode)
                    dnode = dchild
                else:
                    if hierarchical:
                        raise Exception('base item after a hierarchical item: unknown behaviour')
                    if 'type' in dchild and dchild['type'] == 'parsimonious-list-container':
                        for dsubchild in list(dchild['children']):
                            push_node(dnode, dsubchild)
                    else:
                        push_node(dnode, dchild)
                    first = False

        elif len(dchildren) == 1:
            dnode = dchildren[0]

        return (dnode, dproperties)

# vim: set ts=4 sw=4 sts=4 et:
