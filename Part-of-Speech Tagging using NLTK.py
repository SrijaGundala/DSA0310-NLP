import nltk
nltk.download('averaged_perceptron_tagger')

# Sample text
text = "The quick brown fox jumps over the lazy dog."

# Tokenization
tokens = nltk.word_tokenize(text)

# Part-of-speech tagging
pos_tags = nltk.pos_tag(tokens)

print(pos_tags)
