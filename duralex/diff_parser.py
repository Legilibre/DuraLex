# -*- coding=utf-8 -*-

import re

from unidiff import PatchSet

import duralex.tree

def parse(data, tree):
    patches = PatchSet.from_string(data)
    for patch in patches:
        parse_patch(patch, tree)

def parse_article_reference(patch, tree):
    law_ref = duralex.tree.create_node(tree, {
        'type': duralex.tree.TYPE_LAW_REFERENCE,
        'id': parse_law_id(patch.source_file),
    })

    article_ref = duralex.tree.create_node(law_ref, {
        'type': duralex.tree.TYPE_ARTICLE_REFERENCE,
        'id': parse_article_id(patch.source_file),
    })

    return law_ref

def parse_law_id(filename):
    return re.search(r"loi_([-0-9]+)", filename).group(1)

def parse_article_id(filename):
    return re.search(r"Article_([-0-9]+)\.", filename).group(1)

def parse_patch(patch, tree):
    bill_article = duralex.tree.create_node(tree, {
        'type': duralex.tree.TYPE_BILL_ARTICLE,
        'order': 1,
    })
    law_ref = parse_article_reference(patch, bill_article)

    if patch.target_file == '/dev/null':
        # The patch.source_file has been deleted.
        edit = duralex.tree.create_node(bill_article, {
            'type': duralex.tree.TYPE_EDIT,
            'editType': 'delete',
        })
        duralex.tree.push_node(edit, law_ref)
        pass
    else:
        for hunk in patch:
            for line in hunk:
                parse_line(line, bill_article)

def parse_line(line, tree):
    if line.line_type == '+':
        edit = duralex.tree.create_node(tree, {
            'type': duralex.tree.TYPE_EDIT,
            'editType': 'add',
        })

        word_def = duralex.tree.create_node(edit, {
            'type': duralex.tree.TYPE_WORD_DEFINITION,
        })

        quote = duralex.tree.create_node(word_def, {
            'type': duralex.tree.TYPE_QUOTE,
            'words': line.value,
        })
    elif line.line_type == '-':
        edit = duralex.tree.create_node(tree, {
            'type': duralex.tree.TYPE_EDIT,
            'editType': 'remove',
        })

        word_def = duralex.tree.create_node(edit, {
            'type': duralex.tree.TYPE_WORD_DEFINITION,
        })

        quote = duralex.tree.create_node(word_def, {
            'type': duralex.tree.TYPE_QUOTE,
            'words': line.value,
        })
