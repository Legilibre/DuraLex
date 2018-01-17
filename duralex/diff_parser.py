# -*- coding=utf-8 -*-

import re

from unidiff import PatchSet

import duralex.tree

def parse(data, tree):
    patches = PatchSet.from_string(data)
    for patch in patches:
        parse_patch(patch, tree)

def parse_article_reference(patch, tree):
    law_id = parse_law_id(patch.source_file)
    law_ref = None
    if law_id:
      law_ref = duralex.tree.create_node(tree, {
          'type': duralex.tree.TYPE_LAW_REFERENCE,
          'id': parse_law_id(patch.source_file),
      })

    article_id = parse_article_id(patch.source_file)
    article_ref = None
    if article_id:
      article_ref = duralex.tree.create_node(law_ref or tree, {
          'type': duralex.tree.TYPE_ARTICLE_REFERENCE,
          'id': article_id,
      })

    return law_ref or article_ref

def parse_law_id(filename):
    match = re.search(r"loi_([-0-9]+)", filename)

    return match.group(1) if match else False

def parse_article_id(filename):
    match = re.search(r"Article_([-0-9]+)\.", filename)

    return match.group(1) if match else False

def parse_patch(patch, tree):
    amendment = duralex.tree.create_node(tree, {
        'type': duralex.tree.TYPE_AMENDMENT,
        'id': '1',
    })
    article_ref = parse_article_reference(patch, None)

    if patch.target_file == '/dev/null':
        # The patch.source_file has been deleted.
        edit = duralex.tree.create_node(amendment, {
            'type': duralex.tree.TYPE_EDIT,
            'editType': 'delete',
        })
        duralex.tree.push_node(edit, article_ref)
    elif patch.source_file == '/dev/null':
        # The patch.target_file has been added.
        edit = duralex.tree.create_node(amendment, {
            'type': duralex.tree.TYPE_EDIT,
            'editType': 'add',
        })
        duralex.tree.push_node(edit, article_ref)
    else:
        for hunk in patch:
            parse_hunk(hunk, amendment, article_ref)

def parse_hunk(hunk, parent, ref):
    line_type = ''
    edit = None
    word = None

    for line in hunk:
        if line.line_type != line_type:
            if line.line_type == '\\':
                # FIXME: handle "\ No newline at end of file"?
                continue

            if edit:
                duralex.tree.push_node(parent, edit)
                word = None

            edit = duralex.tree.create_node(None, {
                'type': duralex.tree.TYPE_EDIT,
            })
            if ref:
              duralex.tree.push_node(edit, duralex.tree.copy_node(ref))

            if line.line_type == '+':
                edit['editType'] = 'add'
                if not word:
                    word = duralex.tree.create_node(edit, {
                        'type': duralex.tree.TYPE_WORD_DEFINITION,
                    })
                quote = duralex.tree.create_node(word, {
                    'type': duralex.tree.TYPE_QUOTE,
                    'words': line.value,
                })
            elif line.line_type == '-':
                edit['editType'] = 'delete'
                if not word:
                    word = duralex.tree.create_node(edit, {
                        'type': duralex.tree.TYPE_WORD_REFERENCE,
                    })
                quote = duralex.tree.create_node(word, {
                    'type': duralex.tree.TYPE_QUOTE,
                    'words': line.value,
                })
            line_type = line.line_type
    if edit:
        duralex.tree.push_node(parent, edit)
