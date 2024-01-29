from collections import defaultdict
import random

def generate_bigram_model(text):
    words = text.split()
    bigrams = [(words[i], words[i+1]) for i in range(len(words)-1)]
    model = defaultdict(list)
    for w1, w2 in bigrams:
        model[w1].append(w2)
    return model

def generate_text_from_bigram(model, length=10):
    current_word = random.choice(list(model.keys()))
    text = [current_word]
    for _ in range(length-1):
        next_words = model.get(current_word, [])
        if not next_words:
            current_word = random.choice(list(model.keys()))  # Choose a new random starting word
        else:
            next_word = random.choice(next_words)
            text.append(next_word)
            current_word = next_word
    return ' '.join(text)

# Example usage
text = "This is a sample text used for generating a bigram model."
bigram_model = generate_bigram_model(text)
generated_text = generate_text_from_bigram(bigram_model, length=20)
print(generated_text)
