#! /usr/bin/env python3.5
"""NLTK demo showing chart parsing"""

# Not necessary; good for python 2.7 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# an example of a relative imports. Generally only import what you're
# using. The 'as _Parser' makes the token "_Parser" refer to the
# 'ArgumentParser' class instead of 'ArgumentParser'. This extra
# aliasing is not really necessary
from argparse import ArgumentParser as _Parser

# nltk uses "lazy loading," so importing nltk directly rather than using
# relative imports is not terribly slow
import nltk

__author__ = "Sean Robertson"
__email__ = "t6robert@cdf.toronto.edu"

def main(args=None):
    '''Stepwise completion of chart parsing for online tutorial'''
    # ~~~ Argument parser
    parser = _Parser(description=main.__doc__)
    parser.add_argument(
        'to_step', nargs='?', type=int, default=float('inf'),
        help='Run until this step, then exit')
    namespace = parser.parse_args(args)
    to_step = namespace.to_step
    # ~~~~ Define grammar ~~~~
    # - Non terminals. These are syntactic categories. These are the
    #   nodes of the parse tree
    non_terms = dict((sym, nltk.grammar.Nonterminal(sym)) for sym in (
        'S', # sentence
        'NP', # noun phrase
        'N', # noun
        'Det', # determiner
        'VP', # verb phrase
        'V', # verb
    ))
    # - Productions. The grammatical rules dictating how non terminals
    #   can be broken down into a sequence of (non)terminals. These are
    #   the possible edges of the parse tree
    # - Terminals. Lexical elements of sentence. Strings. Leaves in the graph.
    productions = tuple(nltk.grammar.Production(lhs, rhs) for lhs, rhs in (
        (non_terms['S'], (non_terms['NP'], non_terms['VP'])), # S -> NP VP
        (non_terms['NP'], (non_terms['Det'], non_terms['N'])), # NP -> Det N
        (non_terms['NP'], (non_terms['N'],)), # NP -> N
        (non_terms['N'], ('Nadia',)), # N -> 'Nadia'
        (non_terms['N'], ('Gerald',)), # N -> 'Gerald'
        (non_terms['N'], ('eggplant',)), # N -> 'eggplant'
        (non_terms['Det'], ('the',)), # Det -> 'the'
        (non_terms['Det'], ('an',)), # Det -> 'an'
        (non_terms['VP'], (non_terms['V'],)), # VP -> V
        (non_terms['VP'], (non_terms['V'], non_terms['NP'])), # VP -> V NP
        (non_terms['V'], ('scolds',)), # V -> 'scolds'
        (non_terms['V'], ('fondles',)), # V -> 'fondles'
    ))
    # - Grammar: the set of productions and an initial state/root (the
    # sentence in our case)
    cfg = nltk.grammar.CFG(non_terms['S'], productions)
    print('Grammmar from objects:', cfg) # print it to stdout
    # NLTK also often has shortcuts for parsing things from strings or
    # files. In this case:
    cfg = nltk.grammar.CFG.fromstring('''
        S -> NP VP
        NP -> Det N
        NP -> N
        N -> 'Nadia'
        N -> 'Gerald'
        N -> 'eggplant'
        Det -> 'the'
        Det -> 'an'
        VP -> V
        VP -> V NP
        V -> 'scolds'
        V -> 'fondles'
    ''')
    print('Grammar from string:', cfg)
    if to_step <= 1:
        return 0
    # ~~~~ Parsing automatically ~~~~
    sentence_1 = nltk.tokenize.word_tokenize('Nadia fondles the eggplant')
    sentence_2 = nltk.tokenize.word_tokenize('Gerald scolds Nadia')
    # parsing by resolving leaves first
    bu_parser = nltk.parse.BottomUpChartParser(cfg)
    tree_1 = bu_parser.parse_one(sentence_1)
    tree_2 = bu_parser.parse_one(sentence_2)
    print('Sentence 1 parse: ', end='')
    tree_1.pprint() # pretty print to stdout
    print('Sentence 2 parse: ', end='')
    tree_2.pprint()
    # parsing by resolving root first
    td_parser = nltk.parse.TopDownChartParser(cfg)
    assert tree_1 == td_parser.parse_one(sentence_1)
    assert tree_2 == td_parser.parse_one(sentence_2)
    # we can also walk through the steps of the parse by calling
    # *_parser.chart_parse(sentence_*). This returns an iterable that we
    # can loop through. Uncomment these lines:
    # for step in bu_parser.chart_parse(sentence_1):
    #     print(step)
    if to_step == 2:
        return 0
    # a GUI parse of a more interesting string
    nltk.app.chartparser_app.app()
    if to_step == 3:
        return 0
    return 0

if __name__ == '__main__':
    exit(main())
