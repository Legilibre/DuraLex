DEFINITION = [
    'article',
    'header1',
    'header2',
    'header3',
    'alinea',
    'sentence',
    'words'
]

REFERENCE = [
    'code-reference',
    'code-part-reference',
    'book-reference',
    'law-reference',
    'title-reference',
    'chapter-reference',
    'section-reference',
    'subsection-reference',
    'paragraph-reference',
    'article-reference',
    'header1-reference',
    'header2-reference',
    'header3-reference',
    'alinea-reference',
    'sentence-reference',
    'words-reference',
    'incomplete-reference'
]

def is_definition(node):
    return 'type' in node and node['type'] in DEFINITION

def is_reference(node):
    return 'type' in node and node['type'] in REFERENCE
