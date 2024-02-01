import nltk

def extract_noun_phrases(sentence):
    grammar = r"""
        NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
    """
    cp = nltk.RegexpParser(grammar)
    tagged_sentence = nltk.pos_tag(nltk.word_tokenize(sentence))
    parsed_sentence = cp.parse(tagged_sentence)

    noun_phrases = []
    for subtree in parsed_sentence.subtrees():
        if subtree.label() == 'NP':
            words = [word for word, tag in subtree.leaves()]
            noun_phrases.append(' '.join(words))
    return noun_phrases

sentence = "The quick brown fox jumps over the lazy dog"
noun_phrases = extract_noun_phrases(sentence)
print("Noun Phrases:", noun_phrases)
