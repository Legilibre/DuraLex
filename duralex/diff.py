import difflib

def make_html_rich_diff(a, b, filename = None):
    html = ['<div class="diff">']
    if filename:
        html.append('<div class="diff-filename">' + filename + '</div>')

    a = a.splitlines() if a != '' else []
    b = b.splitlines() if b != '' else []

    html.append('<div class="diff-content">')
    for i in range(0, max(len(a), len(b))):
        line_a = a[i] if i < len(a) else ''
        line_b = b[i] if i < len(b) else ''
        s = difflib.SequenceMatcher(a=line_a, b=line_b)
        ops = s.get_opcodes()
        changed = False
        for op in ops:
            if op[0] == 'equal':
                html.append('<span>' + line_a[op[1]:op[2]] + '<span>')
            elif op[0] == 'delete':
                html.append(
                    '<span class="diff-delete">'
                    + line_a[op[1]:op[2]] + line_b[op[3]:op[4]]
                    + '</span>'
                )
                changed = True
            elif op[0] == 'insert':
                html.append(
                    '<span class="diff-insert">'
                    + line_a[op[1]:op[2]] + line_b[op[3]:op[4]]
                    + '</span>'
                )
                changed = True
            elif op[0] == 'replace':
                html.append(
                    '<span class="diff-delete">'
                    + line_a[op[1]:op[2]]
                    + '</span>'
                )
                html.append(
                    '<span class="diff-insert">'
                    + line_b[op[3]:op[4]]
                    + '</span>'
                )
                changed = True
            # html.append(tag + content + '</span>')
        html.append('<br/>')
    html.append('</div></div>')
    return ''.join(html)#.encode('utf-8')
