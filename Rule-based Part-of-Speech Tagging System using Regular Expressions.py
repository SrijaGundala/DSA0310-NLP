import re

def rule_based_pos_tagger(word):
    if re.match(r'\d+', word):
        return 'CD'  # Cardinal Number
    elif re.match(r'.+ly$', word):
        return 'RB'  # Adverb
    elif re.match(r'.+(ing|ed)$', word):
        return 'VB'  # Verb
    else:
        return 'NN'  # Noun by default

# Example usage
word = "running"
pos_tag = rule_based_pos_tagger(word)
print(f"The most probable POS tag for '{word}' is '{pos_tag}'.")
