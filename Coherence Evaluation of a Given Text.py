from gensim.models import CoherenceModel
from gensim.corpora import Dictionary

def evaluate_coherence(texts):
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    coherence_model = CoherenceModel(corpus=corpus, texts=texts, dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model.get_coherence()
    return coherence_score

texts = [["apple", "banana", "orange"], ["car", "bike", "bus"], ["dog", "cat", "rabbit"]]
coherence_score = evaluate_coherence(texts)
print("Coherence Score:", coherence_score)
