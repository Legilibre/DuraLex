# -*- coding: utf-8 -*-

import uuid

TYPE_HEADER1    = 'header1'
TYPE_HEADER2    = 'header2'
TYPE_HEADER3    = 'header3'
TYPE_ARTICLE    = 'article'
TYPE_AMENDMENT  = 'amendment'
TYPE_EDIT       = 'edit'
TYPE_QUOTE      = 'quote'

TYPE_TITLE_DEFINITION           = 'title-definition'
TYPE_ARTICLE_DEFINITION         = 'article-definition'
TYPE_HEADER1_DEFINITION         = 'header1-definition'
TYPE_HEADER2_DEFINITION         = 'header2-definition'
TYPE_HEADER3_DEFINITION         = 'header3-definition'
TYPE_SUBPARAGRAPH_DEFINITION    = 'subparagraph-definition'
TYPE_ALINEA_DEFINITION          = 'alinea-definition'
TYPE_SENTENCE_DEFINITION        = 'sentence-definition'
TYPE_MENTION_DEFINITION         = 'mention-definition'
TYPE_WORD_DEFINITION            = 'word-definition'

TYPE_DEFINITION = [
    TYPE_ARTICLE_DEFINITION,
    TYPE_HEADER1_DEFINITION,
    TYPE_HEADER2_DEFINITION,
    TYPE_HEADER3_DEFINITION,
    TYPE_ALINEA_DEFINITION,
    TYPE_SENTENCE_DEFINITION,
    TYPE_WORD_DEFINITION,
]

TYPE_CODE_REFERENCE         = 'code-reference'
TYPE_CODE_PART_REFERENCE    = 'code-part-reference'
TYPE_BOOK_REFERENCE         = 'book-reference'
TYPE_LAW_REFERENCE          = 'law-reference'
TYPE_TITLE_REFERENCE        = 'title-reference'
TYPE_CHAPTER_REFERENCE      = 'chapter-reference'
TYPE_SECTION_REFERENCE      = 'section-reference'
TYPE_SUBSECTION_REFERENCE   = 'subsection-reference'
TYPE_PARAGRAPH_REFERENCE    = 'paragraph-reference'
TYPE_ARTICLE_REFERENCE      = 'article-reference'
TYPE_HEADER1_REFERENCE      = 'header1-reference'
TYPE_HEADER2_REFERENCE      = 'header2-reference'
TYPE_HEADER3_REFERENCE      = 'header3-reference'
TYPE_ALINEA_REFERENCE       = 'alinea-reference'
TYPE_SENTENCE_REFERENCE     = 'sentence-reference'
TYPE_WORD_REFERENCE         = 'word-reference'
TYPE_INCOMPLETE_REFERENCE   = 'incomplete-reference'

TYPE_REFERENCE = [
    TYPE_CODE_REFERENCE,
    TYPE_CODE_PART_REFERENCE,
    TYPE_BOOK_REFERENCE,
    TYPE_LAW_REFERENCE,
    TYPE_TITLE_REFERENCE,
    TYPE_CHAPTER_REFERENCE,
    TYPE_SECTION_REFERENCE,
    TYPE_SUBSECTION_REFERENCE,
    TYPE_PARAGRAPH_REFERENCE,
    TYPE_ARTICLE_REFERENCE,
    TYPE_HEADER1_REFERENCE,
    TYPE_HEADER2_REFERENCE,
    TYPE_HEADER3_REFERENCE,
    TYPE_ALINEA_REFERENCE,
    TYPE_SENTENCE_REFERENCE,
    TYPE_WORD_REFERENCE,
    TYPE_INCOMPLETE_REFERENCE,
]

def unshift_node(parent, node):
    node['parent'] = parent
    if 'children' not in parent:
        parent['children'] = []
    parent['children'] = [node] + parent['children']

def push_node(parent, node):
    if 'parent' in node:
        remove_node(node['parent'], node)
    node['parent'] = parent
    if 'children' not in parent:
        parent['children'] = []
    parent['children'].append(node)

def create_node(parent, node):
    if parent:
        push_node(parent, node)
    node['children'] = []
    node['uuid'] = str(uuid.uuid4())

    return node

def compare_nodes(a, b):
    return a['uuid'] == b['uuid'] if 'uuid' in a and 'uuid' in b else a == b

def remove_node(parent, node):
    if not parent:
        raise Exception('invalid parent')
    if 'parent' not in node or node['parent'] != parent:
        raise Exception('parent node does not match')

    for i in range(0, len(parent['children'])):
        if compare_nodes(node, parent['children'][i]):
            del parent['children'][i]
            del node['parent']
            return True

    return False

def copy_node(node, recursive=True):
    c = node.copy()
    if 'uuid' in c:
        c['uuid'] = str(uuid.uuid4())
    if 'parent' in c:
        del c['parent']
    c['children'] = []
    if 'children' in node and recursive:
        for child in node['children']:
            push_node(c, copy_node(child))
    return c

def get_node_depth(node):
    if not 'parent' in node:
        return 0
    return 1 + get_node_depth(node['parent'])

def get_root(node):
    while 'parent' in node:
        node = node['parent']

    return node

def filter_nodes(root, fn):
    return filter_nodes_rec(root, fn, [])

def filter_nodes_rec(root, fn, results):
    if fn(root):
        results.append(root)

    if 'children' in root:
        for child in root['children']:
            filter_nodes_rec(child, fn, results)

    return results

def is_definition(node):
    return 'type' in node and node['type'] in TYPE_DEFINITION

def is_reference(node):
    return 'type' in node and node['type'] in TYPE_REFERENCE

def is_root(node):
    return 'parent' not in node
