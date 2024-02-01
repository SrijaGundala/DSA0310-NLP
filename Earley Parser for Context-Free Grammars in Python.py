import nltk
nltk.download('earley_parser')
from nltk.parse.earleychart import EarleyChartParser
from nltk import CFG
grammar = CFG.fromstring("""
S -> NP VP
NP -> Det N
VP -> V NP
Det -> 'the' | 'The'
N -> 'cat' | 'mouse'
V -> 'chased'
""")
parser = EarleyChartParser(grammar)
sentence = "The cat chased the mouse"

for tree in parser.parse(sentence.split()):
    tree.pretty_print()
