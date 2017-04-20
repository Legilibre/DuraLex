# -*- coding: utf-8 -*-

from AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *
from duralex.AddCommitMessageVisitor import int_to_roman
import duralex.node_type
import duralex.diff

from bs4 import BeautifulSoup

import os
import subprocess
import tempfile

class CreateGitBookVisitor(AbstractVisitor):
    def __init__(self, args):
        self.directory = args.gitbook
        super(CreateGitBookVisitor, self).__init__()

    def write_file(self, filename, data):
        f = open(self.directory + '/' + filename, 'w')
        f.write(data.encode('utf-8'))
        f.close()

    def visit_node(self, node):
        if 'type' in node and node['type'] == 'article':
            title = 'Article ' + str(node['order'])
            filename = title.replace(' ', '_')
            body = [
                '# ' + self.icon('bookmark-o') + ' ' + get_root(node)['type'].title() + ', ' + title,
                '## ' + self.icon('file-text-o') + ' Texte',
                node['content'].replace('\n', '\n\n'),
                '## ' + self.icon('pencil-square-o') + ' Suivi des modifications'
            ]

            if 'githubIssue' in node:
                body.append(u'[' + self.icon('code-fork') + u' Voir dans le système de gestion de versions (expert)](' + node['githubIssue'] + ')')

            edits = filter_nodes(node, lambda n: 'type' in n and n['type'] == 'edit')
            for edit in edits:
                ancestors = get_node_ancestors(edit)
                messages = []
                link = ''
                for ancestor in ancestors:
                    if 'type' not in ancestor:
                        continue;

                    if ancestor['type'] == 'article':
                        messages.append('Article ' + str(ancestor['order']))
                        if 'githubIssue' in node:
                            link = ancestor['githubIssue']
                    if ancestor['type'] == 'bill-header1' and 'implicit' not in ancestor:
                        messages.append(int_to_roman(ancestor['order']))
                    if ancestor['type'] == 'bill-header2':
                        messages.append(unicode(ancestor['order']) + u'°')
                body.append('### ' + ', '.join(messages[::-1]))
                if 'commitMessage' in edit:
                    edit_desc = edit['commitMessage'].splitlines()[0]
                    # remove the " ({reference list})" from the commit message since its already printed
                    # in the header above
                    edit_desc = re.sub(r' \(.*\)', '', edit_desc)
                    body.append(edit_desc)
                if 'htmlDiff' in edit:
                    soup = BeautifulSoup(edit['htmlDiff'], "html5lib")
                    filename_div = soup.find('div', {'class': 'diff-filename'})
                    article_ref = filter_nodes(edit, lambda n: n['type'] == 'article-reference')[0]
                    target_title, target_href = self.get_deep_link(self.get_edit_target_nodes(article_ref))
                    a_tag = soup.new_tag('a', href=target_href)
                    a_tag.string = target_title
                    filename_div.string = ''
                    filename_div.append(a_tag)
                    body.append(unicode(soup.body.div))
                elif 'diff' in edit:
                    process = subprocess.Popen(
                        'diff2html -i stdin -d word -o stdout --su hidden -s line',
                        shell=True,
                        stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    out, err = process.communicate(input=edit['diff'].encode('utf-8') + '\n')
                    soup = BeautifulSoup(out, "html5lib")
                    body.append(str(list(soup.find_all('style'))[0]))
                    body.append(unicode(soup.find('div', {'id': 'diff'})))

            self.write_file(title.replace(' ', '_') + '.md', '\n\n'.join(body))

        if 'parent' not in node:
            process = subprocess.Popen(
                'gitbook init ' + self.directory,
                shell=True,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            out, err = process.communicate()

            summary = '# Summary\n\n'
            summary += '## ' + node['type'].title() + '\n\n'
            readme = '# ' + self.get_book_title(node) + '\n\n'
            if 'url' in node and node['url']:
                readme += '[Texte original](' + node['url'] + ')\n\n'
            readme += '## ' + self.icon('bookmark-o') + ' Articles\n\n'

            articles = filter_nodes(node, lambda n: 'type' in n and n['type'] == 'article')
            for article in articles:
                title = 'Article ' + str(article['order'])
                filename = title.replace(' ', '_')
                summary += '* [' + title + '](' + filename + '.md)\n'
                readme += '* [' + title + '](' + filename + '.md)\n'
            summary += '\n'
            readme += '\n'

            modified = ''
            modified += u'## ' + self.icon('file-text-o') + u' Textes modifiés\n\n'
            edits = self.build_edit_matrix(node)
            law_ids = set([i[0] for i in edits.keys()])
            for law_id in law_ids:
                law_edits = {k: v for k, v in edits.iteritems() if k[0] == law_id}
                modified_files = []
                for k, v in edits.iteritems():
                    filename = law_id + '-' + k[1] + '.md'
                    modified_files.append((k[1], u' * [Article ' + k[1] + '](' + filename + ')'))
                    self.write_file(
                        filename,
                        self.get_modified_file_page(k[2], u'Loi n°' + law_id + u', Article ' + k[1], v)
                    )
                modified_files = [m[1] for m in sorted(modified_files, key=lambda x: x[0].replace('-', ' '))]
                modified_law = '\n'.join(modified_files)
                self.write_file(
                    law_id + '.md',
                    '# ' + self.icon('balance-scale') + u' Loi N°' + law_id + u'\n\n'
                    + '## ' + self.icon('pencil-square-o') + u' Articles modifiés\n\n'
                    + modified_law
                )
                modified += u'* [Loi n°' + law_id + '](' + law_id + '.md)\n' + modified_law
            readme += modified
            summary += modified

            if 'cocoricoVote' in node:
                readme += u'\n## ' + self.icon('envelope-o') + ' Vote\n\n'
                readme += u'* [Voter](https://cocorico.cc)\n'
                readme += u'* [Résultats du vote](https://cocorico.cc)\n'
                summary += u'\n## Vote\n\n'
                summary += u'* [Voter](https://cocorico.cc)\n'
                summary += u'* [Résultats du vote](https://cocorico.cc)\n'

        super(CreateGitBookVisitor, self).visit_node(node)

        if 'parent' not in node:
            self.write_file('book.json', '{"language":"fr", "plugins": ["heading-anchors"], "title": "' + self.get_book_title(node) + '"}')
            self.css()
            self.write_file('SUMMARY.md', summary)
            self.write_file('README.md', readme)

            process = subprocess.Popen(
                'gitbook install && gitbook build ' + self.directory,
                shell=True,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            out, err = process.communicate()

    def get_book_title(self, root_node):
        title = root_node['type'].title()
        if 'id' in root_node:
            title += u' N°' + str(root_node['id'])
        if 'legislature' in root_node:
            title += ', ' + str(root_node['legislature']) + u'ème législature'
        return title

    def get_modified_file_page(self, filename, title, edit_sources):
        body = [
            '# ' + self.icon('balance-scale') + ' ' + title,
        ]

        f = open(filename, 'r')
        text = f.read().decode('utf-8')
        original_text = text
        f.close()

        # all diffs are supposed to be applied in sequence
        modif_links = []
        for edit_source in edit_sources:
            title, href = self.get_deep_link(edit_source)
            modif_links.append('* [' + title + '](' + href + ')')
            edit_refs = filter_nodes(edit_source[-1], lambda n: n['type'] == 'edit')
            for edit_ref in edit_refs:
                text = self.patch(text, edit_ref['diff'])

        body.append('## ' + self.icon('file-text-o') + ' Texte')
        body.append(duralex.diff.make_html_rich_diff(original_text, text))

        body.append('## ' + self.icon('pencil-square-o') + ' Suivi des modifications')
        body += modif_links

        return '\n\n'.join(body)

    def icon(self, name):
        return '<i class="fa fa-' + name + '"></i>'

    def patch(self, original, unified_diff):
        fd, filename = input_file = tempfile.mkstemp()
        os.write(fd, original.encode('utf-8'))
        process = subprocess.Popen(
            'patch -p0 --output=- ' + filename,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = process.communicate(input=unified_diff.encode('utf-8') + '\n')
        return ''.join(out).decode('utf-8')

    def get_deep_link(self, nodes):
        href = []
        title = []
        for node in nodes:
            if node['type'] == 'law-reference':
                title.append(u'Loi n°' + node['lawId'])
                href.append(node['lawId'])
            elif node['type'] == 'article':
                title.append(u'Article ' + str(node['order']))
                href.append(u'Article_' + str(node['order']) + '.md#article-' + str(node['order']))
            elif node['type'] == 'article-reference':
                title.append(u'Article ' + node['id'])
                href.append(node['id'] + '.md')
            elif node['type'] == 'bill-header1' and 'implicit' not in node:
                title.append(int_to_roman(node['order']))
                href.append(int_to_roman(node['order']))
            elif node['type'] == 'bill-header2':
                title.append(unicode(node['order']) + u'°')
                href.append(str(node['order']) + u'°')
        return (', '.join(title), '-'.join(href))

    def get_edit_target_nodes(self, node):
        nodes = []

        if node_type.is_reference(node):
            nodes.append(node)

        nodes += filter(
            lambda n: node_type.is_reference(n),
            get_node_ancestors(node)
        )

        return sorted(
            nodes,
            key=lambda n: node_type.REFERENCE.index(n['type'])
        )

    def get_edit_source_nodes(self, node):
        edit_source_types = [
            'article',
            'bill-header1',
            'bill-header2'
        ]

        return sorted(
            filter(
                lambda n: 'type' in n and n['type'] in edit_source_types,
                get_node_ancestors(node)
            ),
            key=lambda n: edit_source_types.index(n['type'])
        )

    def build_edit_matrix(self, node):
        edits = {}

        article_refs = filter_nodes(node, lambda n: 'type' in n and n['type'] == 'article-reference')
        for article_ref in article_refs:
            law_ref = filter(
                lambda n: 'type' in n and n['type'] == 'law-reference',
                get_node_ancestors(article_ref)
            )[0]
            t = (law_ref['lawId'], article_ref['id'], article_ref['filename'])
            if t not in edits:
                edits[t] = []
            edits[t].append(self.get_edit_source_nodes(article_ref))

        return edits

    def css(self):
        if not os.path.exists(self.directory + '/styles'):
            os.makedirs(self.directory + '/styles')
        self.write_file(
            'styles/website.css',
            ('.gitbook-link, .divider {display:none!important}'
            '.diff .diff-delete {color:#a33;text-decoration:line-through;background:#ffeaea}'
            '.diff .diff-insert {background:#eaffea;}'
            '.diff {border:1px solid rgba(0,0,0,.15);margin-bottom:20px;border-radius:3px}'
            '.diff .diff-content {padding:10px;background:#fcfcfc}'
            '.diff .diff-filename {background:#f6f6f6;padding:10px;border-bottom:1px solid rgba(0,0,0,.15)}'
            '.diff .diff-filename:before {font:normal normal normal 14px/1 FontAwesome;content:"\\f0f6";padding-right:10px}')
        )
