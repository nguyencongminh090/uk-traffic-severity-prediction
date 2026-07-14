import urllib.request
import urllib.parse
import json
import time

queries = [
    "traffic accident severity prediction machine learning",
    "UK road accidents severity classification",
    "gradient boosting traffic severity",
    "CatBoost tabular data classification",
    "spatial feature engineering traffic accidents clustering",
    "class imbalance traffic severity SMOTE"
]

all_results = []
seen_ids = set()

fields = "title,authors,year,externalIds,venue,publicationDate,abstract,citationCount,url"

def fetch_with_retry(url):
    retries = 3
    for i in range(retries):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"429 Rate limit, backing off for {5 * (i+1)}s...")
                time.sleep(5 * (i+1))
            else:
                print(f"HTTP Error {e.code}: {e.reason}")
                break
        except Exception as e:
            print(f"Error: {e}")
            break
    return None

for q in queries:
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(q)}&limit=15&fields={fields}&year=2015-2026"
    print(f"Searching: {q}")
    data = fetch_with_retry(url)
    if data and 'data' in data:
        for paper in data['data']:
            pid = paper.get('paperId')
            if pid and pid not in seen_ids:
                seen_ids.add(pid)
                paper['search_query'] = q
                all_results.append(paper)
    time.sleep(3) # safe delay

# Fetch some foundational papers (e.g. original CatBoost paper, SMOTE, XGBoost)
foundational_queries = [
    ("CatBoost: unbiased boosting with categorical features", "CatBoost foundational"),
    ("XGBoost: A Scalable Tree Boosting System", "XGBoost foundational"),
    ("LightGBM: A Highly Efficient Gradient Boosting Decision Tree", "LightGBM foundational"),
    ("SMOTE: Synthetic Minority Over-sampling Technique", "SMOTE foundational")
]

for q, label in foundational_queries:
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(q)}&limit=1&fields={fields}"
    print(f"Searching foundational: {q}")
    data = fetch_with_retry(url)
    if data and 'data' in data and len(data['data']) > 0:
        paper = data['data'][0]
        pid = paper.get('paperId')
        if pid and pid not in seen_ids:
            seen_ids.add(pid)
            paper['search_query'] = label
            all_results.append(paper)
    time.sleep(3)

with open('candidates.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, indent=2)

print(f"Saved {len(all_results)} candidates to candidates.json")
