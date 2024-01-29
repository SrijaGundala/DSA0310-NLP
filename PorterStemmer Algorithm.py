from nltk.stem import PorterStemmer
words = ["running", "easily", "consistently"]
stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(word) for word in words]

print(stemmed_words)
