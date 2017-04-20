# -*- coding: utf-8 -*-

from AbstractVisitor import AbstractVisitor

from duralex.alinea_parser import *

from github import Github

class AddGitHubIssueVisitor(AbstractVisitor):
    def __init__(self, args):
        self.github = Github(args.github_token)
        self.repo = self.github.get_repo(args.github_repository)
        self.issues = list(self.repo.get_issues())
        self.current_issue = -1

        super(AddGitHubIssueVisitor, self).__init__()

    def visit_edit_node(self, node, post):
        if post:
            return

        if 'commitMessage' not in node:
            node['commitMessage'] = '(#' + str(self.current_issue) + ')'
        else:
            node['commitMessage'] = node['commitMessage'] + '\nGitHub: #' + str(self.current_issue)


    def visit_node(self, node):
        if 'type' in node and node['type'] == 'article':
            title = 'Article ' + str(node['order'])
            body = node['content']
            found = False
            for issue in self.issues:
                if issue.title == title:
                    found = True
                    node['githubIssue'] = issue.html_url
                    self.current_issue = issue.number
                    if issue.body != body:
                        issue.edit(title=title, body=body)
            if not found:
                issue = self.repo.create_issue(title=title, body=body)
                self.current_issue = issue.number

        super(AddGitHubIssueVisitor, self).visit_node(node)
