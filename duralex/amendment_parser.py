# -*- coding: utf-8 -*-

import alinea_lexer as lexer

from bill_parser import clean_html
from ast import *
from alinea_parser import is_number_word, word_to_number, is_number, parse_int, parse_alineas

AMENDMENT_STATUS = {
    u'rejeté': 'rejected',
    u'retiré': 'removed',
    u'non soutenu': 'undefended',
    u'retiré avant séance': 'removed',
    u'adopté': 'approved'
}

def parse(data, ast):
    amendements = []
    # ast = create_node(ast, {'type': 'amendments'})
    for amendement in data['amendements']:
        amendements.append(parse_amendment(amendement, ast))
    return ast

import re

def parse_amendment(data, node):
    subject = data['amendement']['sujet']
    text = clean_html(data['amendement']['texte'])

    tokens = lexer.tokenize(subject + '\n' + text)
    node = create_node(node, {
        'type': 'amendment',
        'content': text,
        'status': AMENDMENT_STATUS[data['amendement']['sort'].lower()],
        'description': clean_html(data['amendement']['expose']),
        'signatories': [s.strip() for s in data['amendement']['signataires'].split(', ')]
    })

    parse_subject(tokens, 0, node)
    parse_alineas(node['content'], node)

    return node

def parse_subject(tokens, i, parent):
    node = create_node(parent, {
        'type': 'article-reference'
    })

    i = parse_ref_position(tokens, i, node)

    # ART. PREMIER
    if tokens[i] == 'ART' and is_number_word(tokens[i + 3]):
        node['id'] = word_to_number(tokens[i + 3])
        i += lexer.skip_to_end_of_line(tokens, i)
    # ART. {id}
    elif tokens[i] == 'ART' and is_number(tokens[i + 3]):
        node['id'] = parse_int(tokens[i + 3])
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
