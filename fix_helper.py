import re

path = r"c:\Users\ASUS\Downloads\capstone 3.2\build_pptx_full.py"
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('def p(rel):', 'def get_path(rel):')
text = re.sub(r'\bp\("', 'get_path("', text)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Replacement complete: p() -> get_path()")
