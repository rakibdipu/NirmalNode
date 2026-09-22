import os, re

journal_dir = r'c:\Users\ASUS\Downloads\capstone 3.2\journal_nirmalnode'
bib_path = os.path.join(journal_dir, 'references.bib')
tex_path = os.path.join(journal_dir, 'main.tex')

with open(bib_path, 'r', encoding='utf-8') as f:
    bib_text = f.read()

entries = re.findall(r'@(\w+)\s*\{\s*([^,]+),([\s\S]*?)(?=\n@|\Z)', bib_text)
print(f"Total BibTeX entries: {len(entries)}")

def clean_val(val):
    val = re.sub(r'[\{\}\"]', '', val).strip()
    return val

def get_field(body, field):
    m = re.search(r'\b' + field + r'\s*=\s*\{([^}]*)\}', body, re.IGNORECASE)
    if not m:
        m = re.search(r'\b' + field + r'\s*=\s*\"([^"]*)\"', body, re.IGNORECASE)
    if not m:
        m = re.search(r'\b' + field + r'\s*=\s*([0-9]+)', body, re.IGNORECASE)
    return clean_val(m.group(1)) if m else ''

bbl_items = []
for entry_type, key, body in entries:
    authors = get_field(body, 'author')
    title = get_field(body, 'title')
    journal = get_field(body, 'journal') or get_field(body, 'booktitle')
    year = get_field(body, 'year')
    volume = get_field(body, 'volume')
    number = get_field(body, 'number')
    pages = get_field(body, 'pages')
    publisher = get_field(body, 'publisher') or get_field(body, 'institution')
    
    # Format author
    author_list = authors.split(' and ')
    formatted_authors = []
    for a in author_list:
        parts = [p.strip() for p in a.split(',')]
        if len(parts) == 2:
            formatted_authors.append(f"{parts[1]} {parts[0]}")
        else:
            formatted_authors.append(a.strip())
            
    if len(formatted_authors) > 3:
        author_str = f"{formatted_authors[0]} \\emph{{et al.}}"
    elif len(formatted_authors) == 2:
        author_str = f"{formatted_authors[0]} and {formatted_authors[1]}"
    elif len(formatted_authors) == 3:
        author_str = f"{formatted_authors[0]}, {formatted_authors[1]}, and {formatted_authors[2]}"
    else:
        author_str = formatted_authors[0] if formatted_authors else "Anon."

    ref_str = f"\\bibitem{{{key}}}\n{author_str}, ``{title},'' "
    if journal:
        ref_str += f"\\emph{{{journal}}}, "
    if volume:
        ref_str += f"vol.~{volume}, "
    if number:
        ref_str += f"no.~{number}, "
    if pages:
        ref_str += f"pp.~{pages}, "
    if publisher and not journal:
        ref_str += f"{publisher}, "
    if year:
        ref_str += f"{year}."
        
    bbl_items.append(ref_str)

bbl_block = "\\begin{thebibliography}{42}\n\n" + "\n\n".join(bbl_items) + "\n\n\\end{thebibliography}"

# Read main.tex and replace \bibliography{references} with bbl_block
with open(tex_path, 'r', encoding='utf-8') as f:
    tex_text = f.read()

# Replace bibliographystyle and bibliography
target = "\\bibliographystyle{IEEEtran}\n\\bibliography{references}"
if target in tex_text:
    tex_text = tex_text.replace(target, bbl_block)
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(tex_text)
    print("Successfully embedded formatted thebibliography into main.tex!")
else:
    print("Direct replace failed, checking lines...")

