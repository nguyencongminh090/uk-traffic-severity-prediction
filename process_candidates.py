import json
import re

with open('candidates_openalex.json', 'r', encoding='utf-8') as f:
    candidates = json.load(f)

# Deduplicate
seen_titles = set()
unique_cands = []
for c in candidates:
    if not c.get('title'):
        continue
    norm_title = re.sub(r'[^a-z0-9]', '', c['title'].lower())
    if norm_title not in seen_titles:
        seen_titles.add(norm_title)
        unique_cands.append(c)

# Scoring
def score_paper(c):
    score = 0
    title = (c.get('title') or "").lower()
    abstract = (c.get('abstract') or "").lower()
    query = (c.get('search_query') or "").lower()
    year = c.get('year') or 0
    citations = c.get('citationCount') or 0
    
    if "foundational" in query:
        return 1000 + citations # Foundational always top

    # Relevance points
    if "traffic" in title or "accident" in title or "crash" in title: score += 10
    if "severit" in title: score += 10
    if "catboost" in title or "xgboost" in title or "lightgbm" in title or "gradient boosting" in title: score += 10
    if "spatial" in title or "cluster" in title or "geographic" in title: score += 10
    if "imbalance" in title or "smote" in title: score += 10
    
    # Keyword points in abstract
    if "catboost" in abstract: score += 5
    if "spatial" in abstract or "uk" in abstract: score += 5
    if "imbalance" in abstract: score += 5
    
    # Recency
    if year >= 2023: score += 5
    elif year >= 2020: score += 2
    
    # Citations
    score += min(citations, 50) / 10.0
    return score

unique_cands.sort(key=score_paper, reverse=True)

# Select top 35 candidates
top_35 = unique_cands[:35]

def assign_section_and_relevance(c):
    title = (c.get('title') or "").lower()
    abstract = (c.get('abstract') or "").lower()
    query = (c.get('search_query') or "").lower()
    
    if "foundational" in query:
        return "High", "Foundational methodology paper.", "Methodology / Gradient Boosting and Ensemble Methods"
    
    relevance = "Medium"
    justification = "Relevant to traffic severity prediction."
    section = "Traffic Accident Severity Prediction"
    
    if "catboost" in title or "xgboost" in title:
        relevance = "High"
        justification = "Directly uses target boosting methods for comparison."
        section = "Gradient Boosting and Ensemble Methods for Tabular Data"
    elif "spatial" in title or "geograph" in title:
        relevance = "High"
        justification = "Provides context on spatial feature engineering."
        section = "Spatial Feature Engineering in Predictive Modeling"
    elif "imbalance" in title or "smote" in title:
        relevance = "High"
        justification = "Addresses class imbalance, highly relevant to our data preprocessing."
        section = "Handling Class Imbalance in Traffic Analysis"
    elif "uk" in title:
        relevance = "High"
        justification = "Analyzes UK traffic data, providing direct domain context."
        section = "Traffic Accident Severity Prediction (Domain Context)"
        
    return relevance, justification, section

cand_md = ["# Literature Candidates (Phase 7A)\n"]
for i, c in enumerate(top_35):
    rel, just, sec = assign_section_and_relevance(c)
    c['_relevance'] = rel
    c['_justification'] = just
    c['_section'] = sec
    
    authors = ", ".join(c.get('authors', [])[:3]) + (" et al." if len(c.get('authors', []))>3 else "")
    doi = c.get('doi') or "N/A"
    
    cand_md.append(f"### [{i+1}] {c['title']}")
    cand_md.append(f"- **Authors**: {authors}")
    cand_md.append(f"- **Year**: {c['year']}")
    cand_md.append(f"- **Venue**: {c.get('venue') or 'N/A'}")
    cand_md.append(f"- **DOI**: {doi}")
    cand_md.append(f"- **Relevance**: {rel} - {just}")
    cand_md.append(f"- **Target Section**: {sec}")
    cand_md.append(f"- **Search Query**: {c.get('search_query')}")
    cand_md.append("")

with open('draft_en/literature_candidates.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(cand_md))

# Select 25 from the 35 to form the final list, ensuring distribution
final_25 = []
# Ensure foundationals are in
for c in top_35:
    if "foundational" in c.get('search_query', '').lower():
        final_25.append(c)
# Fill the rest with the highest scored ones
for c in top_35:
    if len(final_25) >= 25:
        break
    if c not in final_25:
        final_25.append(c)

sel_md = ["# Literature Selection (Phase 7B)\n"]
for i, c in enumerate(final_25):
    authors = ", ".join(c.get('authors', [])[:3]) + (" et al." if len(c.get('authors', []))>3 else "")
    sel_md.append(f"### [{i+1}] {c['title']}")
    sel_md.append(f"- **Authors**: {authors}")
    sel_md.append(f"- **Year**: {c['year']}")
    sel_md.append(f"- **Category/Section**: {c['_section']}")
    sel_md.append(f"- **DOI**: {c.get('doi') or 'N/A'}")
    sel_md.append(f"- **Rationale**: {c['_justification']}")
    sel_md.append("")

with open('draft_en/literature_selection.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(sel_md))

with open('selected_papers.json', 'w', encoding='utf-8') as f:
    json.dump(final_25, f, indent=2)

print(f"Written candidates ({len(top_35)}) and selected ({len(final_25)}).")
