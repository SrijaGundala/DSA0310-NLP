# 20. Basic Information Retrieval System using TF-IDF in Python:
from sklearn.feature_extraction.text import TfidfVectorizer

documents = [
    "This is the first document.",
    "This document is the second document.",
    "And this is the third one.",
    "Is this the first document?",
]

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

query = "document"
query_vector = tfidf_vectorizer.transform([query])
similarities = tfidf_matrix.dot(query_vector.T).toarray().flatten()
sorted_indices = similarities.argsort()[::-1]

for idx in sorted_indices:
    print(f"Document {idx + 1}: {documents[idx]}")
