Here are details about how the grammar is written.


Multiple grammars
=================

Historically DuraLex was written as raw Python, with multiple Python functions, each one calling other ones. Hence the transitions between functions were encoded generally at the end of each function, but sometimes in the middle of the function.

Since June 2018, DuraLex is rewritten in the PEG (Parsing Expression Grammar) library Parsimonious. To keep continuity and a smooth transition between legacy functions and PEG-powered functions, it was decided to keep the general structure of Python functions, but convert the inner parsing into PEG (when possible). As of now (December 2018), DuraLex is half-raw-Python and half-PEG, or PEG-by-part.

The conversion from PEG trees, which are low-level parse trees, and DuraLex trees, which are high-level semantic trees is achieved through two Parsimonious visitors:
* `CaptureVisitor`, a very simple visitor capturing some Parsimonious named rules and storing them in a table, multiple occurences are not managed;
* `ToSemanticTreeVisitor`, a more powerful visitor capturing some Parsimonious named rules and creating a local DuraLex tree according to a table describing how to fashion the DuraLex tree.

`ToSemanticTreeVisitor` requires a mapping table between Parsimonious nodes and DuraLex nodes; this mapping table takes the Parsimonious rule name as key and a dictionary describing the DuraLex behaviour. It can create new DuraLex nodes when the `type` is given, assign new properties with `property`, `value`, and `replace`, and either create sibling lists (by default) when there are multiple children either create in-depth lists when `_priority` is true (this second behaviour is not well-tested as of December 2018).

The next major movement is to unify the multiple small grammars into bigger grammars. It was started to unify the *-definition rules given they have a lower complexity than *-reference rules.


Whitespaces
===========

Most entry rules are written so that initial and final whitespaces are discarded:
```
rule = whitespaces my_real_rule whitespaces
my_real_rule = …
whitespaces = ~"\s*"
```

With the exception that, if a quote is expected to follow, it should be avoided to remove final whitespaces, because the presence or not of a newline could have a meaning for so-called “free quotes”, which are single-line quotes after a newline but without quote delimiters ("" or «») (such amendments are found in the Sénat).
