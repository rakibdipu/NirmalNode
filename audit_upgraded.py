import os, re

tex_dir = "thesis_upgraded"
print("=" * 60)
print("AUDITING THESIS UPGRADED DIRECTORY")
print("=" * 60)

bib_path = os.path.join(tex_dir, "references.bib")
with open(bib_path, "r", encoding="utf-8") as f:
    bib_text = f.read()
bib_keys = set(re.findall(r"@\w+\s*\{\s*([^,]+),", bib_text))
print(f"[INFO] Found {len(bib_keys)} entries in references.bib")

all_labels = {}
all_citations = []
all_refs = []

for root, dirs, files in os.walk(tex_dir):
    for file in files:
        if file.endswith(".tex"):
            fp = os.path.join(root, file)
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
            
            labels = re.findall(r"\\label\{([^}]+)\}", content)
            for lab in labels:
                if lab in all_labels:
                    print(f"[ERROR] Duplicate label: '{lab}' in {file} and {all_labels[lab]}")
                else:
                    all_labels[lab] = file
                    
            cites = re.findall(r"\\cite[pt]?\{([^}]+)\}", content)
            for c_group in cites:
                for c in c_group.split(","):
                    all_citations.append((file, c.strip()))
                    
            refs = re.findall(r"\\(?:c|page)?ref\{([^}]+)\}", content)
            for r in refs:
                all_refs.append((file, r.strip()))

missing_cites = [(f, c) for f, c in all_citations if c not in bib_keys]
if missing_cites:
    print(f"[ERROR] {len(missing_cites)} Missing citations:")
    for f, c in missing_cites:
        print(f"   {f}: {c}")
else:
    print("[PASS] All citations exist in references.bib!")

broken_refs = [(f, r) for f, r in all_refs if r not in all_labels]
if broken_refs:
    print(f"[WARNING] Broken refs: {broken_refs[:5]}")
else:
    print("[PASS] All internal references exist!")
