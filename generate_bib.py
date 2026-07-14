import json
import re

with open('selected_papers.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

# Generate citation keys
def generate_key(author_str, year):
    if not author_str:
        last_name = "unknown"
    else:
        # Get first author's last name
        first_author = author_str[0]
        # roughly get last word
        last_name = first_author.split()[-1].lower()
        last_name = re.sub(r'[^a-z]', '', last_name)
    
    if not last_name:
        last_name = "unknown"
    
    return f"{last_name}{year}"

key_counts = {}
for p in papers:
    base_key = generate_key(p.get('authors'), p.get('year'))
    if base_key not in key_counts:
        key_counts[base_key] = 0
        p['cite_key'] = base_key
    else:
        key_counts[base_key] += 1
        suffix = chr(97 + key_counts[base_key]) # 'a', 'b', etc.
        p['cite_key'] = f"{base_key}{suffix}"

# Sort papers alphabetically by cite_key
papers.sort(key=lambda x: x['cite_key'])

# Generate references.bib
bib_lines = []
for p in papers:
    # Use @article as default, or @inproceedings if conference
    entry_type = "article"
    venue = (p.get('venue') or "").lower()
    if "proceedings" in venue or "conference" in venue or "symposium" in venue:
        entry_type = "inproceedings"
    elif not venue:
        entry_type = "misc"
        
    bib_lines.append(f"@{entry_type}{{{p['cite_key']},")
    
    # authors formatted with ' and '
    authors_str = " and ".join(p.get('authors', []))
    bib_lines.append(f"  author = {{{authors_str}}},")
    bib_lines.append(f"  title = {{{p.get('title')}}},")
    
    if entry_type == "article":
        if p.get('venue'): bib_lines.append(f"  journal = {{{p['venue']}}},")
    elif entry_type == "inproceedings":
        if p.get('venue'): bib_lines.append(f"  booktitle = {{{p['venue']}}},")
    
    bib_lines.append(f"  year = {{{p.get('year')}}},")
    if p.get('doi'):
        # Just put the URL/DOI
        doi_val = p['doi'].replace('https://doi.org/', '')
        bib_lines.append(f"  doi = {{{doi_val}}},")
    
    bib_lines.append("}")
    bib_lines.append("")

with open('references.bib', 'w', encoding='utf-8') as f:
    f.write("\n".join(bib_lines))

# Output mapping for the rewrite phase
mapping_lines = ["# Citation Key Mapping\n"]
for i, p in enumerate(papers):
    mapping_lines.append(f"[{i+1}] = {p['cite_key']} | {p['title']} | Section: {p['_section']}")
    
with open('citation_mapping.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(mapping_lines))

with open('selected_papers_sorted.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=2)

print(f"Generated references.bib and mapping for {len(papers)} papers.")
