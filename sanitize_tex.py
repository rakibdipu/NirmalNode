import os

tex_dir = r'C:\Users\ASUS\Downloads\capstone 3.2\thesis_src\nirmalnode_thesis'

replacements = {
    '\u2014': '---',  # em-dash
    '\u2013': '--',   # en-dash
    '\u201c': '``',   # left double quote
    '\u201d': "''",   # right double quote
    '\u2018': '`',    # left single quote
    '\u2019': "'",    # right single quote
    '\u00a0': ' ',    # non-breaking space
}

for root, dirs, files in os.walk(tex_dir):
    for f in files:
        if f.endswith('.tex'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            new_content = content
            for k, v in replacements.items():
                new_content = new_content.replace(k, v)
            if new_content != content:
                with open(fp, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f'Sanitized: {f}')

print('All TeX files sanitized.')
