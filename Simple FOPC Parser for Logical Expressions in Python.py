import re

def parse_fopc(expression):
    tokens = re.findall(r'[A-Za-z]+|\(|\)', expression)
    return tokens

expression = "(P AND Q) OR (R AND S)"
parsed_expression = parse_fopc(expression)
print(parsed_expression)
