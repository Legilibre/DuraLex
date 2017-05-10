# -*- coding: utf-8 -*-

import alinea_lexer as lexer

from bill_parser import clean_html
from duralex.tree import *
from alinea_parser import is_number_word, word_to_number, is_number, parse_int, parse_alineas

AMENDMENT_STATUS = {
    u'rejeté': 'rejected',
    u'retiré': 'removed',
    u'non soutenu': 'undefended',
    u'retiré avant séance': 'removed',
    u'adopté': 'approved'
}

def parse(data, tree):
    amendements = []
    # ast = create_node(ast, {'type': 'amendments'})
    for amendement in data['amendements']:
        amendements.append(parse_amendment(amendement['amendement'], tree))
    return tree

def parse_amendment(data, parent):
    subject = data['sujet']
    text = clean_html(data['texte'])

    tokens = lexer.tokenize(subject + '\n' + text)
    node = create_node(parent, {
        'type': 'amendment',
        'content': text,
        'status': AMENDMENT_STATUS[data['sort'].lower()],
        'description': clean_html(data['expose']),
        'signatories': [s.strip() for s in data['signataires'].split(', ')]
    })

    # The "subject" declares the article referenced by the admendment as a whole.
    # We create a "fake" 'edit' node with the corresponding 'article-reference' node
    # and the ResolveFullyQualifiedReferencesVisitor will take care of properly transforming this:
    #
    # - amendment
    #   - edit <- our "fake" 'edit' node
    #     - article-reference <- the 'article-reference' node coming from the "subject"
    #   - edit <- the actual 'edit' node coming from the admendment text
    #     - *-reference
    #
    # into this:
    #
    # - amendment
    #   - edit <- the actual 'edit' node coming from the admendment text
    #     - article-reference <- the 'article-reference' node coming from the "subject"
    #       - *-reference
    fake_edit = create_node(node, {'type': 'edit', 'editType': 'edit'})
    parse_subject(tokens, 0, fake_edit)
    parse_alineas(node['content'], node)

    return node

def parse_subject(tokens, i, parent):
    node = create_node(parent, {
        'type': 'article-reference'
    })

    i = parse_ref_position(tokens, i, node)

    # ART. PREMIER
    if tokens[i] == 'ART' and is_number_word(tokens[i + 3]):
        node['id'] = str(word_to_number(tokens[i + 3]))
        i += lexer.skip_to_end_of_line(tokens, i)
    # ART. {id}
    elif tokens[i] == 'ART' and is_number(tokens[i + 3]):
        node['id'] = tokens[i + 3]
        i += lexer.skip_to_end_of_line(tokens, i)

    return i

def parse_ref_position(tokens, i, node):
    if i >= len(tokens):
        return

    if tokens[i] == u'AVANT':
        node['position'] = u'before'
        i += 2
    elif tokens[i] == u'APRÈS':
        node['position'] = u'after'
        i += 2

    return i
