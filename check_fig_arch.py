with open(r'c:\Users\ASUS\Downloads\capstone 3.2\nirmalnode_thesis\chapters\chapter3_methodology.tex', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Look for figure five-layer
idx = text.find('five-layer')
if idx != -1:
    print("Found 'five-layer' in chapter3:")
    print(text[max(0, idx-200):min(len(text), idx+1200)])
else:
    print("'five-layer' not found, searching for figure:")
    figs = re.findall(r'\\begin\{figure\}.*?\\end\{figure\}', text, re.DOTALL)
    for i, fig in enumerate(figs[:5]):
        print(f"--- Figure {i+1} ---")
        print(fig[:300])
