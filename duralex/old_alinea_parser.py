# -*- coding: utf-8 -*-

#
# Old unitary grammars now merged/unified into a bigger grammar
#

def parse_article_definition(tokens, i, parent):
    # Transfered to parse_definition
    if i >= len(tokens):
        return i
    LOGGER.debug('parse_article_definition %s', str(tokens[i:i+10]))

    grammar = parsimonious.Grammar("""
rule = whitespaces article_def whitespaces

article_def = ( ~"un +"i / ~"l['’] *"i ) ~"article"i (_ article_id (_ so_that_written not_a_quote quoted)?)?

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
        toSemanticTree.attach(parent, tree)
    except parsimonious.exceptions.ParseError:
        LOGGER.debug('parse_article_definition none %s', str(tokens[i:i+10]))
        return i

    LOGGER.debug('parse_article_definition end %s', str(tokens[i:i+10]))

    return i

