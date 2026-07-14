import os
import re
import glob
import statistics

def get_sentences(text):
    # Remove code blocks and tables roughly
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'\|.*?\|', '', text)
    # split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def get_paragraphs(text):
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'\|.*?\|', '', text)
    paragraphs = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paragraphs if p.strip() and not p.startswith('#')]

phrases = [
    "It is important to note",
    "It should be noted",
    "It is worth mentioning",
    "plays a crucial role",
    "has gained significant attention",
    "in recent years",
    "increasingly popular",
    "comprehensive study",
    "extensive experiments",
    "state-of-the-art"
]

files = glob.glob('draft_en/*.md')
files.sort()

report = []
report.append("# AI Pattern Check Report")
report.append("")

for f in files:
    if f.endswith('ai_pattern_check.md'): continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    report.append(f"## File: {f}")
    
    # Phrase check
    found_phrases = []
    for p in phrases:
        if p.lower() in content.lower():
            found_phrases.append(p)
    if found_phrases:
        report.append(f"- **Phrases found**: {', '.join(found_phrases)}")
    else:
        report.append("- **Phrases found**: None")
        
    # Sentence length
    sentences = get_sentences(content)
    lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
    if len(lengths) > 1:
        stdev = statistics.stdev(lengths)
        report.append(f"- **Sentence length std dev**: {stdev:.2f} words (mean: {statistics.mean(lengths):.2f})")
    else:
        report.append("- **Sentence length std dev**: N/A (too few sentences)")
        
    # Paragraph openings
    paragraphs = get_paragraphs(content)
    openings = [ " ".join(re.findall(r'\b\w+\b', p)[:3]).lower() for p in paragraphs ]
    from collections import Counter
    c = Counter(openings)
    most_common = c.most_common(1)
    if most_common and paragraphs:
        pct = (most_common[0][1] / len(paragraphs)) * 100
        report.append(f"- **Most common paragraph opening**: '{most_common[0][0]}' ({pct:.1f}%)")
    
    report.append("")

with open('draft_en/ai_pattern_check.md', 'w', encoding='utf-8') as out:
    out.write("\n".join(report))
print("Done")
