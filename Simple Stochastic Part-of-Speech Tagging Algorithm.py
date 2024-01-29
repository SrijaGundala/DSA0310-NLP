from collections import defaultdict
import random

def train_stochastic_pos_tagger(training_data):
    pos_counts = defaultdict(lambda: defaultdict(int))
    for sentence in training_data:
        for word, pos in sentence:
            pos_counts[word][pos] += 1
    return pos_counts

def stochastic_pos_tagger(model, word):
    pos_counts = model[word]
    total_count = sum(pos_counts.values())
    rand_num = random.randint(1, total_count)
    for pos, count in pos_counts.items():
        rand_num -= count
        if rand_num <= 0:
            return pos

# Example usage
training_data = [[("The", "DT"), ("cat", "NN"), ("runs", "VBZ")], [("A", "DT"), ("dog", "NN"), ("barks", "VBZ")]]
pos_model = train_stochastic_pos_tagger(training_data)
word = "cat"
pos_tag = stochastic_pos_tagger(pos_model, word)
print(f"The most probable POS tag for '{word}' is '{pos_tag}'.")
