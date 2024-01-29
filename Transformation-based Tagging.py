def apply_transformation_rule(word):
    if word.endswith('ing'):
        return 'VBG' 
    elif word.endswith('ed'):
        return 'VBD' 
    elif word.endswith('s'):
        return 'NNS' 
    else:
        return 'NN'  

word = "running"
pos_tag = apply_transformation_rule(word)
print(f"The most probable POS tag for '{word}' is '{pos_tag}'.")
