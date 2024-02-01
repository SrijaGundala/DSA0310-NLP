import openai

openai.api_key = "your-api-key"

def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

prompt = "Once upon a time,"
generated_text = generate_text(prompt)
print("Generated Text:", generated_text)
