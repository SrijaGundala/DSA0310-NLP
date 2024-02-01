from transformers import MarianMTModel, MarianTokenizer

def translate_text(text, src_lang='en', tgt_lang='fr'):
    model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=50)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

text = "Translate this text to French."
translated_text = translate_text(text)
print("Translated Text:", translated_text)
