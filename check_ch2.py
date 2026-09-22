with open(r'c:\Users\ASUS\Downloads\capstone 3.2\nirmalnode_thesis\chapters\chapter2_literature_review.tex', 'r', encoding='utf-8') as f:
    text = f.read()

import re
citations = re.findall(r'\\cite[pt]?\{([^}]+)\}', text)
c_set = set()
for c in citations:
    for item in c.split(','):
        c_set.add(item.strip())

print(f"Citations in Chapter 2: {len(c_set)}")
for c in sorted(c_set):
    print(" ", c)
