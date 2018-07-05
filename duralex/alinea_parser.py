# -*- coding: utf-8 -*-

import re
import sys

import duralex.alinea_lexer as alinea_lexer
import duralex.tree

from duralex.tree import *

import parsimonious

import logging

LOGGER = logging.getLogger('alinea_parser')

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
        [u'neuf', u'neuvième'],
        [u'dix', u'dixième'],
        [u'onze', u'onzième'],
        [u'douze', u'douzième'],
        [u'treize', u'treizième'],
        [u'quatorze', u'quatorzième'],
        [u'quinze', u'quinzième'],
        [u'seize', u'seizième'],
    ]

    word = word.lower()
    word = word.replace(u'È', u'è')

    for i in range(0, len(words)):
        if word in words[i]:
            return i + 1

    return -1

def month_to_number(month):
    return alinea_lexer.TOKEN_MONTH_NAMES.index(month) + 1

def parse_section_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_SECTION_REFERENCE,
        'children': [],
    })

    LOGGER.debug('parse_section_reference %s', str(tokens[i:i+10]))

    grammar = parsimonious.Grammar("""
section_ref = ~"(de )*" "la section " section_order
section_order = ~"\d+"
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['section_order' ])
        capture.visit(tree)
        node['order'] = parse_int(capture.captures['section_order'])
    except parsimonious.exceptions.ParseError:
        remove_node(parent, node)
        return i

    i = parse_reference(tokens, i, node)

    LOGGER.debug('parse_section_reference end %s', str(tokens[i:i+10]))

    return i

def parse_subsection_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_SUBSECTION_REFERENCE,
        'children': [],
    })

    LOGGER.debug('parse_subsection_reference %s', str(tokens[i:i+10]))

    grammar = parsimonious.Grammar("""
sub_section_ref = ~"(de )*" "la sous-section " sub_section_order
sub_section_order = ~"\d+"
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['sub_section_order' ])
        capture.visit(tree)
        node['order'] = parse_int(capture.captures['sub_section_order'])
    except parsimonious.exceptions.ParseError:
        remove_node(parent, node)
        return i

    i = parse_reference(tokens, i, node)

    LOGGER.debug('parse_subsection_reference end %s', str(tokens[i:i+10]))

    return i

def parse_chapter_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_CHAPTER_REFERENCE,
        'children': [],
    })

    LOGGER.debug('parse_chapter_reference %s', str(tokens[i:i+10]))

    grammar = parsimonious.Grammar("""
chapter_ref = ("du chapitre " chapter_order) / ("le chapitre " chapter_order)
chapter_order = roman_number
roman_number = ~"Ier|[IVXLCDM]+(èm)?e?"
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['roman_number' ])
        capture.visit(tree)
        node['order'] = parse_roman_number(capture.captures['roman_number'])
    except parsimonious.exceptions.ParseError:
        remove_node(parent, node)
        return i

    i = parse_reference(tokens, i, node)

    LOGGER.debug('parse_chapter_reference end %s', str(tokens[i:i+10]))

    return i

def parse_paragraph_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_PARAGRAPH_REFERENCE,
        'children': [],
    })

    LOGGER.debug('parse_paragraph_reference %s', str(tokens[i:i+10]))

    grammar = parsimonious.Grammar("""
paragraph_ref = ("du paragraphe " paragraph_order) / ("le paragraphe " paragraph_order)
paragraph_order = ~"\d+"
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['paragraph_order' ])
        capture.visit(tree)
        node['order'] = parse_int(capture.captures['paragraph_order'])
    except parsimonious.exceptions.ParseError:
        remove_node(parent, node)
        return i

    i = parse_reference(tokens, i, node)

    LOGGER.debug('parse_paragraph_reference end %s', str(tokens[i:i+10]))

    return i

def parse_subparagraph_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    LOGGER.debug('parse_subparagraph_definition %s', str(tokens[i:i+10]))

    node = create_node(parent, {
        'type': TYPE_SUBPARAGRAPH_DEFINITION,
        'children': [],
    })

    grammar = parsimonious.Grammar("""
rule = whitespaces subparagraph whitespaces
subparagraph = ~"un"i _ ~"sous-paragraphe"i (_ number)? (_ ~"ainsi"i _ ~"rédigé"i)?

number = ~"[0-9]+"
_ = ~"\s+"
whitespaces = ~"\s*"
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['number'])
        capture.visit(tree)
        if 'number' in capture.captures:
            node['order'] = parse_int(capture.captures['number'])
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_for_each(parse_quote, tokens, i, node)
    except parsimonious.exceptions.ParseError:
        remove_node(parent, node)
        LOGGER.debug('parse_subparagraph_definition none %s', str(tokens[i:i+10]))
        return i

    LOGGER.debug('parse_subparagraph_definition end %s', str(tokens[i:i+10]))

    return i

def parse_law_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    j = i

    LOGGER.debug('parse_law_reference %s', str(tokens[i:i+10]))

    grammar = parsimonious.Grammar("""
law_ref = _* (explicit_law_ref / lookback_law_ref) _*
explicit_law_ref = (pronoun _*) law_type _ ((number_abvr _* law_id _ "du" _ date) / (number_abvr _* law_id) / ("du" _ date))
lookback_law_ref = (pronoun _*) "même" _ law_type

law_type = ~"loi( +constitutionnelle| +organique)?|ordonnance|d[ée]cret(-loi)?|arr[êe]t[ée]|circulaire"i
law_id = ~"[0-9]+[-‑][0-9]+"

date = day _ month _ year
day = ~"1er|[12][0-9]|3[01]|[1-9]"i
month = ~"janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre"i
year = ~"(1[5-9]|2[0-9])[0-9]{2}"

pronoun = ~"la"i / ~"de la"i / ~"de l'"i / ~"l'"i
number_abvr = ~"n°|no"i
_ = ~"\s+"
    """)

    node = create_node(parent, {
        'type': TYPE_LAW_REFERENCE,
        'id': '',
        'children': [],
    })

    try:
        tree = grammar.match(''.join( tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))

        capture = CaptureVisitor(['law_type', 'lookback_law_ref', 'law_id', 'year', 'month', 'day'])
        capture.visit(tree)

        if 'lookback_law_ref' in capture.captures:
            mark_as_lookback_reference(node)
        else:
            if 'law_id' in capture.captures:
                node['id'] = capture.captures['law_id']
            if 'law_type' in capture.captures:
                node['lawType'] = capture.captures['law_type']
            if 'year' in capture.captures:
                node['lawDate'] = '%s-%i-%s' % (capture.captures['year'], month_to_number( capture.captures['month'] ), capture.captures['day'] )
    except parsimonious.exceptions.ParseError as e:
        remove_node(parent, node)
        return i

    i = alinea_lexer.skip_spaces(tokens, i)
    if i < len(tokens) and tokens[i] == u'modifiant':
        j = alinea_lexer.skip_to_token(tokens, i, 'code')
        if j < len(tokens):
            i = parse_code_reference(tokens, j, node)

    # les mots
    i = parse_one_of(
        [
            parse_word_reference,
        ],
        tokens,
        i,
        node
    )

    LOGGER.debug('parse_law_reference end %s', str(tokens[i:i+10]))

    return i

def parse_multiplicative_adverb(tokens, i, node):
    if i >= len(tokens):
        return i

    grammar = parsimonious.Grammar("""
multiplicative_adverb = ( multiplicative_adverb_units_before_decades? multiplicative_adverb_decades ) / multiplicative_adverb_units
multiplicative_adverb_units = ~"semel|bis|ter|quater|(quinqu|sex|sept|oct|no[nv])ies"i
multiplicative_adverb_units_before_decades = ~"un(de?)?|duo(de)?|ter|quater|quin|sex?|sept|octo|novo"i
multiplicative_adverb_decades = ~"(dec|v[ei]c|tr[ei]c|quadrag|quinquag|sexag|septuag|octog|nonag)ies"i
""")

    try:
        tree = grammar.match(''.join(tokens[i:]))
        node['is' + tokens[i].title()] = True
        # ? FIXME: we should re-asses how we handle multiplicative adverbs
        # ? We might want to include them in the actual ID.
        # ? Code might look like that:
        # ? for k, adverb in enumerate(alinea_lexer.TOKEN_MULTIPLICATIVE_ADVERBS):
        # ?   if re.fullmatch(adverb, tokens[j]):
        j = i
        i += len(alinea_lexer.tokenize(tree.text))
        i = alinea_lexer.skip_spaces(tokens, i)
    except parsimonious.exceptions.ParseError:
        return i

    return i

def parse_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    i = parse_one_of(
        [
            parse_article_definition,
            parse_alinea_definition,
            parse_mention_definition,
            parse_header1_definition,
            parse_header2_definition,
            parse_header3_definition,
            parse_sentence_definition,
            parse_word_definition,
            parse_title_definition,
            parse_subparagraph_definition
        ],
        tokens,
        i,
        parent
    )

    return i

def parse_sentence_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    LOGGER.debug('parse_sentence_definition %s', str(tokens[i:i+10]))
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
                lambda : create_node(parent, {'type': TYPE_SENTENCE_DEFINITION, 'children': []})
            )
        else:
            create_node(parent, {'type': TYPE_SENTENCE_DEFINITION, 'count': count})
    else:
        LOGGER.debug('parse_sentence_definition none %s', str(tokens[i:i+10]))
        return j

    LOGGER.debug('parse_sentence_definition end %s', str(tokens[i:i+10]))

    return i

def parse_word_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_WORD_DEFINITION,
    })
    LOGGER.debug('parse_word_definition %s', str(tokens[i:i+10]))

    j = i
    i = parse_position(tokens, i, node)
    i = parse_scope(tokens, i, node)
    # le mot
    # les mots
    # des mots
    if tokens[i].lower() in [u'le', u'les', u'des'] and tokens[i + 2].startswith(u'mot'):
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_for_each(parse_quote, tokens, i, node)
        # i = alinea_lexer.skip_spaces(tokens, i)
    # le nombre
    # le chiffre
    # le taux
    elif tokens[i].lower() == u'le' and tokens[i + 2] in [u'nombre', u'chiffre', u'taux']:
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_quote(tokens, i, node)
    # les dispositions suivantes \n "
    elif tokens[i].lower() == u'les' and tokens[i+2] == 'dispositions' and tokens[i+4] == u'suivantes':
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_for_each(parse_quote, tokens, i, node)
        i = alinea_lexer.skip_spaces(tokens, i)
    # "
    elif tokens[i] == alinea_lexer.TOKEN_DOUBLE_QUOTE_OPEN:
        i = parse_for_each(parse_quote, tokens, i, node)
        i = alinea_lexer.skip_spaces(tokens, i)
    # la référence
    # les références
    elif tokens[i].lower() in [u'la', u'les'] and tokens[i + 2].startswith(u'référence'):
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_quote(tokens, i, node)
    else:
        LOGGER.debug('parse_word_definition none %s', str(tokens[i:i+10]))
        remove_node(parent, node)
        return j
    LOGGER.debug('parse_word_definition end %s', str(tokens[i:i+10]))
    return i

def parse_article_definition(tokens, i, parent):
    if i >= len(tokens):
        return i
    LOGGER.debug('parse_article_definition %s', str(tokens[i:i+10]))

    #node = create_node(parent, {
    #    'type': TYPE_ARTICLE_DEFINITION,
    #    'children': [],
    #})

    # Small-scale experiment of a function transforming a “Parsimonious syntactic tree” into a “DuraLex semantic tree”
    # Previous code is commented (until 64ff59b) - but both methods work
    tableToSemanticTree = {
        'article_id': {
            'type': TYPE_ARTICLE_DEFINITION,
            'property': 'id',
            'dynamic': 'childrify',
        },
        'quoted': {
            'type': TYPE_QUOTE,
            'property': 'words',
            'replace': [('"', '')],
        },
    }
    toSemanticTree = ToSemanticTreeVisitor(tableToSemanticTree, parent)

    grammar = parsimonious.Grammar("""
rule = whitespaces an_article whitespaces

an_article = ( ~"un +"i / ~"l['’] *"i ) ~"article"i (_ article_id (_ so_that_written not_a_quote quoted)?)?

so_that_written = ~"ainsi +rédigé"i

article_id = numbered_article / named_article

# Classically numbered article
numbered_article = article_type ~"[0-9]+(er|ème|e)?" ( ~" *[-‐‑] *| *\.| +" ( ~"[A-Z0-9]+(er|ème|e)?" / multiplicative_adverb ) )*

# Optional prefix
article_type = ~"\*?\*?((L\.O|LO|L|R|D|A)\*?\*?\.? *)?"

# Specific article names
named_article = ~"annexe|ex[ée]cution|unique|(pr[ée])?liminaire|pr[ée]ambule"i

not_a_quote = ~"[^\\\"]*"
quoted = "\\"" ~"[^\\n\\\"]+(\\n\\\"[^\\n\\\"]+)*" "\\""

multiplicative_adverb = ( multiplicative_adverb_units_before_decades? multiplicative_adverb_decades ) / multiplicative_adverb_units
multiplicative_adverb_units = ~"semel|bis|ter|quater|(quinqu|sex|sept|oct|no[nv])ies"i
multiplicative_adverb_units_before_decades = ~"un(de?)?|duo(de)?|ter|quater|quin|sex?|sept|octo|novo"i
multiplicative_adverb_decades = ~"(dec|v[ei]c|tr[ei]c|quadrag|quinquag|sexag|septuag|octog|nonag)ies"i

_ = ~"\s+"
whitespaces = ~"\s*"
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        toSemanticTree.visit(tree)
        if toSemanticTree.node == None: # should be improved or possibly deleted: are there definitions without quotes?
            create_node(parent, {
                'type': TYPE_ARTICLE_DEFINITION,
                'children': [],
            })
        #capture = CaptureVisitor(['article_id', 'multiplicative_adverb'])
        #capture.visit(tree)
        #if 'article_id' in capture.captures:
        #    node['id'] = capture.captures['article_id']
        #if 'multiplicative_adverb' in capture.captures:
        #    node['is' + capture.captures['multiplicative_adverb'].title()] = True
        #i = alinea_lexer.skip_to_quote_start(tokens, i)
        #i = parse_for_each(parse_quote, tokens, i, node)
    except parsimonious.exceptions.ParseError:
        LOGGER.debug('parse_article_definition none %s', str(tokens[i:i+10]))
        #remove_node(parent, node)
        return i

    LOGGER.debug('parse_article_definition end %s', str(tokens[i:i+10]))

    return i

def parse_alinea_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    LOGGER.debug('parse_alinea_definition %s', str(tokens[i:i+10]))

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
                lambda: create_node(parent, {'type': TYPE_ALINEA_DEFINITION, 'children': []})
            )
        else:
            node = create_node(parent, {'type': TYPE_ALINEA_DEFINITION, 'count': count})
    else:
        LOGGER.debug('parse_alinea_definition none %s', str(tokens[i:i+10]))
        return i

    LOGGER.debug('parse_alinea_definition end %s', str(tokens[i:i+10]))

    return i

def parse_mention_definition(tokens, i, parent):
    if i >= len(tokens):
        return i
    node = create_node(parent, {
        'type': TYPE_MENTION_DEFINITION,
    })
    LOGGER.debug('parse_mention_definition %s', str(tokens[i:i+10]))
    # la mention
    if tokens[i].lower() == u'la' and tokens[i + 2] == u'mention':
        i += 4
    else:
        LOGGER.debug('parse_mention_definition none %s', str(tokens[i:i+10]))
        remove_node(parent, node)
        return i
    # :
    if tokens[i] == ':':
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_for_each(parse_quote, tokens, i, node)

    LOGGER.debug('parse_mention_definition end %s', str(tokens[i:i+10]))

    return i

def parse_header1_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    LOGGER.debug('parse_header1_definition %s', str(tokens[i:i+10]))
    # un {romanPartNumber}
    if tokens[i].lower() == u'un' and is_roman_number(tokens[i + 2]):
        node = create_node(parent, {
            'type': TYPE_HEADER1_DEFINITION,
            'order': parse_roman_number(tokens[i + 2]),
            })
        i += 4
        i = alinea_lexer.skip_spaces(tokens, i)
        if i + 2 < len(tokens) and tokens[i] == u'ainsi' and tokens[i + 2] == u'rédigé':
            i = alinea_lexer.skip_to_quote_start(tokens, i)
            i = parse_quote(tokens, i, node)
    # des {start} à {end}
    elif (tokens[i].lower() == u'des' and is_roman_number(tokens[i + 2])
        and tokens[i + 4] == u'à' and is_roman_number(tokens[i + 6])):
        start = parse_roman_number(tokens[i + 2])
        end = parse_roman_number(tokens[i + 6])
        i += 8
        # ainsi rédigés
        if (i + 2 < len(tokens) and tokens[i + 2].startswith(u'rédigé')
            or (i + 4 < len(tokens) and tokens[i + 4].startswith(u'rédigé'))):
            i = alinea_lexer.skip_to_quote_start(tokens, i + 4)
            i = parse_for_each(
                parse_quote,
                tokens,
                i,
                lambda : create_node(parent, {'type': TYPE_HEADER1_DEFINITION, 'order': start + len(parent['children']), 'children': []})
            )
    else:
        LOGGER.debug('parse_header1_definition end %s', str(tokens[i:i+10]))
        return i

    return i

def parse_header2_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    LOGGER.debug('parse_header2_definition %s', str(tokens[i:i+10]))

    # un ... ° ({articlePartRef})
    if tokens[i].lower() == u'un' and ''.join(tokens[i + 2:i + 5]) == u'...' and tokens[i + 6] == u'°':
        node = create_node(parent, {
            'type': TYPE_HEADER2_DEFINITION,
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
            'type': TYPE_HEADER2_DEFINITION,
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
                lambda : create_node(parent, {'type': TYPE_HEADER2_DEFINITION, 'order': start + len(parent['children']), 'children': []})
            )
    else:
        LOGGER.debug('parse_header2_definition end %s', str(tokens[i:i+10]))
        return i

    return i

def parse_header3_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    LOGGER.debug('parse_header3_definition %s', str(tokens[i:i+10]))

    # un {orderLetter}
    if tokens[i].lower() == u'un' and re.compile(u'^[a-z]$').match(tokens[i + 2]):
        node = create_node(parent, {
            'type': TYPE_HEADER3_DEFINITION,
            'order': ord(str(tokens[i + 2])) - ord('a') + 1,
            })
        i += 4
        i = alinea_lexer.skip_spaces(tokens, i)
        if i < len(tokens) and tokens[i] == u'ainsi' and tokens[i + 2] == u'rédigé':
            i = alinea_lexer.skip_to_quote_start(tokens, i + 4)
            i = parse_quote(tokens, i, node)
    # des {orderLetter} à {orderLetter}
    elif (tokens[i].lower() == u'des' and re.compile(u'^[a-z]$').match(tokens[i + 2])
        and tokens[i + 4] == u'à' and re.compile(u'^[a-z]$').match(tokens[i + 6])):
        start = ord(str(tokens[i + 2])) - ord('a') + 1
        end = ord(str(tokens[i + 6])) - ord('a') + 1
        i += 8
        # ainsi rédigés
        if (i + 2 < len(tokens) and tokens[i + 2].startswith(u'rédigé')
            or (i + 4 < len(tokens) and tokens[i + 4].startswith(u'rédigé'))):
            i = alinea_lexer.skip_to_quote_start(tokens, i + 4)
            i = parse_for_each(
                parse_quote,
                tokens,
                i,
                lambda : create_node(parent, {'type': TYPE_HEADER3_DEFINITION, 'order': start + len(parent['children']), 'children': []})
            )
    else:
        LOGGER.debug('parse_header3_definition end %s', str(tokens[i:i+10]))
        return i

    return i

def parse_article_id(tokens, i, node):

    grammar = parsimonious.Grammar("""
rule = whitespaces article_id whitespaces

article_id = numbered_article / named_article

# Classically numbered article
numbered_article = article_type ~"[0-9]+(er|ème|e)?" ( ~" *[-‐‑] *| *\.| +" ( ~"[A-Z0-9]+(er|ème|e)?" / multiplicative_adverb ) )*

# Optional prefix
article_type = ~"\*?\*?((L\.O|LO|L|R|D|A)\*?\*?\.? *)?"

# Specific article names
named_article = ~"annexe|ex[ée]cution|unique|(pr[ée])?liminaire|pr[ée]ambule"i

multiplicative_adverb = ( multiplicative_adverb_units_before_decades? multiplicative_adverb_decades ) / multiplicative_adverb_units
multiplicative_adverb_units = ~"semel|bis|ter|quater|(quinqu|sex|sept|oct|no[nv])ies"i
multiplicative_adverb_units_before_decades = ~"un(de?)?|duo(de)?|ter|quater|quin|sex?|sept|octo|novo"i
multiplicative_adverb_decades = ~"(dec|v[ei]c|tr[ei]c|quadrag|quinquag|sexag|septuag|octog|nonag)ies"i

whitespaces = ~"\s*"
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['article_id', 'multiplicative_adverb'])
        capture.visit(tree)
        node['id'] = capture.captures['article_id']
        if 'multiplicative_adverb' in capture.captures:
            node['is' + capture.captures['multiplicative_adverb'].title()] = True
    except parsimonious.exceptions.ParseError:
        return i

    if not node['id'] or is_space(node['id']):
        del node['id']

    return i

def parse_title_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_TITLE_REFERENCE,
        'children': [],
    })

    LOGGER.debug('parse_title_reference %s', str(tokens[i:i+10]))

    j = i
    i = parse_position(tokens, i, node)
    i = parse_scope(tokens, i, node)

    grammar = parsimonious.Grammar("""
title_ref = pronoun whitespace* "titre" whitespace* title_order
title_order = roman_number

roman_number = ~"Ier|[IVXLCDM]+(èm)?e?"
whitespace = ~"\s+"
pronoun = ~"le"i / ~"du"i
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['roman_number'])
        capture.visit(tree)
        node['order'] = parse_roman_number(capture.captures['roman_number'])
    except parsimonious.exceptions.ParseError:
        remove_node(parent, node)
        return j

    i = parse_reference(tokens, i, node)

    LOGGER.debug('parse_title_reference end %s', str(tokens[i:i+10]))

    return i

def parse_title_definition(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_TITLE_DEFINITION,
        'children': [],
    })

    LOGGER.debug('parse_title_definition %s', str(tokens[i:i+10]))

    grammar = parsimonious.Grammar("""
rule = whitespaces a_title whitespaces

a_title = ~"un"i _ ~"titre"i _ roman_number (_ ~"ainsi"i _ ~"rédigé"i)?

roman_number = ~"Ier|[IVXLCDM]+(èm)?e?"
_ = ~"\s+"
whitespaces = ~"\s*"
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['roman_number'])
        capture.visit(tree)
        node['order'] = parse_roman_number(capture.captures['roman_number'])
        i = alinea_lexer.skip_to_quote_start(tokens, i)
        i = parse_for_each(parse_quote, tokens, i, node)
    except parsimonious.exceptions.ParseError:
        LOGGER.debug('parse_title_definition none %s', str(tokens[i:i+10]))
        remove_node(parent, node)
        return i

    LOGGER.debug('parse_title_definition end %s', str(tokens[i:i+10]))

    return i

def parse_code_part_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_CODE_PART_REFERENCE,
        'children': [],
    })

    LOGGER.debug('parse_code_part_reference %s', str(tokens[i:i+10]))

    j = i
    i = parse_position(tokens, i, node)
    i = parse_scope(tokens, i, node)

    grammar = parsimonious.Grammar("""
code_part_ref = pronoun whitespace+ code_part_order whitespace+ "partie" whitespace+
code_part_order = number_word

pronoun = ~"la"i / ~"de la"i
number_word = "une" / "un" / "première" / "premier" / "deuxième" / "deux" / "seconde" / "second" / "troisième" / "trois" / "quatrième" / "quatre" / "cinquième" / "cinq" / "sixième" / "six" / "septième" / "sept" / "huitième" / "huit" / "neuvième" / "neuf" / "dixième" / "dix" / "onzième" / "onze" / "douzième" / "douze" / "treizième" / "treize" / "quatorzième" / "quatorze" / "quinzième" / "quinze" / "seizième" / "seize"
whitespace = ~"\s+"
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        
        capture = CaptureVisitor(['number_word' ])
        capture.visit(tree)
        node['order'] = word_to_number(capture.captures['number_word'])

        i = parse_code_reference(tokens, i, node)
    except parsimonious.exceptions.ParseError as e:
        remove_node(parent, node)
        return j

    LOGGER.debug('parse_code_part_reference end %s', str(tokens[i:i+10]))

    return i

def parse_book_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_BOOK_REFERENCE,
        'children': [],
    })

    LOGGER.debug('parse_book_reference %s', str(tokens[i:i+10]))

    grammar = parsimonious.Grammar("""
book_ref = pronoun whitespace* "livre" whitespace book_order
book_order = roman_number

roman_number = ~"Ier|[IVXLCDM]+(èm)?e?"
whitespace = ~"\s+"
pronoun = ~"du"i / ~"le"i
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i = parse_position(tokens, i, node)
        i = parse_scope(tokens, i, node)
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['roman_number' ])
        capture.visit(tree)
        node['order'] = parse_roman_number(capture.captures['roman_number'])
        i = parse_reference(tokens, i, node)
    except parsimonious.exceptions.ParseError as e:
        remove_node(parent, node)
        return i

    LOGGER.debug('parse_book_reference end %s', str(tokens[i:i+10]))

    return i

def parse_scope(tokens, i, parent):
    if i >= len(tokens):
        return i

    LOGGER.debug('parse_scope %s', str(tokens[i:i+10]))

    grammar = parsimonious.Grammar("""
rule = whitespaces scope_end whitespaces
scope_end = ~"la +fin +(de|du)"i

_ = ~"\s+"
whitespaces = ~"\s*"
    """)

    node = None
    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        parent['scope'] = 'end'
    except parsimonious.exceptions.ParseError as e:
        return i

    LOGGER.debug('parse_scope end %s', str(tokens[i:i+10]))

    return i

def parse_bill_article_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    LOGGER.debug('parse_bill_article_reference %s', str(tokens[i:i+10]))

    # cet article
    if tokens[i] == u'cet' and tokens[i + 2] == u'article':
        i += 4
        article_refs = filter_nodes(
            get_root(parent),
            lambda n: 'type' in n and n['type'] == TYPE_BILL_ARTICLE_REFERENCE
        )
        # the last one in order of traversal is the previous one in order of syntax
        article_ref = copy_node(article_refs[-1])
        push_node(parent, article_ref)

    LOGGER.debug('parse_bill_article_reference end %s', str(tokens[i:i+10]))

    return i

def parse_article_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_ARTICLE_REFERENCE,
    })

    LOGGER.debug('parse_article_reference %s', str(tokens[i:i+10]))

    j = i
    i = parse_position(tokens, i, node)
    i = parse_scope(tokens, i, node)
    # de l'article
    # à l'article
    if tokens[i].lower() in [u'de', u'à'] and tokens[i + 2] == u'l' and tokens[i + 4] == u'article':
        i += 5
        i = alinea_lexer.skip_spaces(tokens, i)
        i = parse_article_id(tokens, i, node)
    # l'article
    elif tokens[i].lower() == u'l' and tokens[i + 2].startswith(u'article'):
        i += 3
        i = alinea_lexer.skip_spaces(tokens, i)
        i = parse_article_id(tokens, i, node)
    # les articles
    # des articles
    elif tokens[i].lower() in [u'des', u'les'] and tokens[i + 2].startswith(u'article'):
        i += 3
        i = alinea_lexer.skip_spaces(tokens, i)
        i = parse_article_id(tokens, i, node)
        i = alinea_lexer.skip_spaces(tokens, i)
        nodes = []
        while tokens[i] == u',':
            i += 2
            nodes.append(create_node(parent, {'type':TYPE_ARTICLE_REFERENCE}))
            i = parse_article_id(tokens, i, nodes[-1])
            i = alinea_lexer.skip_spaces(tokens, i)
        if tokens[i] == u'et':
            i += 2
            nodes.append(create_node(parent, {'type':TYPE_ARTICLE_REFERENCE}))
            i = parse_article_id(tokens, i, nodes[-1])
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
                parse_word_reference,
                parse_alinea_reference
            ],
            tokens,
            i,
            node
        )
        # if there are are descendant *-reference nodes parsed by the previous call to
        # parse_one_of, we must make sure they apply to all the article-reference nodes
        # we just created
        if len(node['children']) != 0:
            for n in nodes:
                for c in node['children']:
                    push_node(n, copy_node(c))
        return i
    # elif tokens[i] == u'un' and tokens[i + 2] == u'article':
    #     i += 4
    # Article {articleNumber}
    elif tokens[i].lower().startswith(u'article'):
        i += 1
        i = alinea_lexer.skip_spaces(tokens, i)
        i = parse_article_id(tokens, i, node)
    # le même article
    # du même article
    elif tokens[i].lower() in [u'le', u'du'] and tokens[i + 2] == u'même' and tokens[i + 4] == u'article':
        i += 6
        article_refs = filter_nodes(
            get_root(parent),
            lambda n: 'type' in n and n['type'] == TYPE_ARTICLE_REFERENCE
        )
        # the last one in order of traversal is the previous one in order of syntax
        # don't forget the current node is in the list too => -2 instead of -1
        article_ref = copy_node(article_refs[-2])
        push_node(parent, article_ref)
        remove_node(parent, node)
    else:
        remove_node(parent, node)
        return j

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
            parse_word_reference,
            parse_alinea_reference
        ],
        tokens,
        i,
        node
    )

    # i = parse_quote(tokens, i, node)

    LOGGER.debug('parse_article_reference end %s', str(tokens[i:i+10]))

    return i

def parse_position(tokens, i, node):
    if i >= len(tokens):
        return i

    grammar = parsimonious.Grammar("""
rule = whitespaces position whitespaces

position = ~"après|avant|au +début|à +la +fin"i

whitespaces = ~"\s*"
""")

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['position'])
        capture.visit(tree)
        if re.fullmatch( r' *après *', tree.text, flags=re.IGNORECASE ):
            node['position'] = 'after'
        elif re.fullmatch( r' *avant *', tree.text, flags=re.IGNORECASE ):
            node['position'] = 'before'
        elif re.fullmatch( r' *à +la +fin *', tree.text, flags=re.IGNORECASE ):
            node['position'] = 'beginning'
        elif re.fullmatch( r' *au +début *', tree.text, flags=re.IGNORECASE ):
            node['position'] = 'end'
    except parsimonious.exceptions.ParseError as e:
        return i

    return i

def parse_alinea_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_ALINEA_REFERENCE,
    })
    LOGGER.debug('parse_alinea_reference %s', str(tokens[i:i+10]))

# introduced in c2eb094 but unused and there is a grammar syntax error -> to be improved
#    grammar = parsimonious.Grammar("""
#alinea_ref = _* ("à" _)? (pronoun _)? (explicit_alinea_ref / last_alinea_ref / before_last_alinea_ref / lookback_alinea_ref) _*
#before_last_alinea_ref = ("avant" _ "dernier" _ "alinéa" / "avant-dernier" _ "alinéa")
#last_alinea_ref = "dernier" _ "alinéa"
#explicit_alinea_ref = (ordinal_adjective_number / ) _ "alinéa"
#lookback_alinea_ref = "même" _ "alinéa"
#
#alinea_ref_list = (alinea_ref _* ",") _ "et"
#
#whitespace = ~"\s+"
#ordinal_adjective_number = ~"première|seconde|dernière|dixième|onzième|douzième|treizième|quatorzième|quinzième|seizième|(dix-|vingt-|trente-|quarante-|cinquante-|soixante-|soixante-dix-|quatre-vingt-|quatre-vingt-dix-)?(et-)?(un|deux|trois|quatr|cinqu|six|sept|huit|neuv)ième"i
#pronoun = / ~"de l'"i / ~"du"i / ~"les"i / ~"le"i / ~"au"i / ~"l'"i
#    """)

    j = i
    i = parse_position(tokens, i, node)
    i = parse_scope(tokens, i, node)
    # le {order} alinéa
    # du {order} alinéa
    # au {order} alinéa
    if tokens[i].lower() in [u'du', u'le', u'au'] and is_number_word(tokens[i + 2]) and tokens[i + 4].startswith(u'alinéa'):
        node['order'] = word_to_number(tokens[i + 2])
        i += 6
    # l'alinéa
    elif tokens[i].lower() == u'l' and tokens[i + 2].startswith(u'alinéa'):
        node['order'] = parse_int(tokens[i + 4])
        i += 6
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
            lambda n: 'type' in n and n['type'] == TYPE_ALINEA_REFERENCE
        )
        # the lduralex.tree.one in order of traversal is the previous one in order of syntax
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
    # les {order} alinéas
    elif tokens[i].lower() == u'les' and is_number_word(tokens[i+2].lower()) and tokens[i + 4] == u'alinéas':
        node['order'] = parse_int(tokens[i + 2])
        i += 6
    # les alinéas
    # des alinéas
    elif tokens[i].lower() in [u'les', u'des'] and tokens[i + 2] == u'alinéas':
        node['order'] = parse_int(tokens[i + 4])
        i += 5
        i = alinea_lexer.skip_spaces(tokens, i)
        nodes = []
        while tokens[i] == u',':
            nodes.append(create_node(parent, {
                'type': TYPE_ALINEA_REFERENCE,
                'order': parse_int(tokens[i + 2])
            }))
            i += 3
            i = alinea_lexer.skip_spaces(tokens, i)
        if tokens[i] == u'et':
            i += 2
            nodes.append(create_node(parent, {
                'type': TYPE_ALINEA_REFERENCE,
                'order': parse_int(tokens[i])
            }))
            i += 2
        i = parse_article_part_reference(tokens, i, node)
        if len(node['children']) != 0:
            for n in nodes:
                for c in node['children']:
                    push_node(n, copy_node(c))
        return i
    else:
        LOGGER.debug('parse_alinea_reference none %s', str(tokens[i:i+10]))
        remove_node(parent, node)
        return j

    # i = parse_article_part_reference(tokens, i, node)
    i = parse_reference_list(tokens, i, node)
    # i = parse_quote(tokens, i, node)

    LOGGER.debug('parse_alinea_reference end %s', str(tokens[i:i+10]))

    return i

def parse_sentence_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_SENTENCE_REFERENCE,
    })
    LOGGER.debug('parse_sentence_reference %s', str(tokens[i:i+10]))

    j = i
    i = parse_position(tokens, i, node)
    i = parse_scope(tokens, i, node)

    grammar = parsimonious.Grammar("""
entry = ( ( ( ~"de"i / ~"à"i ) whitespace )? ( ~"la"i / ~"une"i ) whitespace ordinal_adjective_number whitespace ~"phrase"i ) / ( ( ~"des +"i / ~"les +"i ) ( cardinal_adjective_number whitespace )? ordinal_adjective_number ~"s"? whitespace ~"phrases" )

ordinal_adjective_number = ~"première|seconde|dernière|dixième|onzième|douzième|treizième|quatorzième|quinzième|seizième|(dix-|vingt-|trente-|quarante-|cinquante-|soixante-|soixante-dix-|quatre-vingt-|quatre-vingt-dix-)?(et-)?(un|deux|trois|quatr|cinqu|six|sept|huit|neuv)ième"i

cardinal_adjective_number = ~"(vingt|trente|quarante|cinquante|soixante|septante|quatre-vingt|huitante|octante|nonante)(-et-un|-deux|-trois|-quatre|-cinq|-six|-sept|-huit|-neuf)?|(soixante|quatre-vingt)(-et-onze|-douze|-treize|-quatorze|-quinze|-seize|-dix-sept|-dix-huit|-dix-neuf)?|zéro|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|dix-sept|dix-huit|dix-neuf|quatre-vingt-un|quatre-vingt-onze"i

whitespace = ~" +"
""")

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        i = alinea_lexer.skip_spaces(tokens, i)
        capture = CaptureVisitor(['cardinal_adjective_number', 'ordinal_adjective_number'])
        capture.visit(tree)
        node['order'] = word_to_number(capture.captures['ordinal_adjective_number'])
        if 'cardinal_adjective_number' in capture.captures and capture.captures['cardinal_adjective_number']:
            node['order'] = [0, word_to_number(capture.captures['cardinal_adjective_number'])]
    except parsimonious.exceptions.ParseError as e:
        LOGGER.debug('parse_sentence_reference none %s', str(tokens[i:i+10]))
        remove_node(parent, node)
        return j

    i = parse_article_part_reference(tokens, i, node)

    LOGGER.debug('parse_sentence_reference end %s', str(tokens[i:i+10]))

    fix_incomplete_references(parent, node)

    return i

def fix_incomplete_references(parent, node):
    if len(parent['children']) >= 2:
        for child in parent['children']:
            if child['type'] == TYPE_INCOMPLETE_REFERENCE:
                # set the actual reference type
                child['type'] = node['type']
                # copy all the child of the fully qualified reference node
                for c in node['children']:
                    push_node(child, copy_node(c))

def parse_lookback_reference(tokens, i, parent):
    if i >= len(tokens):
        return i
 
    if tokens[i] == u'Il':
        create_node(parent, {
            'type': TYPE_LOOKBACK_REFERENCE,
        })

        i += 2
    return i

def parse_incomplete_reference(tokens, i, parent):
    if i >= len(tokens):
        return i
    node = create_node(parent, {
        'type': TYPE_INCOMPLETE_REFERENCE,
    })
    j = i
    i = parse_position(tokens, i, node)
    i = parse_scope(tokens, i, node)
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

def parse_word_reference(tokens, i, parent):
    if i >= len(tokens):
        return i
    
    node = create_node(parent, {
        'type': TYPE_WORD_REFERENCE
    })

    LOGGER.debug('parse_word_reference %s', str(tokens[i:i+10]))

    grammar = parsimonious.Grammar("""
word_ref = not_a_word* (positional_conjunction whitespace)* pronoun whitespace* word_ref_type not_double_quote*
word_ref_type = "mots" / "mot" / "nombre" / "chiffre" / "taux" / "références" / "référence"

pronoun = ~"les"i / ~"le"i / ~"des"i / ~"la"i / ~"l'"i
whitespace = ~"\s+"
not_double_quote = ~"[^\\"]*"
positional_conjunction = ~"après"i / ~"avant"i / ~"au début"i / ~"à la fin"i
not_a_word = ~"\W*"
    """)

    position = {
        'après': 'after',
        'avant': 'before',
        'au début': 'begining',
        'à la fin': 'end',
    }

    i = parse_scope(tokens, i, node)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['positional_conjunction' ])
        capture.visit(tree)
        if 'positional_conjunction' in capture.captures:
            node['position'] = position[capture.captures['positional_conjunction'].lower()]
        i = parse_quote(tokens, i, node)
    except parsimonious.exceptions.ParseError:
        remove_node(parent, node)
        return i

    i = alinea_lexer.skip_to_next_word(tokens, i)
    i = parse_reference(tokens, i, node)
    
    LOGGER.debug('parse_word_reference end %s', str(tokens[i:i+10]))

    return i

def parse_header2_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_HEADER2_REFERENCE
    })
    LOGGER.debug('parse_header2_reference %s', str(tokens[i:i+10]))
    j = i
    i = parse_position(tokens, i, node)
    i = parse_scope(tokens, i, node)

    grammar = parsimonious.Grammar("""
header2_ref = whitespace* pronoun whitespace* ("même" whitespace)* header2_order whitespace*
header2_order = ~"\d+" "°" (whitespace multiplicative_adverb)*

whitespace = ~"\s+"
pronoun = ~"le"i / ~"du"i / "au"

multiplicative_adverb = ( multiplicative_adverb_units_before_decades? multiplicative_adverb_decades ) / multiplicative_adverb_units
multiplicative_adverb_units = ~"semel|bis|ter|quater|(quinqu|sex|sept|oct|no[nv])ies"i
multiplicative_adverb_units_before_decades = ~"un(de?)?|duo(de)?|ter|quater|quin|sex?|sept|octo|novo"i
multiplicative_adverb_decades = ~"(dec|v[ei]c|tr[ei]c|quadrag|quinquag|sexag|septuag|octog|nonag)ies"i
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))

        capture = CaptureVisitor(['header2_order', 'multiplicative_adverb'])
        capture.visit(tree)
        
        if 'multiplicative_adverb' in capture.captures:
            node['is' + capture.captures['multiplicative_adverb'].title()] = True
        node['order'] = parse_int(capture.captures['header2_order'])

        parse_article_part_reference(tokens, i, node)
    except parsimonious.exceptions.ParseError as e:
        remove_node(parent, node)
        return j
    
    LOGGER.debug('parse_header2_reference end %s', str(tokens[i:i+10]))
    
    return i

def parse_header3_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_HEADER3_REFERENCE
    })

    LOGGER.debug('parse_header3_reference %s', str(tokens[i:i+10]))

    j = i
    i = parse_position(tokens, i, node)
    i = parse_scope(tokens, i, node)

    grammar = parsimonious.Grammar("""
header3_ref = whitespaces pronoun _ ("même" _)* header3_order whitespaces
header3_order = ~"[a-z]" (_ multiplicative_adverb)*

_ = ~"\s+"
whitespaces = ~"\s*"
pronoun = ~"le"i / ~"du"i / ~"au"i

multiplicative_adverb = ( multiplicative_adverb_units_before_decades? multiplicative_adverb_decades ) / multiplicative_adverb_units
multiplicative_adverb_units = ~"semel|bis|ter|quater|(quinqu|sex|sept|oct|no[nv])ies"i
multiplicative_adverb_units_before_decades = ~"un(de?)?|duo(de)?|ter|quater|quin|sex?|sept|octo|novo"i
multiplicative_adverb_decades = ~"(dec|v[ei]c|tr[ei]c|quadrag|quinquag|sexag|septuag|octog|nonag)ies"i
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['header3_order', 'multiplicative_adverb'])
        capture.visit(tree)

        if 'multiplicative_adverb' in capture.captures:
            node['is' + capture.captures['multiplicative_adverb'].title()] = True
        node['order'] = ord(capture.captures['header3_order']) - ord('a') + 1
    except parsimonious.exceptions.ParseError as e:
        remove_node(parent, node)
        return j

    i = parse_article_part_reference(tokens, i, node)
    
    LOGGER.debug('parse_header3_reference end %s', str(tokens[i:i+10]))
    
    return i

def parse_header1_reference(tokens, i, parent):
    if i >= len(tokens):
        return i
    
    node = create_node(parent, {
        'type': TYPE_HEADER1_REFERENCE,
    })
    
    LOGGER.debug('parse_header1_reference %s', str(tokens[i:i+10]))

    j = i
    i = parse_position(tokens, i, node)
    i = parse_scope(tokens, i, node)

    grammar = parsimonious.Grammar("""
header1_ref = whitespace* pronoun whitespace* header1_order whitespace*
header1_order = roman_number (whitespace multiplicative_adverb)*

roman_number = ~"Ier|[IVXLCDM]+(èm)?e?"
whitespace = ~"\s+"
pronoun = ~"le"i / ~"du"i

multiplicative_adverb = ( multiplicative_adverb_units_before_decades? multiplicative_adverb_decades ) / multiplicative_adverb_units
multiplicative_adverb_units = ~"semel|bis|ter|quater|(quinqu|sex|sept|oct|no[nv])ies"i
multiplicative_adverb_units_before_decades = ~"un(de?)?|duo(de)?|ter|quater|quin|sex?|sept|octo|novo"i
multiplicative_adverb_decades = ~"(dec|v[ei]c|tr[ei]c|quadrag|quinquag|sexag|septuag|octog|nonag)ies"i
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))

        capture = CaptureVisitor(['roman_number', 'multiplicative_adverb'])
        capture.visit(tree)

        if 'multiplicative_adverb' in capture.captures:
            node['is' + capture.captures['multiplicative_adverb'].title()] = True
        node['order'] = parse_roman_number(capture.captures['roman_number'])
    except parsimonious.exceptions.ParseError as e:
        remove_node(parent, node)
        return j

    i = parse_article_part_reference(tokens, i, node)
    # i = parse_quote(tokens, i, node)

    LOGGER.debug('parse_header1_reference end %s', str(tokens[i:i+10]))

    return i

def parse_article_part_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    # i = alinea_lexer.skip_to_next_word(tokens, i)

    i = parse_one_of(
        [
            parse_alinea_reference,
            parse_sentence_reference,
            parse_word_reference,
            parse_article_reference,
            parse_header1_reference,
            parse_header2_reference,
            parse_header3_reference,
        ],
        tokens,
        i,
        parent
    )

    return i

def parse_quote(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_QUOTE,
        'words': '',
    })

    LOGGER.debug('parse_quote %s', str(tokens[i:i+10]))

    grammar = parsimonious.Grammar("""
rule = whitespaces quoted whitespaces
quoted = "\\"" ~"[^\\n\\\"]+(\\n\\\"[^\\n\\\"]+)*" "\\""

whitespaces = ~"\s*"
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))
        capture = CaptureVisitor(['quoted'])
        capture.visit(tree)
        node['words'] = capture.captures['quoted'].replace('"','') # there could be some quote inside the string in multiline strings
    except parsimonious.exceptions.ParseError as e:
        remove_node(parent, node)
        return i

    LOGGER.debug('parse_quote end %s', str(tokens[i:i+10]))

    return i

# Parse the verb to determine the corresponding action (one of 'add', 'delete', 'edit' or 'replace').
def parse_edit(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_EDIT
    })

    LOGGER.debug('parse_edit %s', str(tokens[i:i+10]))

    # Supprimer {reference}
    if tokens[i] == u'Supprimer':
        i += 2
        node['editType'] = 'delete'
        i = parse_reference(tokens, i, node)
        return i

    r = i
    # i = parse_for_each(parse_reference, tokens, i, node)
    i = parse_reference_list(tokens, i, node)
    # if we did not parse a reference

    i = alinea_lexer.skip_spaces(tokens, i)

    # if we didn't find any reference as a subject and the subject/verb are not reversed
    if len(node['children']) == 0 and tokens[i] != 'Est' and tokens[i] != 'Sont':
        remove_node(parent, node)
        LOGGER.debug('parse_edit none %s', str(tokens[i:i+10]))
        return i
    # i = r

    i = alinea_lexer.skip_tokens(tokens, i, lambda t: t.lower() not in [u'est', u'sont', u'devient'] and not t == u'.')
    if i + 2 >= len(tokens):
        remove_node(parent, node)
        LOGGER.debug('parse_edit eof %s', str(tokens[i:i+10]))
        return r

    # sont supprimés
    # sont supprimées
    # est supprimé
    # est supprimée
    # est abrogé
    # est abrogée
    # sont abrogés
    # sont abrogées
    if i + 2 < len(tokens) and (tokens[i + 2].startswith(u'supprimé') or tokens[i + 2].startswith(u'abrogé')):
        node['editType'] = 'delete'
        i = alinea_lexer.skip_to_end_of_line(tokens, i)
    # est ainsi rédigé
    # est ainsi rédigée
    # est ainsi modifié
    # est ainsi modifiée
    elif i + 4 < len(tokens) and (tokens[i + 4].startswith(u'rédigé') or tokens[i + 4].startswith(u'modifié')):
        node['editType'] = 'edit'
        i = alinea_lexer.skip_to_end_of_line(tokens, i)
        i = alinea_lexer.skip_spaces(tokens, i)
        i = parse_definition(tokens, i, node)
    # est remplacé par
    # est remplacée par
    # sont remplacés par
    # sont remplacées par
    elif i + 2 < len(tokens) and (tokens[i + 2].startswith(u'remplacé')):
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
    elif i + 2 < len(tokens) and (tokens[i + 2].startswith(u'inséré') or tokens[i + 2].startswith(u'ajouté')):
        node['editType'] = 'add'
        i += 4
        i = parse_definition(tokens, i, node)
        i = alinea_lexer.skip_to_end_of_line(tokens, i)
    # est ainsi rétabli
    elif i + 4 < len(tokens) and tokens[i + 4].startswith(u'rétabli'):
        node['editType'] = 'add'
        i = alinea_lexer.skip_to_end_of_line(tokens, i)
        i = alinea_lexer.skip_spaces(tokens, i)
        i = parse_definition(tokens, i, node)
    # est complété par
    elif i + 2 < len(tokens) and tokens[i + 2] == u'complété':
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
    # est ratifié:
    elif i + 2 < len(tokens) and (tokens[i].lower() == u'est' and tokens[i + 2] == u'ratifié'):
        node['editType']= 'ratified'
        i += 4
    else:
        i = r
        LOGGER.debug('parse_edit remove %s', str(tokens[i:i+10]))
        remove_node(parent, node)
        i = parse_raw_article_content(tokens, i, parent)
        i = alinea_lexer.skip_to_end_of_line(tokens, i)
        return i

    # We've parsed pretty much everything we could handle. At this point,
    # there should be no meaningful content. But their might be trailing
    # spaces or ponctuation (often "." or ";"), so we skip to the end of
    # the line.
    i = alinea_lexer.skip_to_end_of_line(tokens, i)

    LOGGER.debug('parse_edit end %s', str(tokens[i:i+10]))

    return i

def parse_raw_article_content(tokens, i, parent):
    node = create_node(parent, {
        'type': 'raw-content',
        'content': ''
    })

    LOGGER.debug('parse_raw_article_content %s', str(tokens[i:i+10]))

    while i < len(tokens) and tokens[i] != alinea_lexer.TOKEN_NEW_LINE:
        node['content'] += tokens[i]
        i += 1

    if node['content'] == '' or is_space(node['content']):
        remove_node(parent, node)

    LOGGER.debug('parse_raw_article_content end %s', str(tokens[i:i+10]))

    return i

# Parse a reference to a specific or aforementioned code.
# References to a specific code are specified by using the exact name of that code (cf parse_code_name).
# References to an aforementioned code will be in the form of "le même code".
def parse_code_reference(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_CODE_REFERENCE,
    })

    LOGGER.debug('parse_code_reference %s', str(tokens[i:i+10]))

    grammar = parsimonious.Grammar("""
code_ref = named_code_ref / back_reference_code_ref
named_code_ref = whitespace* (pronoun whitespace)* code whitespace*
code = ( ~"code"i whitespace+ code_name ) / ~"constitution"i
back_reference_code_ref = whitespace* (pronoun whitespace)* "même" whitespace+ "code" whitespace*
code_name = ~"de +la +consommation +des +boissons +et +des +mesures +contre +l['’] *alcoolisme +applicable +dans +la +collectivité +territoriale +de +Mayotte|du +domaine +de +l['’] *Etat +et +des +collectivités +publiques +applicable +à +la +collectivité +territoriale +de +Mayotte|des +pensions +de +retraite +des +marins +français +du +commerce, +de +pêche +ou +de +plaisance|des +pensions +militaires +d['’] *invalidité +et +des +victimes +de +la +guerre|des +tribunaux +administratifs +et +des +cours +administratives +d['’] *appel|des +pensions +militaires +d['’] *invalidité +et +des +victimes +de +guerre|de +déontologie +des +professionnels +de +l['’] *expertise +comptable|de +déontologie +de +la +profession +de +commissaire +aux +comptes|de +l['’] *entrée +et +du +séjour +des +étrangers +et +du +droit +d['’] *asile|des +débits +de +boissons +et +des +mesures +contre +l['’] *alcoolisme|du +domaine +public +fluvial +et +de +la +navigation +intérieure|de +la +Légion +d['’] *honneur +et +de +la +médaille +militaire|des +relations +entre +le +public +et +l['’] *administration|de +l['’] *expropriation +pour +cause +d['’] *utilité +publique|général +de +la +propriété +des +personnes +publiques|des +postes +et +des +communications +électroniques|des +pensions +civiles +et +militaires +de +retraite|de +l['’] *Office +national +interprofessionnel +du +blé|de +déontologie +des +agents +de +police +municipale|disciplinaire +et +pénal +de +la +marine +marchande|des +instruments +monétaires +et +des +médailles|de +déontologie +des +chirurgiens-dentistes|général +des +collectivités +territoriales|de +la +construction +et +de +l['’] *habitation|de +déontologie +de +la +police +nationale|des +communes +de +la +Nouvelle-Calédonie|général +des +impôts, +annexe +2, +CGIAN2|général +des +impôts, +annexe +3, +CGIAN3|général +des +impôts, +annexe +4, +CGIAN4|général +des +impôts +annexe +1, +CGIAN1|de +l['’] *action +sociale +et +des +familles|des +procédures +civiles +d['’] *exécution|de +la +famille +et +de +l['’] *aide +sociale|de +l['’] *industrie +cinématographique|du +travail +applicable +à +Mayotte|de +déontologie +des +sages-femmes|de +déontologie +des +architectes|de +la +propriété +intellectuelle|du +cinéma +et +de +l['’] *image +animée|rural +et +de +la +pêche +maritime|de +l['’] *organisation +judiciaire|des +juridictions +financières|de +déontologie +des +médecins|de +l['’] *enseignement +technique|de +la +nationalité +française|de +déontologie +vétérinaire|de +justice +administrative|de +la +sécurité +intérieure|de +déontologie +médicale|général +des +impôts(, +CGI)?|de +la +sécurité +sociale|monétaire +et +financier|des +caisses +d['’] *épargne|de +la +voirie +routière|de +l['’] *aviation +civile|de +justice +militaire|de +la +santé +publique|du +domaine +de +l['’] *Etat|des +marchés +publics( +\(édition +(1964|2001|2004|2006)\))?|de +procédure +civile( +\(1807\))?|de +procédure +pénale|du +travail +maritime|du +service +national|des +ports +maritimes|de +l['’] *environnement|de +la +consommation|de +la +mutualité|de +la +recherche|de +l['’] *artisanat|de +l['’] *éducation|de +l['’] *urbanisme|des +assurances|des +transports|du +patrimoine|de +la +défense|des +communes|de +l['’] *énergie|des +douanes( +de +Mayotte)?|de +commerce|de +la +route|du +tourisme|du +travail|forestier( +de +Mayotte)?|électoral|du +sport|du +blé|du +vin|minier|pénal|rural|civil"i

whitespace = ~"\s+"
pronoun = ~"le"i / ~"la"i / ~"du"i / ~"de +la"i
    """)

    try:
        tree = grammar.match(''.join(tokens[i:]))
        i += len(alinea_lexer.tokenize(tree.text))

        capture = CaptureVisitor(['code', 'back_reference_code_ref'])
        capture.visit(tree)

        if 'back_reference_code_ref' in capture.captures:
            node = mark_as_lookback_reference(node)
        else:
            node['id'] = capture.captures['code'].lower()

        i = parse_reference(tokens, i, node)
    except parsimonious.exceptions.ParseError as e:
        remove_node(parent, node)
        return i

    LOGGER.debug('parse_code_reference end %s', str(tokens[i:i+10]))

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
        def_nodes = filter_nodes(parent, lambda x: duralex.tree.is_definition(x))
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

    LOGGER.debug('parse_reference_list %s', str(tokens[i:i+10]))    

    i = parse_reference(tokens, i, parent)
    i = alinea_lexer.skip_spaces(tokens, i)
    if ((i + 2 < len(tokens) and tokens[i] == u',' and tokens[i + 2] in [u'à', u'au', u'l'])
        or (i + 2 < len(tokens) and tokens[i] == u'et')):
        i = parse_reference_list(tokens, i + 2, parent)
    i = alinea_lexer.skip_spaces(tokens, i)

    LOGGER.debug('parse_reference_list end %s', str(tokens[i:i+10]))    

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

    # node = create_node(parent, {'type':'reference'})
    node = parent

    j = i
    i = parse_one_of(
        [
            parse_law_reference,
            parse_code_reference,
            parse_code_part_reference,
            parse_section_reference,
            parse_subsection_reference,
            parse_chapter_reference,
            parse_title_reference,
            parse_book_reference,
            parse_article_reference,
            parse_article_part_reference,
            parse_paragraph_reference,
            parse_lookback_reference,
            parse_incomplete_reference,
            parse_alinea_reference,
            parse_word_reference,
            parse_bill_article_reference,
        ],
        tokens,
        i,
        node
    )

    # if len(node['children']) == 0:
    #     remove_node(parent, node)
    #     return j

    return i

# {romanNumber}.
# u'ex': I., II.
def parse_header1(tokens, i, parent):
    if i >= len(tokens):
        return i

    i = alinea_lexer.skip_spaces(tokens, i)

    node = create_node(parent, {
        'type': TYPE_HEADER1,
    })

    LOGGER.debug('parse_header1 %s', str(tokens[i:i+10]))

    # skip '{romanNumber}.'
    if is_roman_number(tokens[i]) and tokens[i + 1] == u'.':
        LOGGER.debug('parse_header1 found article header-1 %s', str(tokens[i:i+10]))
        node['order'] = parse_roman_number(tokens[i])
        i = alinea_lexer.skip_to_next_word(tokens, i + 2)
    else:
        remove_node(parent, node)
        node = parent

    j = i
    i = parse_edit(tokens, i, node)
    i = parse_for_each(parse_header2, tokens, i, node)
    if len(node['children']) == 0:
        i = parse_raw_article_content(tokens, i, node)
        i = parse_for_each(parse_header2, tokens, i, node)

    if len(node['children']) == 0 and parent != node:
        remove_node(parent, node)

    LOGGER.debug('parse_header1 end %s', str(tokens[i:i+10]))

    return i

# {number}°
# u'ex': 1°, 2°
def parse_header2(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_HEADER2,
    })

    LOGGER.debug('parse_header2 %s', str(tokens[i:i+10]))

    i = alinea_lexer.skip_spaces(tokens, i)
    if i < len(tokens) and re.compile(u'\d+°').match(tokens[i]):
        LOGGER.debug('parse_header2 found article header-2 %s', str(tokens[i:i+10]))

        node['order'] = parse_int(tokens[i])
        # skip {number}°
        i += 2
        i = alinea_lexer.skip_to_next_word(tokens, i)
    else:
        remove_node(parent, node)
        node = parent

    j = i
    i = parse_edit(tokens, i, node)
    i = parse_for_each(parse_header3, tokens, i, node)
    if len(node['children']) == 0 and 'order' in node:
        i = parse_raw_article_content(tokens, i, node)
        i = parse_for_each(parse_header3, tokens, i, node)

    if node != parent and len(node['children']) == 0:
        remove_node(parent, node)

    LOGGER.debug('parse_header2 end %s', str(tokens[i:i+10]))

    return i

# {number})
# u'ex': a), b), a (nouveau))
def parse_header3(tokens, i, parent):
    if i >= len(tokens):
        return i

    node = create_node(parent, {
        'type': TYPE_HEADER3,
    })

    LOGGER.debug('parse_header3 %s', str(tokens[i:i+10]))

    i = alinea_lexer.skip_spaces(tokens, i)
    if i >= len(tokens):
        remove_node(parent, node)
        return i

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

    j = i
    i = parse_edit(tokens, i, node)
    if len(node['children']) == 0 and 'order' in node:
        i = parse_raw_article_content(tokens, i, node)

    if node != parent and len(node['children']) == 0:
        remove_node(parent, node)

    LOGGER.debug('parse_header3 end %s', str(tokens[i:i+10]))

    return i

def mark_as_lookback_reference(node):
    ref = create_node(node['parent'], {
        'type': TYPE_LOOKBACK_REFERENCE,
    })
    push_node(ref, node)
    return ref

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

def parse_bill_articles(data, parent):
    if 'articles' in data:
        for article_data in data['articles']:
            parse_bill_article(article_data, parent)
    elif 'alineas' in data:
        parse_bill_article(data, parent)

    return data

def parse_bill_article(data, parent):
    node = create_node(parent, {
        'type': TYPE_BILL_ARTICLE,
        'order': 1,
        'isNew': False
    })

    node['order'] = data['order']

    if 'alineas' in data:
        parse_json_alineas(data['alineas'], node)

def parse_json_alineas(data, parent):
    text = alinea_lexer.TOKEN_NEW_LINE.join(value for key, value in list(iter(sorted(data.items()))))
    parent['content'] = text#.decode('utf-8')
    return parse_alineas(text, parent)

def parse_alineas(data, parent):
    tokens = alinea_lexer.tokenize(data.strip())
    parse_for_each(parse_header1, tokens, 0, parent)

    if len(parent['children']) == 0:
        parse_raw_article_content(tokens, 0, parent)

def parse(data, tree):
    # tree = create_node(tree, {'type': 'articles'})
    parse_bill_articles(data, tree)
    return tree


class CaptureVisitor(parsimonious.NodeVisitor):

    def __init__( self, table ):

        self.table = table
        self.captures = {}

    def generic_visit( self, node, visited_children ):

        if node.expr_name in self.table:

            rule_name = node.expr_name
            self.captures[rule_name] = node.text


class ToSemanticTreeVisitor(parsimonious.NodeVisitor):

    def __init__( self, table, parent ):

        self.table = table
        self.parent = parent
        self.node = None

    def generic_visit( self, node, visited_children ):

        if node.expr_name in self.table:

            rule_name = node.expr_name
            rule = self.table[rule_name]
            node_type = rule['type']
            self.node = create_node(self.parent, {
                'type': node_type,
                'children': [],
            })
            text = node.text
            if 'replace' in rule:
                for r in rule['replace']:
                    text = text.replace(r[0], r[1])
            if 'property' in rule:
                self.node[rule['property']] = text
            if 'dynamic' in rule and rule['dynamic'] == 'childrify':
                self.parent = self.node

# vim: set ts=4 sw=4 sts=4 et:
