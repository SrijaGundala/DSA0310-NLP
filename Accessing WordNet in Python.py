# 17. Accessing WordNet in Python:
from nltk.corpus import wordnet

word = "car"
synsets = wordnet.synsets(word)
for synset in synsets:
    print(f"Synset: {synset.name()}")
    print(f"Definition: {synset.definition()}")
    print(f"Examples: {synset.examples()}")
    print()

