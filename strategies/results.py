import json

with open('formulas/output.json', 'r') as f:
    data = json.load(f)

print(data)
