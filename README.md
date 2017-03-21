# DuraLex

[![Build Status](http://img.shields.io/travis/promethe42/duralex.svg)](https://travis-ci.org/promethe42/duralex)

DuraLex is a extensible French bill parsing and automating framework.
It turns bills written in plain natural French into an intermediary tree representation that can be automatically processed.

The main use case is the evaluation of the edits described by the bill to automagically apply them to the existing law texts.

## Intermediary representation

### Principle

DuraLex turns plain text into a standardized JSON tree structure intermediary representation.
This standardized intermediary representation can then be used as an input for other (third party) tools.

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

## Generating patch files

By default, the intermediary representation will not compute/feature the diff of each edit.
You must add the `--diff` switch to the command line:

```bash
./bin/duralex --diff articles.json
```

Then, using [jq](https://stedolan.github.io/jq/), it is easy to extract only the `diff` fields to get a complete unified diff that can be used as a patch:

```bash
./bin/duralex --diff articles.json | jq -r '.. | .diff? | strings' > articles.patch
```

The patch can then be applied by calling:

```bash
patch -p0 < articles.patch
```

You can even use a pipe to patch files directly:

```bash
./bin/duralex --diff articles.json | jq -r '.. | .diff? | strings' | patch -p0
```

## Installation

```bash
pip install -r requirements.txt
```

## Tests

```bash
cd tests
python main.py
```

## Related projects

* https://github.com/Legilibre/NuitCodeCitoyen
* https://github.com/Legilibre/Archeo-Lex
