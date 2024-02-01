import spacy

def resolve_references(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    resolved_text = []
    for token in doc:
        if token.dep_ == 'pron' and token.head.pos_ == 'NOUN':
            resolved_text.append(token.head.text)
        else:
            resolved_text.append(token.text)
    return ' '.join(resolved_text)

text = "John lost his phone. He was very upset."
resolved_text = resolve_references(text)
print("Resolved Text:", resolved_text)
