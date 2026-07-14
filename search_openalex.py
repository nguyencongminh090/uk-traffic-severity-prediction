import urllib.request
import urllib.parse
import json
import time

def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return ""
    try:
        max_idx = max(idx for indices in inverted_index.values() for idx in indices)
        words = [""] * (max_idx + 1)
        for word, indices in inverted_index.items():
            for idx in indices:
                words[idx] = word
        return " ".join(words)
    except:
        return ""

queries = [
    "traffic accident severity prediction machine learning",
    "UK road accidents severity classification",
    "gradient boosting traffic severity",
    "CatBoost tabular classification",
    "spatial feature engineering traffic accidents",
    "class imbalance traffic severity SMOTE"
]

foundational_queries = [
    ("CatBoost: unbiased boosting with categorical features", "CatBoost foundational"),
    ("XGBoost: A Scalable Tree Boosting System", "XGBoost foundational"),
    ("LightGBM: A Highly Efficient Gradient Boosting Decision Tree", "LightGBM foundational"),
    ("SMOTE: Synthetic Minority Over-sampling Technique", "SMOTE foundational")
]

all_results = []
seen_ids = set()

def fetch_openalex(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:ngmint@example.com'})
    retries = 3
    for i in range(retries):
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"429 Rate limit, backing off for {2 * (i+1)}s...")
                time.sleep(2 * (i+1))
            else:
                print(f"HTTP Error {e.code}: {e.reason}")
                break
        except Exception as e:
            print(f"Error: {e}")
            break
    return None

for q in queries:
    # Filter by year 2015-2026
    url = f"https://api.openalex.org/works?search={urllib.parse.quote(q)}&filter=publication_year:2015-2026&per-page=15&mailto=ngmint@example.com"
    print(f"Searching: {q}")
    data = fetch_openalex(url)
    if data and 'results' in data:
        for paper in data['results']:
            pid = paper.get('id')
            if pid and pid not in seen_ids:
                seen_ids.add(pid)
                # reformat to match our expected structure
                authors = [a['author']['display_name'] for a in paper.get('authorships', []) if 'author' in a]
                venue = paper.get('primary_location', {}).get('source', {}).get('display_name') if paper.get('primary_location') and paper['primary_location'].get('source') else None
                all_results.append({
                    "title": paper.get('title'),
                    "authors": authors,
                    "year": paper.get('publication_year'),
                    "venue": venue,
                    "doi": paper.get('doi'),
                    "abstract": reconstruct_abstract(paper.get('abstract_inverted_index')),
                    "citationCount": paper.get('cited_by_count'),
                    "search_query": q,
                    "source": "OpenAlex"
                })
    time.sleep(0.2) # Polite pool rate limit is 10/s

for q, label in foundational_queries:
    url = f"https://api.openalex.org/works?search={urllib.parse.quote(q)}&per-page=3&mailto=ngmint@example.com"
    print(f"Searching foundational: {q}")
    data = fetch_openalex(url)
    if data and 'results' in data and len(data['results']) > 0:
        paper = data['results'][0]
        pid = paper.get('id')
        if pid and pid not in seen_ids:
            seen_ids.add(pid)
            authors = [a['author']['display_name'] for a in paper.get('authorships', []) if 'author' in a]
            venue = paper.get('primary_location', {}).get('source', {}).get('display_name') if paper.get('primary_location') and paper['primary_location'].get('source') else None
            all_results.append({
                "title": paper.get('title'),
                "authors": authors,
                "year": paper.get('publication_year'),
                "venue": venue,
                "doi": paper.get('doi'),
                "abstract": reconstruct_abstract(paper.get('abstract_inverted_index')),
                "citationCount": paper.get('cited_by_count'),
                "search_query": label,
                "source": "OpenAlex"
            })
    time.sleep(0.2)

with open('candidates_openalex.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, indent=2)

print(f"Saved {len(all_results)} candidates to candidates_openalex.json")
