# -*- coding: utf-8 -*-

import re

TOKEN_DELIMITERS = re.compile(u'(\xa0|\s|\(|\)|\.|\!|\'|,|")')
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
    u'bis',
    u'ter',
    u'quater',
    u'quinquies',
    u'sexies',
    u'septies',
    u'octies',
    u'novies',
    u'decies',
    u'undecies',
    u'duodecies',
    u'terdecies',
    u'quaterdecies',
    u'quindecies',
    u'sexdecies',
    u'septdecies',
    u'octodecies',
    u'novodecies',
    u'vicies',
    u'unvicies',
    u'duovicies',
    u'tervicies',
    u'quatervicies',
    u'quinvicies',
    u'sexvicies',
    u'septvicies'
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
