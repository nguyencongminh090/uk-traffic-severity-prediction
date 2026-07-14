import re
import glob
import os

# 1. Load citations from references.bib
in_bib = set()
with open('references.bib', 'r', encoding='utf-8') as f:
    for line in f:
        m = re.match(r'@\w+\{([^,]+),', line)
        if m:
            in_bib.add(m.group(1))

# 2. Parse Markdown files
md_files = sorted(glob.glob('draft_en/0[1-6]*.md'))

all_citations = []
claim_sentences = []
writing_stats = {}

def extract_citations(text):
    # Match [1], [1, 2], [1-3]
    matches = re.findall(r'\[([\d,\s-]+)\]', text)
    cited_nums = []
    for m in matches:
        parts = m.split(',')
        for p in parts:
            p = p.strip()
            if '-' in p:
                start, end = p.split('-')
                cited_nums.extend(list(range(int(start), int(end)+1)))
            elif p.isdigit():
                cited_nums.append(int(p))
    return cited_nums

def get_sentences(text):
    # very naive sentence splitter
    text = re.sub(r'\n+', ' ', text)
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    return [s.strip() for s in sentences if s.strip()]

for md in md_files:
    with open(md, 'r', encoding='utf-8') as f:
        text = f.read()
    
    basename = os.path.basename(md)
    sentences = get_sentences(text)
    
    file_cits = extract_citations(text)
    all_citations.extend(file_cits)
    
    # Writing quality basic stats
    lengths = [len(s.split()) for s in sentences]
    if lengths:
        mean_l = sum(lengths)/len(lengths)
        lengths.sort()
        med_l = lengths[len(lengths)//2]
    else:
        mean_l = med_l = 0
    
    # Passive voice heuristic: be/is/are/was/were/been/being + ed
    passive_count = sum(1 for s in sentences if re.search(r'\b(is|are|was|were|be|been|being)\s+\w+ed\b', s.lower()))
    
    writing_stats[basename] = {
        'num_sentences': len(sentences),
        'mean_len': mean_l,
        'med_len': med_l,
        'passive_pct': (passive_count / len(sentences) * 100) if len(sentences) > 0 else 0
    }
    
    # Extract claims (sentences with numbers or %, or specific empirical words)
    empirical_words = ['showed', 'demonstrated', 'observed', 'proved', 'confirmed', 'highest', 'lowest', 'achieved', 'accuracy', 'f1']
    for s in sentences:
        has_num = bool(re.search(r'\d', s))
        has_emp = any(w in s.lower() for w in empirical_words)
        if (has_num or has_emp) and not s.startswith('#'):
            cits_in_s = extract_citations(s)
            claim_sentences.append({
                'file': basename,
                'text': s,
                'citations': cits_in_s
            })

# Output Citation Integrity Check
with open('draft_en/audit_citation_integrity.md', 'w', encoding='utf-8') as f:
    f.write("# Phase 8B: Citation Integrity Check\n\n")
    
    # Check max citation number
    if all_citations:
        max_cit = max(all_citations)
        missing_cits = [i for i in range(1, max_cit+1) if i not in all_citations]
        if missing_cits:
            f.write(f"⚠️ **Broken/Missing ranges**: Citations {missing_cits} are never used in text.\n")
        else:
            f.write("✅ All numbers from 1 to max are cited.\n")
            
        if max_cit != len(in_bib):
            f.write(f"❌ **Mismatch**: Highest citation is {max_cit}, but .bib has {len(in_bib)} entries.\n")
        else:
            f.write("✅ Citation numbers match bib entry count.\n")
            
        # Check order
        first_appearance = {}
        for num in all_citations:
            if num not in first_appearance:
                first_appearance[num] = len(first_appearance) + 1
        
        out_of_order = []
        for num, expected in first_appearance.items():
            if num != expected:
                out_of_order.append(num)
        
        if out_of_order:
            f.write(f"⚠️ **Citation order**: The following citations appear out of order: {out_of_order[:5]}...\n")
        else:
            f.write("✅ Citations appear in numerical order.\n")
    else:
        f.write("❌ No citations found in text.\n")

# Output Writing Quality Check
with open('draft_en/audit_writing_quality.md', 'w', encoding='utf-8') as f:
    f.write("# Phase 8D: Writing Quality Check\n\n")
    for b, stats in writing_stats.items():
        f.write(f"### {b}\n")
        f.write(f"- Sentences: {stats['num_sentences']}\n")
        f.write(f"- Mean length: {stats['mean_len']:.1f} words\n")
        f.write(f"- Median length: {stats['med_len']} words\n")
        f.write(f"- Passive voice: {stats['passive_pct']:.1f}%\n")
        if stats['passive_pct'] > 40:
            f.write("  - ⚠️ Passive voice exceeds 40% threshold.\n")
        f.write("\n")

# Dump claims for manual review
import json
with open('extracted_claims.json', 'w', encoding='utf-8') as f:
    json.dump(claim_sentences, f, indent=2)

print("Parsed drafts, output citation/writing audits, and dumped claims to extracted_claims.json.")
