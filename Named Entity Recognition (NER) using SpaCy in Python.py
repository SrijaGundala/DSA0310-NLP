import spacy

def perform_ner(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.text, ent.label_)

# Example usage
text = "Your text with named entities here"
perform_ner(text)
