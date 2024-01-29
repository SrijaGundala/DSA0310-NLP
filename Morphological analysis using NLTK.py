import nltk
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')
text = "cats running"
tokens = nltk.word_tokenize(text)

lemmatizer = WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]

print(lemmatized_words)
