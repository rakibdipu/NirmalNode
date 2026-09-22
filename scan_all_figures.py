import os, re

tex_dir = r'C:\Users\ASUS\Downloads\capstone 3.2\thesis_src\nirmalnode_thesis'

print("=== SCANNING ALL .TEX FILES FOR FIGURES & CODE DIAGRAMS ===")
total_figs = 0
for root, dirs, files in os.walk(tex_dir):
    for f in sorted(files):
        if f.endswith('.tex'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Check for tikz
            tikz_matches = re.findall(r'\\begin\{tikzpicture\}[\s\S]*?\\end\{tikzpicture\}', content)
            if tikz_matches:
                print(f'[FOUND TIKZ] {f}: {len(tikz_matches)} tikzpicture block(s)')
                
            # Check for all figures
            figs = re.findall(r'\\begin\{figure\}[\s\S]*?\\end\{figure\}', content)
            for i, fig in enumerate(figs, 1):
                total_figs += 1
                cap = re.search(r'\\caption\{([^}]+)\}', fig)
                inc = re.findall(r'\\includegraphics(?:\[.*?\])?\{([^}]+)\}', fig)
                cap_text = cap.group(1)[:55] if cap else 'No caption'
                print(f'  {f} | Fig {i}: cap="{cap_text}" | includegraphics={inc}')

print(f"\nTotal figures found: {total_figs}")
