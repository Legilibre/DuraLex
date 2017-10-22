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
    amendment = duralex.tree.create_node(tree, {
        'type': duralex.tree.TYPE_AMENDMENT,
        'id': '1',
    })
    law_ref = parse_article_reference(patch, None)

    if patch.target_file == '/dev/null':
        # The patch.source_file has been deleted.
        edit = duralex.tree.create_node(amendment, {
            'type': duralex.tree.TYPE_EDIT,
            'editType': 'delete',
        })
        duralex.tree.push_node(edit, law_ref)
    elif patch.source_file == '/dev/null':
        # The patch.target_file has been added.
        edit = duralex.tree.create_node(amendment, {
            'type': duralex.tree.TYPE_EDIT,
            'editType': 'add',
        })
        duralex.tree.push_node(edit, law_ref)
    else:
        for hunk in patch:
            parse_hunk(hunk, amendment, law_ref)

def parse_hunk(hunk, parent, ref):
    line_type = ''
    edit = None
    word_def = None

    for line in hunk:
        if line.line_type != line_type:
            if edit:
                duralex.tree.push_node(parent, edit)
            edit = duralex.tree.create_node(None, {
                'type': duralex.tree.TYPE_EDIT,
            })
            duralex.tree.push_node(edit, duralex.tree.copy_node(ref))
            word_def = duralex.tree.create_node(edit, {
                'type': duralex.tree.TYPE_WORD_DEFINITION,
            })
            if line.line_type == '+':
                edit['editType'] = 'add'
            elif line.line_type == '-':
                edit['editType'] = 'delete'
            line_type = line.line_type

        quote = duralex.tree.create_node(word_def, {
            'type': duralex.tree.TYPE_QUOTE,
            'words': line.value,
        })

    if edit:
        duralex.tree.push_node(parent, edit)
