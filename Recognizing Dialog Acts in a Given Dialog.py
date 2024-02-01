from nltk import pos_tag, word_tokenize

def recognize_dialog_acts(dialog):
    tagged_dialog = pos_tag(word_tokenize(dialog))
    dialog_acts = set()
    for word, pos in tagged_dialog:
        if pos == 'VB' or pos == 'VBP':
            dialog_acts.add('Assertion')
        elif pos == 'MD':
            dialog_acts.add('Request')
    return dialog_acts

dialog = "Can you pass the salt?"
dialog_acts = recognize_dialog_acts(dialog)
print("Dialog Acts:", dialog_acts)
