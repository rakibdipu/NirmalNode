import os, re

tex_dir = r'C:\Users\ASUS\Downloads\capstone 3.2\thesis_src\nirmalnode_thesis'

print("="*60)
print("NIRMALNODE THESIS - DEEP LATEX AUDIT")
print("="*60)

# 1. Parse references.bib keys
bib_path = os.path.join(tex_dir, 'references.bib')
with open(bib_path, 'r', encoding='utf-8') as f:
    bib_text = f.read()
bib_keys = set(re.findall(r'@\w+\s*\{\s*([^,]+),', bib_text))
print(f'[INFO] Found {len(bib_keys)} entries in references.bib')

# 2. Collect all labels and citations from all .tex files
all_labels = {}
all_citations = []
all_refs = []
all_figures = []
files_content = {}

for root, dirs, files in os.walk(tex_dir):
    for file in files:
        if file.endswith('.tex'):
            fp = os.path.join(root, file)
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            files_content[file] = content
            
            # Find labels
            labels = re.findall(r'\\label\{([^}]+)\}', content)
            for lab in labels:
                if lab in all_labels:
                    print(f'[ERROR] Duplicate label: "{lab}" in {file} and {all_labels[lab]}')
                else:
                    all_labels[lab] = file
                    
            # Find citations
            cites = re.findall(r'\\cite[pt]?\{([^}]+)\}', content)
            for c_group in cites:
                for c in c_group.split(','):
                    all_citations.append((file, c.strip()))
                    
            # Find refs
            refs = re.findall(r'\\(?:c|page)?ref\{([^}]+)\}', content)
            for r in refs:
                all_refs.append((file, r.strip()))
                
            # Find includegraphics
            figs = re.findall(r'\\includegraphics(?:\[.*?\])?\{([^}]+)\}', content)
            for fig in figs:
                all_figures.append((file, fig.strip()))

# 3. Check citations
missing_cites = []
for file, c in all_citations:
    if c not in bib_keys:
        missing_cites.append((file, c))
if missing_cites:
    print(f'[ERROR] Missing citations ({len(missing_cites)}):', missing_cites)
else:
    print(f'[PASS] All {len(all_citations)} citation calls exist in references.bib!')

# 4. Check refs
missing_refs = []
for file, r in all_refs:
    if r not in all_labels:
        missing_refs.append((file, r))
if missing_refs:
    print(f'[ERROR] Missing label references ({len(missing_refs)}):', missing_refs)
else:
    print(f'[PASS] All {len(all_refs)} cross-references have matching labels!')

# 5. Check figures
missing_files = []
fig_dir = os.path.join(tex_dir, 'figures')
for file, fig in all_figures:
    bname = os.path.basename(fig)
    if not os.path.exists(os.path.join(fig_dir, bname)):
        missing_files.append((file, fig))
if missing_files:
    print(f'[ERROR] Missing figure files ({len(missing_files)}):', missing_files)
else:
    print(f'[PASS] All {len(all_figures)} includegraphics targets exist in figures/ directory!')

# 6. Check tables columns and row structure
print("\n--- Checking Table Structures ---")
table_issues = 0
for file, content in files_content.items():
    # Find all tabular environments
    tabulars = re.findall(r'\\begin\{tabular\}\s*(\{[^}]+\})([\s\S]*?)\\end\{tabular\}', content)
    for col_def, tab_body in tabulars:
        # count columns in definition (strip @{...}, p{...}, etc.)
        clean_cols = re.sub(r'@[^}]*\}', '', col_def)
        clean_cols = re.sub(r'p\{[^}]*\}', 'c', clean_cols)
        clean_cols = re.sub(r'm\{[^}]*\}', 'c', clean_cols)
        num_cols = len(re.findall(r'[lcr]', clean_cols))
        
        # check rows
        rows = [r.strip() for r in tab_body.split(r'\\') if r.strip() and not r.strip().startswith(r'\toprule') and not r.strip().startswith(r'\midrule') and not r.strip().startswith(r'\bottomrule') and not r.strip().startswith(r'\hline')]
        for row in rows:
            # skip comment lines or command-only rows
            if row.startswith('%') or not row:
                continue
            # count ampersands
            amps = row.count('&')
            if amps != num_cols - 1 and num_cols > 0:
                # check if multirow or multicolumn is used
                if r'\multicolumn' not in row:
                    print(f'[WARN] Possible column mismatch in {file}: expected {num_cols} cols ({num_cols-1} ampersands), got {amps} in row: {row[:50]}...')
                    table_issues += 1

if table_issues == 0:
    print("[PASS] All tabular environments have exact matching column counts.")

# 7. Check math delimiters
print("\n--- Checking Math Delimiters ---")
math_issues = 0
for file, content in files_content.items():
    # remove escaped \$
    clean_content = content.replace(r'\$', '')
    # count unescaped single $
    dollar_count = clean_content.count('$')
    if dollar_count % 2 != 0:
        print(f'[ERROR] Unbalanced dollar signs in {file}: {dollar_count}')
        math_issues += 1

if math_issues == 0:
    print("[PASS] All dollar math delimiters are perfectly balanced.")

# 8. Check for any unresolved TODOs
print("\n--- Checking Placeholder Artifacts ---")
todo_count = 0
for file, content in files_content.items():
    if file == 'main.tex':
        continue
    todos = re.findall(r'\\TODO\{([^}]+)\}', content)
    figplaces = re.findall(r'\\FIGPLACE', content)
    if todos:
        print(f'[WARN] {len(todos)} \\TODO found in {file}: {todos}')
        todo_count += len(todos)
    if figplaces:
        print(f'[WARN] \\FIGPLACE found in {file}')
        todo_count += len(figplaces)

if todo_count == 0:
    print("[PASS] Zero \\TODO or \\FIGPLACE left in document body.")

print("\n" + "="*60)
print("AUDIT COMPLETE")
print("="*60)
