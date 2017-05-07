# -*- coding: utf-8 -*-

import uuid

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
