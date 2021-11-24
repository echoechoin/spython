# -*- coding: utf-8 -*-
"""
    pyspecific.py
    ~~~~~~~~~~~~~

    Sphinx extension with Python doc-specific markup.

    :copyright: 2008-2014 by Georg Brandl.
    :license: Python license.
"""

ISSUE_URI = 'https://bugs.python.org/issue%s'
SOURCE_URI = 'https://github.com/python/cpython/tree/2.7/%s'

from docutils import nodes, utils
from docutils.parsers.rst import Directive

from sphinx.util.nodes import split_explicit_title
from sphinx.writers.html import HTMLTranslator
from sphinx.writers.latex import LaTeXTranslator

# monkey-patch reST parser to disable alphabetic and roman enumerated lists
from docutils.parsers.rst.states import Body
Body.enum.converters['loweralpha'] = \
    Body.enum.converters['upperalpha'] = \
    Body.enum.converters['lowerroman'] = \
    Body.enum.converters['upperroman'] = lambda x: None

# monkey-patch HTML and LaTeX translators to keep doctest blocks in the
# doctest docs themselves
orig_visit_literal_block = HTMLTranslator.visit_literal_block
def new_visit_literal_block(self, node):
    meta = self.builder.env.metadata[self.builder.current_docname]
    old_trim_doctest_flags = self.highlighter.trim_doctest_flags
    if 'keepdoctest' in meta:
        self.highlighter.trim_doctest_flags = False
    try:
        orig_visit_literal_block(self, node)
    finally:
        self.highlighter.trim_doctest_flags = old_trim_doctest_flags

HTMLTranslator.visit_literal_block = new_visit_literal_block

orig_depart_literal_block = LaTeXTranslator.depart_literal_block
def new_depart_literal_block(self, node):
    meta = self.builder.env.metadata[self.curfilestack[-1]]
    old_trim_doctest_flags = self.highlighter.trim_doctest_flags
    if 'keepdoctest' in meta:
        self.highlighter.trim_doctest_flags = False
    try:
        orig_depart_literal_block(self, node)
    finally:
        self.highlighter.trim_doctest_flags = old_trim_doctest_flags

LaTeXTranslator.depart_literal_block = new_depart_literal_block

# Support for marking up and linking to bugs.python.org issues

def issue_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    issue = utils.unescape(text)
    text = 'bpo-'+ issue
    refnode = nodes.reference(text, text, refuri=ISSUE_URI % issue)
    return [refnode], []


# Support for linking to Python source files easily

def source_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    has_t, title, target = split_explicit_title(text)
    title = utils.unescape(title)
    target = utils.unescape(target)
    refnode = nodes.reference(title, title, refuri=SOURCE_URI % target)
    return [refnode], []


# Support for marking up implementation details

class ImplementationDetail(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    def run(self):
        pnode = nodes.compound(classes=['impl-detail'])
        content = self.content
        add_text = nodes.strong('CPython implementation detail:',
                                'CPython implementation detail:')
        if self.arguments:
            n, m = self.state.inline_text(self.arguments[0], self.lineno)
            pnode.append(nodes.paragraph('', '', *(n + m)))
        self.state.nested_parse(content, self.content_offset, pnode)
        if pnode.children and isinstance(pnode[0], nodes.paragraph):
            pnode[0].insert(0, add_text)
            pnode[0].insert(1, nodes.Text(' '))
        else:
            pnode.insert(0, nodes.paragraph('', '', add_text))
        return [pnode]


# Support for documenting decorators

from sphinx import addnodes
from sphinx.domains.python import PyModulelevel, PyClassmember

class PyDecoratorMixin(object):
    def handle_signature(self, sig, signode):
        ret = super(PyDecoratorMixin, self).handle_signature(sig, signode)
        signode.insert(0, addnodes.desc_addname('@', '@'))
        return ret

    def needs_arglist(self):
        return False

class PyDecoratorFunction(PyDecoratorMixin, PyModulelevel):
    def run(self):
        # a decorator function is a function after all
        self.name = 'py:function'
        return PyModulelevel.run(self)

class PyDecoratorMethod(PyDecoratorMixin, PyClassmember):
    def run(self):
        self.name = 'py:method'
        return PyClassmember.run(self)


# Support for building "topic help" for pydoc

pydoc_topic_labels = [
    'assert', 'assignment', 'atom-identifiers', 'atom-literals',
    'attribute-access', 'attribute-references', 'augassign', 'binary',
    'bitwise', 'bltin-code-objects', 'bltin-ellipsis-object',
    'bltin-file-objects', 'bltin-null-object', 'bltin-type-objects', 'booleans',
    'break', 'callable-types', 'calls', 'class', 'comparisons', 'compound',
    'context-managers', 'continue', 'conversions', 'customization', 'debugger',
    'del', 'dict', 'dynamic-features', 'else', 'exceptions', 'exec', 'execmodel',
    'exprlists', 'floating', 'for', 'formatstrings', 'function', 'global',
    'id-classes', 'identifiers', 'if', 'imaginary', 'import', 'in', 'integers',
    'lambda', 'lists', 'naming', 'numbers', 'numeric-types',
    'objects', 'operator-summary', 'pass', 'power', 'print', 'raise', 'return',
    'sequence-types', 'shifting', 'slicings', 'specialattrs', 'specialnames',
    'string-methods', 'strings', 'subscriptions', 'truth', 'try', 'types',
    'typesfunctions', 'typesmapping', 'typesmethods', 'typesmodules',
    'typesseq', 'typesseq-mutable', 'unary', 'while', 'with', 'yield'
]

from os import path
from time import asctime
from pprint import pformat
from docutils.io import StringOutput
from docutils.utils import new_document

from sphinx.builders import Builder
from sphinx.writers.text import TextWriter


class PydocTopicsBuilder(Builder):
    name = 'pydoc-topics'

    def init(self):
        self.topics = {}

    def get_outdated_docs(self):
        return 'all pydoc topics'

    def get_target_uri(self, docname, typ=None):
        return ''  # no URIs

    def write(self, *ignored):
        writer = TextWriter(self)
        for label in self.status_iterator(pydoc_topic_labels,
                                          'building topics... ',
                                          length=len(pydoc_topic_labels)):
            if label not in self.env.domaindata['std']['labels']:
                self.warn('label %r not in documentation' % label)
                continue
            docname, labelid, sectname = self.env.domaindata['std']['labels'][label]
            doctree = self.env.get_and_resolve_doctree(docname, self)
            document = new_document('<section node>')
            document.append(doctree.ids[labelid])
            destination = StringOutput(encoding='utf-8')
            writer.write(document, destination)
            self.topics[label] = writer.output

    def finish(self):
        f = open(path.join(self.outdir, 'topics.py'), 'wb')
        try:
            f.write('# -*- coding: utf-8 -*-\n'.encode('utf-8'))
            f.write(('# Autogenerated by Sphinx on %s\n' % asctime()).encode('utf-8'))
            f.write(('topics = ' + pformat(self.topics) + '\n').encode('utf-8'))
        finally:
            f.close()


# Support for checking for suspicious markup

import suspicious


# Support for documenting Opcodes

import re

opcode_sig_re = re.compile(r'(\w+(?:\+\d)?)(?:\s*\((.*)\))?')

def parse_opcode_signature(env, sig, signode):
    """Transform an opcode signature into RST nodes."""
    m = opcode_sig_re.match(sig)
    if m is None:
        raise ValueError
    opname, arglist = m.groups()
    signode += addnodes.desc_name(opname, opname)
    if arglist is not None:
        paramlist = addnodes.desc_parameterlist()
        signode += paramlist
        paramlist += addnodes.desc_parameter(arglist, arglist)
    return opname.strip()


# Support for documenting pdb commands

pdbcmd_sig_re = re.compile(r'([a-z()!]+)\s*(.*)')

# later...
#pdbargs_tokens_re = re.compile(r'''[a-zA-Z]+  |  # identifiers
#                                   [.,:]+     |  # punctuation
#                                   [\[\]()]   |  # parens
#                                   \s+           # whitespace
#                                   ''', re.X)

def parse_pdb_command(env, sig, signode):
    """Transform a pdb command signature into RST nodes."""
    m = pdbcmd_sig_re.match(sig)
    if m is None:
        raise ValueError
    name, args = m.groups()
    fullname = name.replace('(', '').replace(')', '')
    signode += addnodes.desc_name(name, name)
    if args:
        signode += addnodes.desc_addname(' '+args, ' '+args)
    return fullname


def setup(app):
    app.add_role('issue', issue_role)
    app.add_role('source', source_role)
    app.add_directive('impl-detail', ImplementationDetail)
    app.add_builder(PydocTopicsBuilder)
    app.add_builder(suspicious.CheckSuspiciousMarkupBuilder)
    app.add_description_unit('opcode', 'opcode', '%s (opcode)',
                             parse_opcode_signature)
    app.add_description_unit('pdbcommand', 'pdbcmd', '%s (pdb command)',
                             parse_pdb_command)
    app.add_description_unit('2to3fixer', '2to3fixer', '%s (2to3 fixer)')
    app.add_directive_to_domain('py', 'decorator', PyDecoratorFunction)
    app.add_directive_to_domain('py', 'decoratormethod', PyDecoratorMethod)
    return {'version': '1.0', 'parallel_read_safe': True}
