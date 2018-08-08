DuraLex tree
============

A DuraLex tree is a computer-readable representation of an amendment. It is a tree where each node generally has a type (a label defining its nature), zero or more children, and possibly some properties.

A node can be either (depending on its type):

* a container of other nodes: in this case it acts as a hierarchical representation of the original amendment or modifying text, it can be for instance a bill, a bill proposal, an article of the bill proposal, a header (with level 1, 2, or 3), or an amendment;
* a action/verb: there is a single verb "edit" with sub-verbs in the property editType: "edit" (no specific action), "replace", "delete", "add"; depending on the action, there are references (almost mandatory) and/or definitions (see below);
* a reference: the place where is located the action, for instance an in-force law, an article, an alinea, a sentence, a word; the reference is the smallest unit location a place but almost mandatorily references are hierarchicaly grouped, for instance "in that law, in that article, in that alinea";
* a definition: the new content, which can be an entire article, or just an alinea or a single word; these nodes generally have a single child of type quote containing the effective content.

A DuraLex trees is internally represented as a set of dictionaries (=nodes), each with properties:

* "type" of type string (not mandatory),
* "children" of type list containing the child nodes,
* "parent" of type node,
* "uuid" of type string, which is a unique identifier to compare nodes and for easier debugging.

A DuraLex tree can be exported into JSON, and in this case "parent" properties must be removed to avoid circular references between parent and child, and "uuid" properties can also be removed because there are probably no more useful.

The standard functions in duralex.tree can care of managing parent-child relations and uuid properties. Note that uuid appear when nodes are copied.

Example
-------

Take the following fictional article of a bill proposal (equivalent in French and English):

Article 5
  Après le mot "huitième" du troisième alinéa de l’article 5 de la loi 58-592 est ajouté le mot "ou neuvième".
  After the word "eighth" of the third alinea of the article 5 of the law 58-592 is added the word "or nineth".

Its DuraLex tree is:
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
                  "children": [
                    {
                      "children": [
                        {
                          "type": "quote",
                          "words": "huitième"
                        }
                      ],
                      "type": "word-reference",
                      "position": "after"
                    }
                  ],
                  "type": "alinea-reference",
                  "order": 3
                }
              ],
              "type": "article-reference",
              "id": "5"
            }
          ],
          "type": "law-reference",
          "id": "58-592"
        },
        {
          "children": [
            {
              "type": "quote",
              "content": "ou neuvième"
            }
          ],
          "type": "word-definition"
        }
      ],
      "type": "edit",
      "editType": "add"
    }
  ],
  "type": "bill-article",
  "id": "5"
}
```

Note that, similarly to the original amendment, a DuraLex tree is agnostic of the modified text: computationally, you can apply the described action on every text, although it could result in no modification if the context (the set of references) does not match. If the modified text changed compared to the version on which was initially computed the amendment, it could result either no modification or an unwanted modification, but this is a legal issue unrelated to the computational problematic.

From a computational point of view, the amendment – or equivalently the DuraLex tree – is a generalised diff, in the sense it can be applied on more texts than a classical diff. Even if it can be sucessfully applied on more texts, and particularly when texts are slightly modified compared to the text on which was initially computed the amendment, the more the text change, the more the result could be an unwanted resulting text.

Parsing
-------

The parsing operation of an amendment has three major steps:

1. parsing itself of the amendment’s text: this is modelised by a grammar (PEG grammar with library Parsimonious) or previously by a dedicated lexer-parser,
2. creation of the DuraLex nodes: this is done by a Parsimonious visitor abstracting some syntactic Parsimonious rules as semantic DuraLex nodes or previously dedicated creation of nodes,
3. manipulation of the DuraLex tree by visitors: the visitors tidy the tree (e.g. reorder the references in their canonical order), or resolve some semi-explicit information (e.g. lookback references or introductory sentences which applies to the rest of the paragraph), or any other operation on the semantic DuraLex tree.

The details of the visitors are explained in a separate document.

Constraints
-----------

Although there are currently no explicit constraints on DuraLex trees, we can observe the following facts on some Duralex runs and these are probably quite sensible constraints:

* quote-type nodes never have children, it is always a leaf,
* reference-type nodes have either reference-type or quote-type nodes as recursive children,
* definition-type nodes have either definition-type or quote-type nodes as recursive children,
* edit-type nodes have only reference-type or definition-type nodes as direct children.
