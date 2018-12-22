# -*- coding: utf-8 -*-

import re

TOKEN_DELIMITERS = re.compile(u'(\xa0|\s|\(|\)|\.|\!|\'|’|,|")')
TOKEN_NEW_LINE = '\n'
TOKEN_SINGLE_QUOTE = u'\''
TOKEN_DOUBLE_QUOTE_OPEN = u'"'
TOKEN_DOUBLE_QUOTE_CLOSE = u'"'
TOKEN_MONTH_NAMES = [
    u'janvier',
    u'février',
    u'mars',
    u'avril',
    u'mai',
    u'juin',
    u'juillet',
    u'août',
    u'septembre',
    u'octobre',
    u'novembre',
    u'décembre'
]
TOKEN_MULTIPLICATIVE_ADVERBS = [
    r'semel',
    r'bis',
    r'ter',
    r'quater',
    r'quinquies',
    r'sexies',
    r'septies',
    r'octies',
    r'no[nv]ies',
    r'decies',
    r'un(de?)?cies',
    r'duo(de)?cies',
    r'terdecies',
    r'quaterdecies',
    r'quindecies',
    r'sex?decies',
    r'septdecies',
    r'octodecies',
    r'novodecies',
    r'vicies',
    r'un(de?)?v[ei]cies',
    r'duo(de)?v[ei]cies',
    r'terv[ei]cies',
    r'quaterv[ei]cies',
    r'quinv[ei]cies',
    r'sex?v[ei]cies',
    r'septv[ei]cies',
    r'octov[ei]cies',
    r'novov[ei]cies',
]

def tokenize(text):
    try:
        text = text.decode('utf-8')
    except:
        pass

    tokens = TOKEN_DELIMITERS.split(text)
    # remove empty strings
    tokens = [s for s in tokens if s != '']
    return tokens

def skip_tokens(tokens, i, f):
    while i < len(tokens) and f(tokens[i]):
        i += 1
    return i

def skip_spaces(tokens, i):
    return skip_tokens(tokens, i, lambda t: re.compile('\s+').match(t))

def skip_to_next_word(tokens, i):
    return skip_tokens(tokens, i, lambda t: not re.compile('[\wà]+', re.IGNORECASE | re.UNICODE).match(t))

def skip_to_token(tokens, i, token):
    return skip_tokens(tokens, i, lambda t: t != token)

def skip_to_end_of_line(tokens, i):
    if i > 0 and i < len(tokens) and tokens[i - 1] == TOKEN_NEW_LINE:
        return i

    return skip_to_token(tokens, i, TOKEN_NEW_LINE)

def skip_to_quote_start(tokens, i):
    return skip_to_token(tokens, i, TOKEN_DOUBLE_QUOTE_OPEN)

# vim: set ts=4 sw=4 sts=4 et:
