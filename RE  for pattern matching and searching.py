import re

# Sample text
text = "Hello, my email is example@email.com"

# Define the pattern
pattern = r'[\w\.-]+@[\w\.-]+'

# Search for the pattern
match = re.search(pattern, text)

if match:
    print("Email found:", match.group())
else:
    print("Email not found.")
