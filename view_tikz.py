with open(r'c:\Users\ASUS\Downloads\capstone 3.2\nirmalnode_thesis\chapters\chapter3_methodology.tex', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('begin{tikzpicture}')
print("Full TikZ for Figure 3.1:")
print(text[idx:idx+1500])
