# DuraLex

[![Build Status](https://img.shields.io/travis/Legilibre/duralex.svg)](https://travis-ci.org/Legilibre/duralex)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/Legilibre/duralex)

DuraLex is a French bill compiler. It takes an official bill document written in plain natural French and transforms
it into an automatable semantic data structure. This data structure describes the content of the bill, including but
not limited to:

* the id and type of the bill
* articles and sections/headers
* each edit with the corresponding operators (add, remove, replace...) and operands (words, articles...)
* references to existing laws, codes, articles, headers...
* definition of new articles, headers...

DuraLex is the backend for [SedLex](https://github.com/Legilibre/SedLex).

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
usage: duralex [-h] [--file FILE] [--url URL] [--quiet] [--diff] [--uuid]
               [--commit-message] [--git-commit] [--github-token GITHUB_TOKEN]
               [--github-repository GITHUB_REPOSITORY]

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           the path of the bill to process
  --url URL             the URL of the bill to process
  --quiet               no stdout output
  --diff                compute a diff for each edit
  --uuid                add a unique ID on each node
  --commit-message      generate a commit message for each edit
  --git-commit          git commit each edit
  --github-token GITHUB_TOKEN
                        the GitHub API token
  --github-repository GITHUB_REPOSITORY
                        the target GitHub repository
```

Examples:

```bash
./duralex --file pion1561.html
```
```bash
./duralex --url http://www.assemblee-nationale.fr/14/propositions/pion1561.asp
```
```bash
curl -s http://www.assemblee-nationale.fr/14/propositions/pion1561.asp | ./duralex
```
```bash
cat http://www.assemblee-nationale.fr/14/propositions/pion1561.asp | ./duralex
```

## Intermediary representation

### Principle

DuraLex turns plain text into a standardized JSON tree structure intermediary representation.
This standardized intermediary representation can then be used as an input for other (third party) tools.

![article to json](article_to_json.jpg)

### Example

The following bill article:

```
L'article 11 de la loi n° 78-753 du 17 juillet 1978 portant diverses mesures d'amélioration des relations entre l'administration et le public et diverses dispositions d'ordre administratif, social et fiscal est abrogé.
```

will give the following intermediary representation:

```json
{
  "children": [
    {
      "children": [
        {
          "children": [
            {
              "children": [
                {
                  "id": "11",
                  "type": "article-reference"
                }
              ],
              "lawDate": "1978-7-17",
              "lawId": "78-753",
              "type": "law-reference"
            }
          ],
          "editType": "delete",
          "type": "edit"
        }
      ],
      "isNew": false,
      "order": 1,
      "type": "article"
    }
  ]
}
```

## Tests

```bash
cd tests
python main.py
```

## Related projects

* https://github.com/Legilibre/NuitCodeCitoyen
* https://github.com/Legilibre/Archeo-Lex
* https://github.com/regardscitoyens/the-law-factory-parser
