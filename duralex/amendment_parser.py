# -*- coding: utf-8 -*-

import duralex.alinea_lexer as lexer

from duralex.bill_parser import clean_html
from duralex.tree import *
from duralex.alinea_parser import is_number_word, word_to_number, is_number, parse_int, parse_alineas

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
        'id': data['numero'],
        'content': text,
        'status': AMENDMENT_STATUS[data['sort'].lower()],
        'description': clean_html(data['expose']),
        'signatories': [{'name': s.strip()} for s in data['signataires'].split(', ')],
        'url': data['source']
    })

    # The "subject" declares the target bill article reference for this admendment.
    # That reference will be referenced later on using syntaxes such as "cet article" ("this article").
    parse_subject(tokens, 0, node)
    parse_alineas(node['content'], node)
    # If the admendment content actually need that bill article reference, they already have it copied by now.
    # So we simply we remove it.
    remove_node(node, node['children'][0])

    return node

def parse_subject(tokens, i, parent):
    node = create_node(parent, {
        'type': TYPE_BILL_ARTICLE_REFERENCE
    })

    i = parse_ref_position(tokens, i, node)

    # ART. PREMIER
    if tokens[i] == 'ART' and is_number_word(tokens[i + 3]):
        node['order'] = word_to_number(tokens[i + 3])
        i += lexer.skip_to_end_of_line(tokens, i)
    # ART. {order}
    elif tokens[i] == 'ART' and is_number(tokens[i + 3]):
        node['order'] = parse_int(tokens[i + 3])
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
