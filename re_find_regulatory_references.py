import json, re

content = ''
with open('Costituzione_ITALIANO_dirty.txt', 'r', encoding='utf-8') as f:
    content = f.read()

matches = []    
pattern = r"costituzionale \d{1,2} \w+ \d{4}, n\. \d+ «.*?»"
for match in re.finditer(pattern, content):
    entity = {
        "label": match.group(),
        "span_start": match.start(),
        "span_end": match.end()
    }
    matches.append(entity)

with open("regulatory_references.json", 'w', encoding='utf-8') as f_out:
    json.dump(matches, f_out, ensure_ascii=False, indent=4)

print(f"Found {len(matches)} matches and saved!")