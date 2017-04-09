# -*- coding: utf-8 -*-

import re
import sys

import alinea_lexer

def_types = [
    'header1',
    'header2',
    'header3',
    'alinea',
    'sentence'
]

def debug(node, tokens, i, msg):
    if '-v' in sys.argv:
        print('    ' * get_node_depth(node) + msg + ' ' + str(tokens[i:i+8]))

def is_number(token):
    return re.compile('\d+').match(token)

def is_space(token):
    return re.compile('^\s+$').match(token)

def parse_int(s):
    return int(re.search(r'\d+', s).group())

def parse_roman_number(n):
    romans_map = zip(
        (1000,  900, 500, 400 , 100,  90 , 50 ,  40 , 10 ,   9 ,  5 ,  4  ,  1),
        ( 'M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    )

    n = n.upper()
    i = res = 0
    for d, r in romans_map:
        while n[i:i + len(r)] == r:
            res += d
            i += len(r)
    return res

def is_roman_number(token):
    return re.compile(r"[IVXCLDM]+(er)?").match(token)

def is_number_word(word):
    return word_to_number(word) >= 0

def word_to_number(word):
    words = [
        [u'un', u'une', u'premier', u'première'],
        [u'deux', u'deuxième', u'second', u'seconde'],
        [u'trois', u'troisième'],
        [u'quatre', u'quatrième'],
        [u'cinq', u'cinquième'],
        [u'six', u'sixième'],
        [u'sept', u'septième'],
        [u'huit', u'huitième'],
        [u'neuf', u'neuvième']
    ]

    for i in range(0, len(words)):
        if word in words[i]:
            return i + 1

    return -1

def month_to_number(month):
    return alinea_lexer.TOKEN_MONTH_NAMES.index(month) + 1

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

    return node

def remove_node(parent, node):
    if node not in parent['children']:
        raise Exception('invalid parent')
    if 'parent' not in node or node['parent'] != parent:
        raise Exception('parent node does not match')

    parent['children'].remove(node)
    del node['parent']

def delete_parent(root):
    if 'parent' in root:
        del root['parent']
    if 'children' in root:
        for child in root['children']:
            delete_parent(child)
    return root

def copy_node(node, recursive=True):
    c = node.copy()
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

def parse_law_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    j = i

    node = create_node(parent, {
        'type': 'law-reference',
        'lawId': '',
        'children': [],
    })

    debug(parent, tokens, i, 'parse_law_reference')

    # de l'ordonnance
    # l'ordonnance
    if i + 4 < len(tokens) and (tokens[i + 2] == u'ordonnance' or tokens[i + 4] == u'ordonnance'):
        node['lawType'] = 'ordonnance'
        i = alinea_lexer.skip_to_token(tokens, i, u'ordonnance') + 2
    # de la loi
    # la loi
    elif i + 4 < len(tokens) and ((tokens[i] == u'la' and tokens[i + 2] == u'loi') or (tokens[i] == u'de' and tokens[i + 4] == u'loi')):
        i = alinea_lexer.skip_to_token(tokens, i, u'loi') + 2
    else:
        remove_node(parent, node)
        return i

    if tokens[i] == u'organique':
        node['lawType'] = 'organic'
        i += 2

    i = alinea_lexer.skip_to_token(tokens, i, u'n°') + 1
    # If we didn't find the "n°" token, the reference is incomplete and we forget about it.
    # FIXME: we might have to handle the "la même ordonnance" or "la même loi" incomplete reference cases.
    if i >= len(tokens):
        remove_node(parent, node)
        return j

    i = alinea_lexer.skip_spaces(tokens, i)
    node['lawId'] = tokens[i]
    # skip {lawId} and the following space
    i += 2

    if i < len(tokens) and tokens[i] == u'du':
        node['lawDate'] = tokens[i + 6] + u'-' + str(month_to_number(tokens[i + 4])) + u'-' + tokens[i + 2]
        # skip {lawDate} and the following space
        i += 7

    # i = alinea_lexer.skip_spaces(tokens, i)
    # if tokens[i] == u'relative':
    #     print('foo')

    debug(parent, tokens, i, 'parse_law_reference end')

    return i

def parse_multiplicative_adverb(tokens, i, node):
    if i >= len(tokens):
        return i

    adverbs = alinea_lexer.TOKEN_MULTIPLICATIVE_ADVERBS.sort(key = lambda s: -len(s))
    for adverb in alinea_lexer.TOKEN_MULTIPLICATIVE_ADVERBS:
        if tokens[i].endswith(adverb):
            node['is' + adverb.title()] = True;
            # skip {multiplicativeAdverb} and the following space
            i += 1
            i = alinea_lexer.skip_spaces(tokens, i)
            return i
    return i

def parse_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    debug(parent, tokens, i, 'parse_definition')

    j = parse_article_definition(tokens, i, parent)
    if j != i:
        return j
    i = j

    j = parse_alinea_definition(tokens, i, parent)
    if j != i:
        return j
    i = j

    j = parse_mention_definition(tokens, i, parent)
    if j != i:
        return j
    i = j

    j = parse_header1_definition(tokens, i, parent)
    if j != i:
        return j
    i = j

    j = parse_header2_definition(tokens, i, parent)
    if j != i:
        return j
    i = j

    j = parse_sentence_definition(tokens, i, parent)
    if j != i:
        return j
    i = j

    j = parse_words_definition(tokens, i, parent)
    if j != i:
        return j
    i = j

    j = parse_title_definition(tokens, i, parent)
    if j != i:
        return j
    i = j

    return i

def parse_sentence_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    debug(parent, tokens, i, 'parse_sentence_definition')
    j = i

    # {count} phrases
    if is_number_word(tokens[i]) and tokens[i + 2].startswith(u'phrase'):
        count = word_to_number(tokens[i])
        i += 4
        # ainsi rédigé
        # est rédigé
        # est ainsi rédigé
        if (i + 2 < len(tokens) and tokens[i + 2].startswith(u'rédigé')
            or (i + 4 < len(tokens) and tokens[i + 4].startswith(u'rédigé'))):
            # we expect {count} definitions => {count} quotes
            # but they don't always match, so for now we parse all of the available contents
            # FIXME: issue a warning because the expected count doesn't match?
            i = alinea_lexer.skip_spaces(tokens, i)
            i = alinea_lexer.skip_to_quote_start(tokens, i)
            i = parse_for_each(
                parse_quote,
                tokens,
                i,
                lambda : create_node(parent, {'type': 'sentence', 'children': []})
            )
        else:
            create_node(parent, {'type': 'sentence', 'count': count})
    else:
        debug(parent, tokens, i, 'parse_sentence_definition none')
        return j

    debug(parent, tokens, i, 'parse_sentence_definition end')

    return i

def parse_words_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'words',
        'children': []
    })
    debug(parent, tokens, i, 'parse_words_definition')

    j = i
    i = parse_position(tokens, i, node)
    # le mot
    # les mots
    # des mots
    if tokens[i].lower() in [u'le', u'les', u'des'] and tokens[i + 2].startswith(u'mot'):
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_for_each(parse_quote, tokens, i, node)
        # i = alinea_lexer.skip_spaces(tokens, i)
    # le nombre
    # le chiffre
    elif tokens[i].lower() in [u'le'] and tokens[i + 2] in [u'nombre', u'chiffre']:
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_quote(tokens, i, node)
    # "
    elif tokens[i] == alinea_lexer.TOKEN_DOUBLE_QUOTE_OPEN:
        i = parse_for_each(parse_quote, tokens, i, node)
        i = alinea_lexer.skip_spaces(tokens, i)
    # la référence
    elif tokens[i] == u'la' and tokens[i + 2] == u'référence':
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_quote(tokens, i, node)
    else:
        debug(parent, tokens, i, 'parse_words_definition none')
        remove_node(parent, node)
        return j
    debug(parent, tokens, i, 'parse_words_definition end')
    return i

def parse_article_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'article',
        'children': [],
    })
    debug(parent, tokens, i, 'parse_article_definition')

    # un article
    if tokens[i] == u'un' and tokens[i + 2] == u'article':
        i += 4
    # l'article
    elif tokens[i] == u'l' and tokens[i + 2] == u'article':
        i += 4
    else:
        debug(parent, tokens, i, 'parse_article_definition none')
        remove_node(parent, node)
        return i

    i = parse_article_id(tokens, i, node)

    i = alinea_lexer.skip_spaces(tokens, i)
    if i < len(tokens) and tokens[i] == u'ainsi' and tokens[i + 2] == u'rédigé':
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_for_each(parse_quote, tokens, i, node)

    debug(parent, tokens, i, 'parse_article_definition end')

    return i

def parse_alinea_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    debug(parent, tokens, i, 'parse_alinea_definition')

    # {count} alinéa(s)
    if is_number_word(tokens[i]) and tokens[i + 2].startswith(u'alinéa'):
        count = word_to_number(tokens[i])
        i += 4
        # ainsi rédigé
        # est rédigé
        # est ainsi rédigé
        if (i + 2 < len(tokens) and tokens[i + 2].startswith(u'rédigé')
            or (i + 4 < len(tokens) and tokens[i + 4].startswith(u'rédigé'))):
            # we expect {count} definitions => {count} quotes
            # but they don't always match, so for now we parse all of the available contents
            # FIXME: issue a warning because the expected count doesn't match?
            i = alinea_lexer.skip_spaces(tokens, i)
            i = alinea_lexer.skip_to_quote_start(tokens, i)
            i = parse_for_each(
                parse_quote,
                tokens,
                i,
                lambda: create_node(parent, {'type': 'alinea', 'children': []})
            )
        else:
            node = create_node(parent, {'type': 'alinea', 'count': count})
    else:
        debug(parent, tokens, i, 'parse_alinea_definition none')
        return i

    debug(parent, tokens, i, 'parse_alinea_definition end')

    return i

def parse_mention_definition(tokens, i, parent):
    if i >= len(tokens):
        return i
    node = create_node(parent, {
        'type': 'mention',
        'children': []
    })
    debug(parent, tokens, i, 'parse_mention_definition')
    # la mention
    if tokens[i].lower() == u'la' and tokens[i + 2] == u'mention':
        i += 4
    else:
        debug(parent, tokens, i, 'parse_mention_definition none')
        remove_node(parent, node)
        return i
    # :
    if tokens[i] == ':':
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_for_each(parse_quote, tokens, i, node)

    debug(parent, tokens, i, 'parse_mention_definition end')

    return i

def parse_header1_definition(tokens, i, parent):
    if i >= len(tokens):
        return i
    node = create_node(parent, {
        'type': 'header1',
        'children': []
    })
    debug(parent, tokens, i, 'parse_header1_definition')
    # un {romanPartNumber}
    if tokens[i].lower() == u'un' and is_roman_number(tokens[i + 2]):
        node['order'] = parse_roman_number(tokens[i + 2])
        i += 4
        i = alinea_lexer.skip_spaces(tokens, i)
        if i + 2 < len(tokens) and tokens[i] == u'ainsi' and tokens[i + 2] == u'rédigé':
            i = alinea_lexer.skip_to_quote_start(tokens, i)
            i = parse_quote(tokens, i, node)
    else:
        debug(parent, tokens, i, 'parse_header1_definition end')
        remove_node(parent, node)
        return i

    return i

def parse_header2_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    debug(parent, tokens, i, 'parse_header2_definition')

    # un ... ° ({articlePartRef})
    if tokens[i].lower() == u'un' and ''.join(tokens[i + 2:i + 5]) == u'...' and tokens[i + 6] == u'°':
        node = create_node(parent, {
            'type': 'header2',
            'children': []
        })
        # FIXME: should we simply ignore the 'order' field all together?
        node['order'] = '...'
        i += 8
        i = alinea_lexer.skip_spaces(tokens, i)
        if tokens[i] == u'ainsi' and tokens[i + 2] == u'rédigé':
            i = alinea_lexer.skip_to_quote_start(tokens, i + 4)
            i = parse_quote(tokens, i, node)
    # un {order}° ({orderLetter}) ({multiplicativeAdverb}) ({articlePartRef})
    elif tokens[i].lower() == u'un' and re.compile(u'\d+°').match(tokens[i + 2]):
        node = create_node(parent, {
            'type': 'header2',
            'children': []
        })
        node['order'] = parse_int(tokens[i + 2])
        i += 4
        if re.compile(u'[A-Z]').match(tokens[i]):
            node['subOrder'] = tokens[i]
            i += 2
        i = parse_multiplicative_adverb(tokens, i, node)
        i = parse_article_part_reference(tokens, i, node)
        i = alinea_lexer.skip_spaces(tokens, i)
        if i < len(tokens) and tokens[i] == u'ainsi' and tokens[i + 2] == u'rédigé':
            i = alinea_lexer.skip_to_quote_start(tokens, i + 4)
            i = parse_quote(tokens, i, node)
    # des {start}° à {end}°
    elif (tokens[i].lower() == u'des' and re.compile(u'\d+°').match(tokens[i + 2])
        and tokens[i + 4] == u'à' and re.compile(u'\d+°').match(tokens[i + 6])):
        start = parse_int(tokens[i + 2])
        end = parse_int(tokens[i + 6])
        i += 8
        # ainsi rédigés
        if (i + 2 < len(tokens) and tokens[i + 2].startswith(u'rédigé')
            or (i + 4 < len(tokens) and tokens[i + 4].startswith(u'rédigé'))):
            i = alinea_lexer.skip_to_quote_start(tokens, i + 4)
            i = parse_for_each(
                parse_quote,
                tokens,
                i,
                lambda : create_node(parent, {'type': 'header2', 'children': []})
            )
    else:
        debug(parent, tokens, i, 'parse_header2_definition end')
        return i

    return i

def parse_article_id(tokens, i, node):
    node['id'] = ''

    # article {articleId} de {lawReference}
    if i < len(tokens) and tokens[i] == 'L' and tokens[i + 1] == '.':
        while not re.compile('\d+(-\d+)?').match(tokens[i]):
            node['id'] += tokens[i]
            i += 1

    if i < len(tokens) and re.compile('\d+(-\d+)?').match(tokens[i]):
        node['id'] += tokens[i]
        # skip {articleId} and the following space
        i += 1
        i = alinea_lexer.skip_spaces(tokens, i)

    # {articleId} {articleLetter}
    # FIXME: handle the {articleLetter}{multiplicativeAdverb} case?
    if i < len(tokens) and re.compile('^[A-Z]$').match(tokens[i]):
        node['id'] += ' ' + tokens[i]
        # skip {articleLetter} and the following space
        i += 1
        i = alinea_lexer.skip_spaces(tokens, i)

    i = parse_multiplicative_adverb(tokens, i, node)

    if not node['id'] or is_space(node['id']):
        del node['id']

    return i

def parse_title_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'title-reference',
        'children': [],
    })

    debug(parent, tokens, i, 'parse_title_reference')

    j = i
    i = parse_position(tokens, i, node)

    # le titre {order}
    if tokens[i].lower() == u'le' and tokens[i + 2] == u'titre' and is_roman_number(tokens[i + 4]):
        node['order'] = parse_roman_number(tokens[i + 4])
        i += 6
        i = parse_multiplicative_adverb(tokens, i, node)
    else:
        debug(parent, tokens, i, 'parse_title_reference none')
        remove_node(parent, node)
        return j

    i = parse_reference(tokens, i, node)

    debug(parent, tokens, i, 'parse_title_reference end')

    return i

def parse_title_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'title',
        'children': [],
    })

    debug(parent, tokens, i, 'parse_title_definition')

    # un titre {order}
    if tokens[i].lower() == u'un' and tokens[i + 2] == u'titre' and is_roman_number(tokens[i + 4]):
        node['order'] = parse_roman_number(tokens[i + 4])
        i += 6
        i = parse_multiplicative_adverb(tokens, i, node)
    else:
        debug(parent, tokens, i, 'parse_title_definition none')
        remove_node(parent, node)
        return i

    i = alinea_lexer.skip_spaces(tokens, i)
    if tokens[i] == u'ainsi' and tokens[i + 2] == u'rédigé':
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_for_each(parse_quote, tokens, i, node)

    debug(parent, tokens, i, 'parse_title_definition end')

    return i

def parse_book_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'book-reference',
        'children': [],
    })

    debug(parent, tokens, i, 'parse_book_reference')

    j = i
    i = parse_position(tokens, i, node)

    # le titre {order}
    if tokens[i].lower() == u'du' and tokens[i + 2] == u'livre' and is_roman_number(tokens[i + 4]):
        node['order'] = parse_roman_number(tokens[i + 4])
        i += 6
    else:
        debug(parent, tokens, i, 'parse_book_reference none')
        remove_node(parent, node)
        return j

    i = parse_reference(tokens, i, node)

    debug(parent, tokens, i, 'parse_book_reference end')

    return i

def parse_article_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'article-reference',
        'id': ''
    })

    debug(parent, tokens, i, 'parse_article_reference')

    j = i
    i = parse_position(tokens, i, node)
    # de l'article
    # à l'article
    if tokens[i].lower() in [u'de', u'à'] and tokens[i + 2] == u'l' and tokens[i + 4] == u'article':
        i += 5
        i = alinea_lexer.skip_spaces(tokens, i)
    # l'article
    elif tokens[i].lower() == u'l' and tokens[i + 1] == alinea_lexer.TOKEN_SINGLE_QUOTE and tokens[i + 2] == u'article':
        i += 3
        i = alinea_lexer.skip_spaces(tokens, i)
    # elif tokens[i] == u'un' and tokens[i + 2] == u'article':
    #     i += 4
    # Article {articleNumber}
    elif tokens[i].lower().startswith(u'article'):
        i += 1
        i = alinea_lexer.skip_spaces(tokens, i)
    # le même article
    elif tokens[i].lower() == u'le' and tokens[i + 2] == u'même' and tokens[i + 4] == u'article':
        i += 6
        article_refs = filter_nodes(
            get_root(parent),
            lambda n: 'type' in n and n['type'] == 'article-reference'
        )
        # the last one in order of traversal is the previous one in order of syntax
        # don't forget the current node is in the list too => -2 instead of -1
        article_ref = copy_node(article_refs[-2])
        push_node(parent, article_ref)
        remove_node(parent, node)
    else:
        remove_node(parent, node)
        return j

    i = parse_article_id(tokens, i, node)

    # i = parse_article_part_reference(tokens, i, node)
    # de la loi
    # de l'ordonnance
    # du code
    # les mots
    # l'alinéa
    i = parse_one_of(
        [
            parse_law_reference,
            parse_code_reference,
            parse_words_reference,
            parse_alinea_reference
        ],
        tokens,
        i,
        node
    )

    # i = parse_quote(tokens, i, node)

    debug(parent, tokens, i, 'parse_article_reference end')

    return i

def parse_position(tokens, i, node):
    if i >= len(tokens):
        return i

    j = i
    # i = alinea_lexer.skip_to_next_word(tokens, i)

    # après
    if tokens[i].lower() == u'après':
        node['position'] = 'after'
        i += 2
    # avant
    elif tokens[i].lower() == u'avant':
        node['position'] = 'before'
        i += 2
    # au début
    elif tokens[i].lower() == u'au' and tokens[i + 2] == u'début':
        node['position'] = 'beginning'
        i += 4
    # la fin du {article}
    elif tokens[i] == u'la' and tokens[i + 2] == u'fin':
        node['position'] = 'end'
        i += 4
    # à la fin du {article}
    elif tokens[i].lower() == u'à' and tokens[i + 2] == u'la' and tokens[i + 4] == u'fin':
        node['position'] = 'end'
        i += 6
    else:
        return j

    return i

def parse_alinea_reference(tokens, i, parent):
    if i >= len(tokens):
        return i
    node = create_node(parent, {
        'type': 'alinea-reference',
        'children': []
    })
    debug(parent, tokens, i, 'parse_alinea_reference')

    j = i
    i = parse_position(tokens, i, node)
    # le {order} alinéa
    # du {order} alinéa
    # au {order} alinéa
    if tokens[i].lower() in [u'du', u'le', u'au'] and is_number_word(tokens[i + 2]) and tokens[i + 4].startswith(u'alinéa'):
        node['order'] = word_to_number(tokens[i + 2])
        i += 6
    # l'alinéa
    elif tokens[i].lower() == u'l' and tokens[i + 2].startswith(u'alinéa'):
        i += 4
    # de l'alinéa
    elif tokens[i] == 'de' and tokens[i + 2].lower() == [u'l'] and tokens[i + 4].startswith(u'alinéa'):
        i += 6
    # {order} {partType}
    elif is_number_word(tokens[i].lower()) and tokens[i + 2].startswith(u'alinéa'):
        node['order'] = word_to_number(tokens[i])
        i += 4
    # aux {count} {position} alinéas
    # elif tokens[i].lowers() == u'aux' and is_number_word(tokens[i + 2]) and tokens[i + 6] == u'alinéas':
    # le même alinéa
    elif tokens[i].lower() in [u'le'] and tokens[i + 2] == u'même' and tokens[i + 4] == u'alinéa':
        i += 6
        alinea_refs = filter_nodes(
            get_root(parent),
            lambda n: 'type' in n and n['type'] == 'alinea-reference'
        )
        # the last one in order of traversal is the previous one in order of syntax
        # don't forget the current node is in the list too => -2 instead of -1
        alinea_ref = copy_node(alinea_refs[-2])
        push_node(parent, alinea_ref)
        remove_node(parent, node)
    # du dernier alinéa
    # au dernier alinéa
    # le dernier alinéa
    elif tokens[i].lower() in [u'du', u'au', u'le'] and tokens[i + 2] == u'dernier' and tokens[i + 4] == u'alinéa':
        node['order'] = -1
        i += 6
    # à l'avant dernier alinéa
    elif tokens[i].lower() == u'à' and tokens[i + 4] == u'avant' and tokens[i + 6] == u'dernier' and tokens[i + 8] == u'alinéa':
        node['order'] = -2
        i += 10
    # l'avant-dernier alinéa
    elif tokens[i].lower() == u'l' and tokens[i + 2] == u'avant-dernier' and tokens[i + 4] == u'alinéa':
        node['order'] = -2
        i += 6
    # à l'avant-dernier alinéa
    elif tokens[i].lower() == u'à' and tokens[i + 2] == u'l' and tokens[i + 4] == u'avant-dernier' and tokens[i + 6] == u'alinéa':
        node['order'] = -2
        i += 10
    # alinéa {order}
    elif tokens[i].lower() == u'alinéa' and is_number(tokens[i + 2]):
        node['order'] = parse_int(tokens[i + 2])
        i += 4
    else:
        debug(parent, tokens, i, 'parse_alinea_reference none')
        remove_node(parent, node)
        return j

    i = parse_article_part_reference(tokens, i, node)
    # i = parse_quote(tokens, i, node)

    debug(parent, tokens, i, 'parse_alinea_reference end')

    return i

def parse_sentence_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'sentence-reference',
        'children': []
    })
    debug(parent, tokens, i, 'parse_sentence_reference')

    j = i
    i = parse_position(tokens, i, node)
    # une phrase
    # la phrase
    if tokens[i].lower() in [u'la', u'une'] and tokens[i + 2] == 'phrase':
        i += 4
    # de la {partNumber} phrase
    elif tokens[i].lower() == u'de' and tokens[i + 2] == u'la' and is_number_word(tokens[i + 4]) and tokens[i + 6] == u'phrase':
        node['order'] = word_to_number(tokens[i + 4])
        i += 8
    # la {partNumber} phrase
    elif tokens[i].lower() == u'la' and is_number_word(tokens[i + 2]) and tokens[i + 4] == u'phrase':
        node['order'] = word_to_number(tokens[i + 2])
        i += 6
    # à la {partNumber} phrase
    # À la {partNumber} phrase
    elif (tokens[i] == u'à' or tokens[i] == u'À') and tokens[i + 2].lower() == u'la' and is_number_word(tokens[i + 4]) and tokens[i + 6] == u'phrase':
        node['order'] = word_to_number(tokens[i + 4])
        i += 8
    # la dernière phrase
    elif tokens[i].lower() == u'la' and tokens[i + 2] == u'dernière' and tokens[i + 4] == u'phrase':
        node['order'] = -1
        i += 6
    else:
        debug(parent, tokens, i, 'parse_sentence_reference none')
        remove_node(parent, node)
        return j

    i = parse_article_part_reference(tokens, i, node)

    debug(parent, tokens, i, 'parse_sentence_reference end')

    fix_incomplete_references(parent, node)

    return i

def fix_incomplete_references(parent, node):
    if len(parent['children']) >= 2:
        for child in parent['children']:
            if child['type'] == 'incomplete-reference':
                # set the actual reference type
                child['type'] = node['type']
                # copy all the child of the fully qualified reference node
                for c in node['children']:
                    push_node(child, copy_node(c))

def parse_back_reference(tokens, i, parent):
    if i >= len(tokens):
        return i
    if tokens[i] == u'Il':
        refs = filter_nodes(
            get_root(parent),
            lambda n: 'type' in n and n['type'].endswith('-reference')
        )
        for j in reversed(range(0, len(refs))):
            if get_node_depth(refs[j]) <= get_node_depth(parent):
                push_node(parent, copy_node(refs[j]))
                break
        i += 2
    return i

def parse_incomplete_reference(tokens, i, parent):
    if i >= len(tokens):
        return i
    node = create_node(parent, {
        'type': 'incomplete-reference',
        'children': []
    })
    j = i
    i = parse_position(tokens, i, node)
    if tokens[i].lower() == u'à' and tokens[i + 2] in [u'le', u'la'] and is_number_word(tokens[i + 4]):
        node['order'] = word_to_number(tokens[i + 4])
        i += 6
    elif tokens[i].lower() in [u'le', u'la'] and is_number_word(tokens[i + 2]):
        node['order'] = word_to_number(tokens[i + 2])
        i += 4
    elif j == i:
        remove_node(parent, node)
        return j

    return i

def parse_words_reference(tokens, i, parent):
    if i >= len(tokens):
        return i
    node = create_node(parent, {
        'type': 'words-reference'
    })
    debug(parent, tokens, i, 'parse_words_reference')
    j = i
    i = alinea_lexer.skip_to_next_word(tokens, i)
    i = parse_position(tokens, i, node)
    # le mot
    # les mots
    # des mots
    if tokens[i].lower() in [u'le', u'les', u'des'] and tokens[i + 2].startswith(u'mot'):
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_for_each(parse_quote, tokens, i, node)
    # le nombre
    # le chiffre
    elif tokens[i].lower() in [u'le'] and tokens[i + 2] in [u'nombre', u'chiffre']:
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_quote(tokens, i, node)
    # la référence
    elif tokens[i].lower() in [u'la'] and tokens[i + 2] == u'référence':
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_quote(tokens, i, node)
    else:
        debug(parent, tokens, i, 'parse_words_reference none')
        remove_node(parent, node)
        return j
    debug(parent, tokens, i, 'parse_words_reference end')
    return i

def parse_header2_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'header2-reference'
    })
    debug(parent, tokens, i, 'parse_header2_reference')
    j = i
    i = parse_position(tokens, i, node)

    # le {order}° ({multiplicativeAdverb}) ({articlePartRef})
    # du {order}° ({multiplicativeAdverb}) ({articlePartRef})
    # au {order}° ({multiplicativeAdverb}) ({articlePartRef})
    if tokens[i].lower() in [u'le', u'du', u'au'] and re.compile(u'\d+°').match(tokens[i + 2]):
        node['order'] = parse_int(tokens[i + 2])
        i += 4
        i = parse_multiplicative_adverb(tokens, i, node)
        i = parse_article_part_reference(tokens, i, node)
    # le même {order}° ({multiplicativeAdverb}) ({articlePartRef})
    # du même {order}° ({multiplicativeAdverb}) ({articlePartRef})
    # au même {order}° ({multiplicativeAdverb}) ({articlePartRef})
    elif tokens[i].lower() in [u'le', u'du', u'au'] and tokens[i + 2] == u'même' and re.compile(u'\d+°').match(tokens[i + 4]):
        node['order'] = parse_int(tokens[i + 4])
        i += 6
        i = parse_multiplicative_adverb(tokens, i, node)
        i = parse_article_part_reference(tokens, i, node)
    else:
        debug(parent, tokens, i, 'parse_header2_reference none')
        remove_node(parent, node)
        return j
    # i = parse_quote(tokens, i, node)
    debug(parent, tokens, i, 'parse_header2_reference end')
    return i

def parse_header1_reference(tokens, i, parent):
    if i >= len(tokens):
        return i
    node = create_node(parent, {
        'type': 'header1-reference',
        'children': []
    })
    debug(parent, tokens, i, 'parse_header1_reference')
    j = i
    i = parse_position(tokens, i, node)
    # le {romanPartNumber}
    # du {romanPartNumber}
    # un {romanPartNumber}
    if tokens[i].lower() in [u'le', u'du', u'un'] and is_roman_number(tokens[i + 2]):
        node['order'] = parse_roman_number(tokens[i + 2])
        i += 4
    else:
        debug(parent, tokens, i, 'parse_header1_reference end')
        remove_node(parent, node)
        return j

    i = parse_article_part_reference(tokens, i, node)
    # i = parse_quote(tokens, i, node)

    debug(parent, tokens, i, 'parse_header1_reference end')

    return i

def parse_article_part_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    # i = alinea_lexer.skip_to_next_word(tokens, i)

    j = parse_alinea_reference(tokens, i, parent)
    if j != i:
        return j
    i = j

    j = parse_sentence_reference(tokens, i, parent)
    if j != i:
        return j
    i = j

    j = parse_words_reference(tokens, i, parent)
    if j != i:
        return j
    i = j

    j = parse_article_reference(tokens, i, parent)
    if j != i:
        return j
    i = j

    j = parse_header1_reference(tokens, i, parent)
    if j != i:
        return j
    i = j

    j = parse_header2_reference(tokens, i, parent)
    if j != i:
        return j
    i = j

    return i

def parse_quote(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'quote',
        'words': ''
    })

    debug(parent, tokens, i, 'parse_quote')

    i = alinea_lexer.skip_spaces(tokens, i)

    # "
    if tokens[i] == alinea_lexer.TOKEN_DOUBLE_QUOTE_OPEN:
        i += 1
    # # est rédigé(es)
    # # ainsi rédigé(es)
    # # est ainsi rédigé(es)
    # elif (i + 2 < len(tokens) and tokens[i + 2].startswith(u'rédigé')
    #     or (i + 4 < len(tokens) and tokens[i + 4].startswith(u'rédigé'))):
    #     i = alinea_lexer.skip_to_quote_start(tokens, i + 2) + 1
    else:
        remove_node(parent, node)
        return i

    while i < len(tokens) and tokens[i] != alinea_lexer.TOKEN_DOUBLE_QUOTE_CLOSE and tokens[i] != alinea_lexer.TOKEN_NEW_LINE:
        node['words'] += tokens[i]
        i += 1

    # skipalinea_lexer.TOKEN_DOUBLE_QUOTE_CLOSE
    i += 1
    i = alinea_lexer.skip_spaces(tokens, i)

    debug(parent, tokens, i, 'parse_quote end')

    return i

# Parse the verb to determine the corresponding action (one of 'add', 'delete', 'edit' or 'replace').
def parse_edit(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'edit'
    })

    debug(parent, tokens, i, 'parse_edit')

    r = i
    # i = parse_for_each(parse_reference, tokens, i, node)
    i = parse_reference_list(tokens, i, node)
    # if we did not parse a reference

    i = alinea_lexer.skip_spaces(tokens, i)

    # if we didn't find any reference as a subject and the subject/verb are not reversed
    if len(node['children']) == 0 and tokens[i] != 'Est' and tokens[i] != 'Sont':
        remove_node(parent, node)
        debug(parent, tokens, i, 'parse_edit none')
        return i
    # i = r

    i = alinea_lexer.skip_tokens(tokens, i, lambda t: t.lower() not in [u'est', u'sont', u'devient'] and not t == u'.')
    if i + 2 >= len(tokens):
        remove_node(parent, node)
        debug(parent, tokens, i, 'parse_edit eof')
        return r

    # sont supprimés
    # sont supprimées
    # est supprimé
    # est supprimée
    # est abrogé
    # est abrogée
    # sont abrogés
    # sont abrogées
    if tokens[i + 2].startswith(u'supprimé') or tokens[i + 2].startswith(u'abrogé'):
        node['editType'] = 'delete'
        i = alinea_lexer.skip_to_end_of_line(tokens, i)
    # est ainsi rédigé
    # est ainsi rédigée
    # est ainsi modifié
    # est ainsi modifiée
    elif tokens[i + 4].startswith(u'rédigé') or tokens[i + 4].startswith(u'modifié'):
        node['editType'] = 'edit'
        i = alinea_lexer.skip_to_end_of_line(tokens, i)
        i = alinea_lexer.skip_spaces(tokens, i)
        i = parse_definition(tokens, i, node)
    # est remplacé par
    # est remplacée par
    # sont remplacés par
    # sont remplacées par
    elif tokens[i + 2].startswith(u'remplacé'):
        node['editType'] = 'replace'
        i += 6
        i = parse_definition(tokens, i, node)
        i = alinea_lexer.skip_to_end_of_line(tokens, i)
    # remplacer
    elif tokens[i].lower() == u'remplacer':
        node['editType'] = 'replace'
        i += 2
        # i = parse_definition(tokens, i, node)
        i = parse_reference(tokens, i, node)
        i = alinea_lexer.skip_to_end_of_line(tokens, i)
        if tokens[i].lower() == 'par':
            i += 2
            i = parse_definition(tokens, i, node)
            i = alinea_lexer.skip_to_end_of_line(tokens, i)
    # est inséré
    # est insérée
    # sont insérés
    # sont insérées
    # est ajouté
    # est ajoutée
    # sont ajoutés
    # sont ajoutées
    elif tokens[i + 2].startswith(u'inséré') or tokens[i + 2].startswith(u'ajouté'):
        node['editType'] = 'add'
        i += 4
        i = parse_definition(tokens, i, node)
        i = alinea_lexer.skip_to_end_of_line(tokens, i)
    # est ainsi rétabli
    elif tokens[i + 4].startswith(u'rétabli'):
        node['editType'] = 'add'
        i = alinea_lexer.skip_to_end_of_line(tokens, i)
        i = alinea_lexer.skip_spaces(tokens, i)
        i = parse_definition(tokens, i, node)
    # est complété par
    elif tokens[i + 2] == u'complété':
        node['editType'] = 'add'
        i += 6
        # i = parse_definition(tokens, i, node)
        i = parse_definition_list(tokens, i, node)
        # i = alinea_lexer.skip_to_end_of_line(tokens, i)
    # devient
    elif tokens[i] == u'devient':
        node['editType'] = 'rename'
        i += 2
        i = parse_definition(tokens, i, node)
    else:
        i = r
        debug(parent, tokens, i, 'parse_edit remove')
        remove_node(parent, node)
        i = parse_raw_article_content(tokens, i, parent)
        i = alinea_lexer.skip_to_end_of_line(tokens, i)
        return i

    # We've parsed pretty much everything we could handle. At this point,
    # there should be no meaningful content. But their might be trailing
    # spaces or ponctuation (ofent "." or ";"), so we alinea_lexer.skip_ to the end of
    # the line.
    i = alinea_lexer.skip_to_end_of_line(tokens, i)

    debug(parent, tokens, i, 'parse_edit end')

    return i

def parse_raw_article_content(tokens, i, parent):
    node = create_node(parent, {
        'type': 'article-content',
        'content': ''
    })

    debug(parent, tokens, i, 'parse_raw_article_content')

    while i < len(tokens) and tokens[i] != alinea_lexer.TOKEN_NEW_LINE:
        node['content'] += tokens[i]
        i += 1

    if node['content'] == '' or is_space(node['content']):
        remove_node(parent, node)

    debug(parent, tokens, i, 'parse_raw_article_content end')

    return i


def parse_code_name(tokens, i, node):
    while i < len(tokens) and tokens[i] != u',' and tokens[i] != u'est':
        node['codeName'] += tokens[i]
        i += 1
    node['codeName'] = node['codeName'].strip()
    return i

# Parse a reference to a specific or aforementioned code.
# References to a specific code are specified by using the exact name of that code (cf parse_code_name).
# References to an aforementioned code will be in the form of "le même code".
def parse_code_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'code-reference',
        'codeName': '',
        'children': []
    })

    debug(parent, tokens, i, 'parse_code_reference')

    # code
    if tokens[i] == u'code':
        i = parse_code_name(tokens, i, node)
    # le code
    # du code
    elif tokens[i].lower() in [u'le', u'du'] and tokens[i + 2] == 'code':
        i = parse_code_name(tokens, i + 2, node)
    # le même code
    # du même code
    elif tokens[i].lower() in [u'le', u'du'] and tokens[i + 2] == u'même' and tokens[i + 4] == 'code':
        remove_node(parent, node)
        codeRefs = filter_nodes(
            get_root(parent),
            lambda n: 'type' in n and n['type'] == 'code-reference'
        )
        # the last one in order of traversal is the previous one in order of syntax
        node = copy_node(codeRefs[-1])
        node['children'] = []
        push_node(parent, node)
        # skip "le même code "
        i += 6

    if node['codeName'] == '' or is_space(node['codeName']):
        remove_node(parent, node)
    else:
        i = parse_reference(tokens, i, node)

    debug(parent, tokens, i, 'parse_code_reference end')

    return i

def parse_definition_list(tokens, i, parent):
    if i >= len(tokens):
        return i

    i = parse_definition(tokens, i, parent)
    i = alinea_lexer.skip_spaces(tokens, i)
    if ((i + 2 < len(tokens) and tokens[i] == u',' and tokens[i + 2] in [u'à', u'au'])
        or (i + 2 < len(tokens) and tokens[i] == u'et')):
        i = parse_definition_list(tokens, i + 2, parent)
    i = alinea_lexer.skip_spaces(tokens, i)

    # est rédigé(es)
    # ainsi rédigé(es)
    # est ainsi rédigé(es)
    if (i + 2 < len(tokens) and tokens[i + 2].startswith(u'rédigé')
        or (i + 4 < len(tokens) and tokens[i + 4].startswith(u'rédigé'))):
        i += 6
        def_nodes = filter_nodes(parent, lambda x: 'type' in x and x['type'] in def_types)
        for def_node in def_nodes:
            i = alinea_lexer.skip_to_quote_start(tokens, i)
            i = parse_quote(tokens, i, def_node)

    return i

# Parse multiple references separated by comas or the "et" word.
# All the parsed references will be siblings in parent['children'] and reso lve_fully_qualified_references + sort_references
# will take care of reworking the tree to make sure each reference in the list is complete and consistent.
def parse_reference_list(tokens, i, parent):
    if i >= len(tokens):
        return i

    i = parse_reference(tokens, i, parent)
    i = alinea_lexer.skip_spaces(tokens, i)
    if ((i + 2 < len(tokens) and tokens[i] == u',' and tokens[i + 2] in [u'à', u'au'])
        or (i + 2 < len(tokens) and tokens[i] == u'et')):
        i = parse_reference_list(tokens, i + 2, parent)
    i = alinea_lexer.skip_spaces(tokens, i)

    return i

def parse_one_of(fns, tokens, i, parent):
    # i = alinea_lexer.skip_to_next_word(tokens, i)

    if i >= len(tokens):
        return i

    for fn in fns:
        j = fn(tokens, i, parent)
        if j != i:
            return j
        i = j

    return i

def parse_reference(tokens, i, parent):
    i = parse_one_of(
        [
            parse_law_reference,
            parse_code_reference,
            parse_title_reference,
            parse_book_reference,
            parse_article_reference,
            parse_article_part_reference,
            parse_back_reference,
            parse_incomplete_reference,
            parse_alinea_reference
        ],
        tokens,
        i,
        parent
    )

    if i >= len(tokens):
        return i

    # if tokens[i] == u'et':
    #     i += 2

    return i

# {romanNumber}.
# u'ex': I., II.
def parse_article_header1(tokens, i, parent):
    if i >= len(tokens):
        return i

    i = alinea_lexer.skip_spaces(tokens, i)

    node = create_node(parent, {
        'type': 'header1',
        'order': 0,
        'children': [],
    })

    debug(parent, tokens, i, 'parse_article_header1')

    # skip'{romanNumber}.'
    if is_roman_number(tokens[i]) and tokens[i + 1] == u'.':
        debug(parent, tokens, i, 'parse_article_header1 found article header-1')
        node['order'] = parse_roman_number(tokens[i])
        i = alinea_lexer.skip_to_next_word(tokens, i + 2)
    else:
        j = i
        i = parse_edit(tokens, i, node)
        i = parse_for_each(parse_article_header2, tokens, i, node)
        if i == j:
            i = parse_raw_article_content(tokens, i, node)
        if len(node['children']) == 0:
            remove_node(parent, node)
        else:
            node['order'] = len(filter(lambda x: x['type'] == 'header1', parent['children']))

    debug(parent, tokens, i, 'parse_article_header1 end')

    return i

# {number}°
# u'ex': 1°, 2°
def parse_article_header2(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'header2',
        'order': 0,
        'children': [],
    })

    debug(parent, tokens, i, 'parse_article_header2')

    i = alinea_lexer.skip_spaces(tokens, i)
    if re.compile(u'\d+°').match(tokens[i]):
        debug(parent, tokens, i, 'parse_article_header2 found article header-2')

        node['order'] = parse_int(tokens[i])
        # skip {number}°
        i = alinea_lexer.skip_to_next_word(tokens, i + 2)
    else:
        remove_node(parent, node)
        node = parent

    i = parse_edit(tokens, i, node)
    i = parse_for_each(parse_article_header3, tokens, i, node)

    if node != parent and len(node['children']) == 0:
        remove_node(parent, node)

    debug(parent, tokens, i, 'parse_article_header2 end')

    return i

# {number})
# u'ex': a), b), a (nouveau))
def parse_article_header3(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': 'header3',
        'children': [],
    })

    debug(parent, tokens, i, 'parse_article_header3')

    i = alinea_lexer.skip_spaces(tokens, i)
    match = re.compile('([a-z]+)').match(tokens[i])
    if match and (tokens[i + 1] == u')' or (tokens[i + 2] == u'(' and tokens[i + 5] == u')')):
        node['order'] = ord(match.group()[0].encode('utf-8')) - ord('a') + 1
        # skip'{number}) ' or '{number} (nouveau))'
        if tokens[i + 1] == u')':
            i += 3
        else:
            i += 7
        # i = parse_edit(tokens, i, node)
    else:
        remove_node(parent, node)
        node = parent

    i = parse_edit(tokens, i, node)

    if node != parent and len(node['children']) == 0:
        remove_node(parent, node)

    debug(parent, tokens, i, 'parse_article_header3 end')

    return i

def parse_for_each(fn, tokens, i, parent):
    n = parent() if callable(parent) else parent
    test = fn(tokens, i, n)
    if (test == i or len(n['children']) == 0) and callable(parent):
        remove_node(n['parent'], n)

    while test != i:
        i = test
        n = parent() if callable(parent) else parent
        test = fn(tokens, i, n)
        if (test == i or len(n['children']) == 0) and callable(parent):
            remove_node(n['parent'], n)

    return i

def parse_json_articles(data, parent):
    if 'articles' in data:
        for article_data in data['articles']:
            parse_json_article(article_data, parent)
    elif 'alineas' in data:
        parse_json_article(data, parent)

    return data

def parse_json_article(data, parent):
    node = create_node(parent, {
        'type': 'article',
        'children': [],
        'order': 1,
        'isNew': False
    })

    node['order'] = data['order']

    if 'alineas' in data:
        parse_json_alineas(data['alineas'], node)

def parse_json_alineas(data, parent):
    text = alinea_lexer.TOKEN_NEW_LINE.join(value for key, value in list(iter(sorted(data.iteritems()))))
    return parse_alineas(text, parent)

def parse_alineas(data, parent):
    tokens = alinea_lexer.tokenize(data.strip())
    parse_for_each(parse_article_header1, tokens, 0, parent)

    if len(parent['children']) == 0:
        parse_raw_article_content(tokens, 0, parent)

def parse_json_amendement(data, node):
    node = create_node(node, {
        'type': 'amendement',
        'order': 1,
        'isNew': False
    })

    text = data['texte']
    text = text.replace(u'</p><p>', u'\n')
    text = re.sub(r'<[^>]*?>', ' ', text)
    text = data['sujet'] + ' '  + text

    tokens = alinea_lexer.tokenize(text)
    parse_for_each(parse_article_header1, tokens, 0, node)

def parse_json_amendements(data, node):
    if 'amendements' in data:
        for amendement_data in data['amendements']:
            parse_json_amendement(amendement_data['amendement'], node)

def parse_data(data):
    node = {'children': []}

    parse_alineas(data, node)

    return node

def parse_json_data(data):
    node = {'children': []}

    parse_json_articles(data, node)
    parse_json_amendements(data, node)

    return node

def resolve_fully_qualified_definitions(node):
    if 'type' in node and node['type'] == 'edit':
        def_nodes = filter_nodes(node, lambda x : x['type'] in def_types)
        # if we have more than 1 definition in a single edit, we assume:
        # - they have different types
        # - the final type of definition is the combination of all those types
        if len(def_nodes) > 1:
            content_nodes = filter(lambda x : len(x['children']) > 0, def_nodes)
            type_nodes = filter(lambda x : len(x['children']) == 0, def_nodes)
            types = []
            for type_node in type_nodes:
                remove_node(node, type_node)
                types.append(type_node)
                del type_node['count']
                # if 'count' in type_node and type_node['count'] == len(content_nodes):
                # FIXME: else we should issue a warning because the count doesn't match and the type qualifier cannot
                # apply
            for content_node in content_nodes:
                children = []
                for child in content_node['children']:
                    children.append(child)
                    remove_node(content_node, child)
                remove_node(node, content_node)
                sorted_types = sorted(types + [content_node], key=lambda x : def_types.index(x['type']))
                type_node = node
                for sorted_type in sorted_types:
                    t = copy_node(sorted_type)
                    push_node(type_node, t)
                    type_node = t
                for child in children:
                    push_node(type_node, child)
    elif 'children' in node and node['children'] > 0:
        for child in node['children']:
            resolve_fully_qualified_definitions(child)

def get_node_ancestors(node):
    a = []
    node = node['parent']
    while node and 'type' in node:
        a.append(node)
        node = node['parent']
    return a

def get_ancestors(node, fn = None):
    ancestors = []
    while node and fn(node):
        ancestors.append(node)
        node = node['parent']
    return ancestors
