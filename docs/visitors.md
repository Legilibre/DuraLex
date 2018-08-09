Visitors
========

The visitors do operations on the DuraLex tree, for instance reorder some nodes or implement lookback references. The DuraLex tree is parsed by a walk top-down then first-to-last-child.


DuraLex visitors
----------------

### Abstract visitors

#### AbstractVisitor

Abstract visitor class with a walking method parsing the DuraLex tree and calling the appropriate method depending on node type.

The only public method is `visit(node)` taking a DuraLex node as argument.

##### Internals

The mapping “node type to method” is declared during class initialisation as `self.visitors`.

The walking method `visit_node(node)` does 3 things:

* call the method for current node as “pre-treatment”;
* recursively iterate over direct children;
* call the method for current node as “post-treatment”;

Each method treating a node type takes two arguments: `node` and `post`. This latter argument is a boolean: `True` when the method is called as “post-treatment”, `False` when the method is called as “pre-treatment”. By default all methods referenced in `self.visitors` are declared and are stubs.

### Technical visitors

#### Before export

Before export, the visitors `DeleteEmptyChildrenVisitor` and `DeleteUUIDVisitor` are cosmetic visitors to remove unusefull information, and `DeleteParentVisitor` is a mandatory visitor.

##### DeleteEmptyChildrenVisitor

This visitor operates on all nodes. It is an idempotent visitor.

Mainly usefull before export, this visitor removes the empty lists of children.

##### DeleteUUIDVisitor

This visitor operates on all nodes. It is an idempotent visitor.

During internal operations, all DuraLex nodes have a `uuid` property to uniquely identify nodes; they are created by internal tree methods.

These unique identifiers are generally useless for typical uses and they could be removed before export: this is this visitor’s work.

##### DeleteParentVisitor

This visitor operates on all nodes. It is an idempotent visitor.

During internal operations, all DuraLex nodes have a `parent` property to enable bottom-up walks.

Before export, these properties must be removed: this is this visitor’s work, which should be the last visitor before exporting a DuraLex tree. The opposite visitor is `AddParentVisitor`.

#### After import

After import, the visitor `AddParentVisitor` is a mandatory visitor.

##### AddParentVisitor

This visitor operates on all nodes. It is an idempotent visitor.

During internal operations, all DuraLex nodes have a `parent` property to enable bottom-up walks.

This visitor adds a `parent` property on each node referencing the parend node, and should be the first visitor after importing a DuraLex tree. The opposite visitor is `DeleteParentVisitor`.

### Tree-manipulation visitors

#### ResolveLookbackReferencesVisitor

This visitor operates on lookback-reference-type nodes. It is an idempotent visitor.

It resolves the lookback references by searching in the former nodes which one is the implicit reference. The resolved reference is:

* if the lookback reference has a type (in its first child): the latest reference-type node with the same type;
* else: the latest reference-type node.

In either case, "latest" is understood in linear order of the whole sentence, not hierarchically when there are headers.

FIXME:

* Check the resolve algorithm over multiple situations, particularly with the undefined lookback reference "Il est ajouté" in hierarchical amendements (with headers).

#### ForkReferenceVisitor

This visitor operates on reference-type nodes. It is an idempotent visitor.

It splites (direct children) lists of references in a reference-type node, and transforms this into a list of reference-subreferences (with the same relative order).

Typically it is an introductory sentence says to modify some large-scale part (e.g. an article) and then are enumerated smaller-scale parts (e.g. sentences).

#### ResolveFullyQualifiedDefinitionsVisitor

This visitor operates on edit-type nodes. It is an idempotent visitor.

(NB: I’m not sure to understand the case where it is useful. ~ Seb35)

It manages the case where there are multiple definition-type nodes and there are empty definition-type nodes (i.e. without a quote-type node). In these cases, empty definition-type nodes are copied and embedded into non-empty definition-type nodes. Children of non-empty definition-type nodes (which should be quote-type nodes) are moved deepest.

#### ResolveFullyQualifiedReferencesVisitor

This visitor operates on parents of edit-type nodes. It is an idempotent visitor.

It manages the case of an introductory sentence in a header, whose the context applies inside this header, or more generally in the cases of introductory sentences (edit-type nodes with editType=edit). It copies the references of this introductory sentence in the next children and sub-children.

#### FixMissingCodeOrLawReferenceVisitor

This visitor operates on article-reference-type nodes. It is an idempotent visitor.

It adds a code- or law-reference-type node on article-type nodes when they don’t have such nodes, either in their ancestors or in their descendants.

#### SortReferencesVisitor

This visitor operates on reference-type nodes. It is an idempotent visitor.

It reorder references by canonical order defined in `duralex.tree.TYPE_REFERENCE`.

FIXME:

* Should we raise because we're not supposed to have the same \*-reference twice? `{"type": "alinea-reference", "children": [{"type": "alinea-reference"}]}`
* Should we raise when we have a sub-list of references? of different type? `{"type": "alinea-reference", "children": [{"type": "sentence-reference"}, {"type": "word-reference"}]}`

#### SwapDefinitionAndReferenceVisitor

This visitor operates on edit-type nodes. It is an idempotent visitor.

It normalises these nodes by putting all definition-type nodes at the end of the children list. Consequently there should only be reference-type nodes at the beginning of the children list.

#### RemoveQuotePrefixVisitor

This visitor operates on quote-type nodes. It is an idempotent visitor.

It removes the string `"Art. {articleId}. -"` at the beginning of the lines contained in the property `words`.

### Unused/other visitors

#### ForkEditVisitor

This visitor operates on edit-type nodes. It is an idempotent visitor.

It splites (direct children) lists of references and definitions by creating edit-type nodes each with a single reference and definition (if there are definitions). At the end, there are len(references) x max(len(definitions),1) edit-type nodes.


Parsimonious visitors
---------------------

### ToSemanticTreeVisitor



### CaptureVisitor

Simple visitor capturing some Parsimonious nodes corresponding to some rule.

It must be given during initialisation a list of Parsimonious rule names to be captured. The resulting captures can be read in the class property `captures`, which is a map “rule name” → “captured text”.
