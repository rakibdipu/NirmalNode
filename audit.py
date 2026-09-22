import re

# Check server routes
content = open('server.py', encoding='utf-8').read()
routes = re.findall(r"@app\.route\('([^']+)'\)", content)
print("=== SERVER ROUTES ===")
for r in routes:
    print("  ", r)

print()

# Check JS functions
js = open('app.js', encoding='utf-8').read()
fns = re.findall(r'(?:async\s+)?function\s+(\w+)', js)
print("=== JS FUNCTIONS ===")
for f in fns:
    print("  ", f)

print()

# Check HTML IDs used in JS but check they exist in HTML
html = open('index.html', encoding='utf-8').read()
js_ids = re.findall(r"\$\('(\w+)'\)", js)
unique_ids = sorted(set(js_ids))
print("=== JS getElementById IDs vs HTML ===")
missing = []
for id_ in unique_ids:
    in_html = ('id="' + id_ + '"' in html) or ("id='" + id_ + "'" in html)
    status = "OK" if in_html else "MISSING"
    if not in_html:
        missing.append(id_)
    print("  [" + status + "] " + id_)

print()
if missing:
    print("IDs MISSING FROM HTML:", missing)
else:
    print("ALL JS IDs FOUND IN HTML")
