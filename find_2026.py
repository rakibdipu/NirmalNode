with open(r'c:\Users\ASUS\Downloads\capstone 3.2\nirmalnode_thesis\references.bib', 'r', encoding='utf-8') as f:
    text = f.read()

import re
entries = text.split('@')
print(f"Total bib entries: {len(entries)}")
for e in entries:
    if '2026' in e:
        first_line = e.split('\n')[0]
        title_match = re.search(r'title\s*=\s*[\"{](.*?)[\"}]', e, re.IGNORECASE)
        author_match = re.search(r'author\s*=\s*[\"{](.*?)[\"}]', e, re.IGNORECASE)
        journal_match = re.search(r'journal\s*=\s*[\"{](.*?)[\"}]', e, re.IGNORECASE)
        print("--- 2026 Paper ---")
        print("Key:", first_line)
        if author_match: print("Author:", author_match.group(1))
        if title_match: print("Title:", title_match.group(1))
        if journal_match: print("Journal:", journal_match.group(1))
