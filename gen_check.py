import re

html = open(r'NirmalNode_Defense_Presentation.html', 'r', encoding='utf-8').read()

# Count NirmalNode keyword
for kw in ['NirmalNode', 'PM2.5', 'TODO', 'Champion', 'HEPA', 'Slide']:
    print(f'{kw}: {html.count(kw)}')

# Find class=slide occurrences
slide_divs = html.count('class="slide"') + html.count("class='slide'")
print(f'slide divs: {slide_divs}')

# show structure of first 3000 chars (no base64)
plain = html[:5000].replace('\n','|')
print(plain[:500])
