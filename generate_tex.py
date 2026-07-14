import re
import os

# Read references.bib
with open("references.bib", "r") as f:
    bib_content = f.read()

# Parse bib items
entries = []
current_entry = {}
lines = bib_content.split('\n')
for line in lines:
    line = line.strip()
    if line.startswith('@'):
        if current_entry:
            entries.append(current_entry)
        match = re.match(r'@(\w+)\{([^,]+),', line)
        if match:
            current_entry = {'type': match.group(1), 'id': match.group(2)}
    elif '=' in line and current_entry:
        key, val = line.split('=', 1)
        key = key.strip()
        val = val.strip().strip('{},')
        current_entry[key] = val
if current_entry:
    entries.append(current_entry)

# Sort entries alphabetically by ID (which is authorYear)
entries.sort(key=lambda x: x['id'])

bib_str = "\\begin{thebibliography}{8}\n"
for i, entry in enumerate(entries):
    bib_str += f"\\bibitem{{{entry['id']}}}\n"
    author = entry.get('author', '').replace(' and ', ', ')
    title = entry.get('title', '')
    journal = entry.get('journal', entry.get('booktitle', ''))
    year = entry.get('year', '')
    doi = entry.get('doi', '')
    
    bib_str += f"{author}: {title}. \\textit{{{journal}}}. {year}."
    if doi:
        bib_str += f" \\doi{{{doi}}}"
    bib_str += "\n\n"

bib_str += "\\end{thebibliography}\n"

# Read markdown files
md_files = [
    "draft_en/01_introduction.md",
    "draft_en/02_related_work.md",
    "draft_en/03_methodology.md",
    "draft_en/04_experiments_results.md",
    "draft_en/05_discussion.md",
    "draft_en/06_conclusion.md"
]

tex_content = r"""\documentclass[runningheads]{llncs}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath,amssymb}
\usepackage{hyperref}
\usepackage{tabularx}

\begin{document}

\title{Evaluating Spatial Feature Engineering in CatBoost for UK Traffic Accident Severity Prediction}
\author{Anonymous Author(s)}
\institute{Anonymous Institute}
\maketitle

\begin{abstract}
Traffic accidents remain a severe public safety challenge. Predicting accident severity helps authorities deploy timely interventions. While standard machine learning models effectively use administrative and environmental variables, integrating explicit spatial data remains challenging due to sparsity and dimensionality. This study develops a CatBoost framework evaluating the impact of explicit spatial features---KMeans coordinate clusters and distances to major cities---on predicting traffic fatalities in the United Kingdom. Using a balanced dataset of 289,444 records, we establish a baseline across multiple classification algorithms, with CatBoost achieving the highest ROC-AUC of 0.8132. Subsequent ablation experiments reveal that injecting engineered spatial features yields no statistically significant performance gain (ROC-AUC 0.8136, $p=0.7644$). We attribute this to severe coordinate sparsity (54\% missing data) and the overlapping spatial proxy signals already present in standard administrative variables such as speed limits and police zones. The results suggest that for traffic datasets with extensive missing coordinates, complex spatial feature engineering provides redundant information.
\keywords{Traffic Accident Severity \and Spatial Feature Engineering \and CatBoost \and Machine Learning \and Imbalanced Data}
\end{abstract}

"""

def convert_md_to_tex(md_text):
    # Headings
    md_text = re.sub(r'^#\s+\d+\.\s+(.*)', r'\\section{\1}', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^##\s+\d+\.\d+\.\s+(.*)', r'\\subsection{\1}', md_text, flags=re.MULTILINE)
    
    # Bold
    md_text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', md_text)
    
    # Inline code
    md_text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', md_text)
    
    # Citations
    def replace_citation(m):
        nums = [int(x.strip()) for x in m.group(1).split(',')]
        ids = [entries[num-1]['id'] for num in nums]
        return r'\cite{' + ','.join(ids) + '}'
    
    md_text = re.sub(r'\[(\d+(?:,\s*\d+)*)\]', replace_citation, md_text)
    
    return md_text

for f in md_files:
    with open(f, "r") as file:
        md_text = file.read()
        tex_content += convert_md_to_tex(md_text) + "\n\n"

# Replace tables
table1 = r"""\begin{table}[ht]
\centering
\caption{Baseline model performance comparison}
\label{tab:baseline}
\begin{tabular}{lcccccc}
\toprule
\textbf{Model} & \textbf{Accuracy} & \textbf{Precision} & \textbf{Recall} & \textbf{F1-Score} & \textbf{ROC-AUC} & \textbf{Time (s)} \\
\midrule
CatBoost & 0.7360 & 0.7271 & 0.7555 & 0.7410 & 0.8132 & 41.88 \\
XGBoost & 0.7358 & 0.7277 & 0.7537 & 0.7404 & 0.8130 & 16.48 \\
LightGBM & 0.7351 & 0.7262 & 0.7546 & 0.7401 & 0.8124 & 14.30 \\
Random Forest & 0.7300 & 0.7220 & 0.7480 & 0.7348 & 0.8066 & 121.81 \\
Logistic Regression & 0.6752 & 0.6834 & 0.6526 & 0.6677 & 0.7368 & 302.01 \\
\bottomrule
\end{tabular}
\end{table}"""

table2 = r"""\begin{table}[ht]
\centering
\caption{CatBoost ablation study}
\label{tab:ablation}
\begin{tabular}{lcccccc}
\toprule
\textbf{Model} & \textbf{Accuracy} & \textbf{Precision} & \textbf{Recall} & \textbf{F1-Score} & \textbf{ROC-AUC} & \textbf{Time (s)} \\
\midrule
1. Baseline CatBoost & 0.7360 & 0.7271 & 0.7555 & 0.7410 & 0.8132 & 41.88 \\
2. CatBoost + Spatial Features & 0.7350 & 0.7262 & 0.7542 & 0.7400 & 0.8132 & 169.05 \\
3. Final Improved CatBoost & 0.7362 & 0.7278 & 0.7547 & 0.7410 & 0.8136 & 279.67 \\
\bottomrule
\end{tabular}
\end{table}"""

# Remove markdown tables and insert LaTeX tables
tex_content = re.sub(r'\*\*Table 1.*?\n\|---\|.*?\n\| Logistic Regression.*?\|', table1.replace('\\', '\\\\'), tex_content, flags=re.DOTALL)
tex_content = re.sub(r'\*\*Table 2.*?\n\|---\|.*?\n\| 3\. Final Improved CatBoost.*?\|', table2.replace('\\', '\\\\'), tex_content, flags=re.DOTALL)

# Handle python code block
code_block = r"""\begin{verbatim}
# Target variable preprocessing
df_model[TARGET] = df_model[TARGET].replace({2: 0, 3: 0})

# Train and test set partitioning
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)
\end{verbatim}"""
tex_content = re.sub(r'```python.*?```', code_block.replace('\\', '\\\\'), tex_content, flags=re.DOTALL)

# Handle bullet points
def convert_bullets(match):
    items = match.group(0).strip().split('\n')
    out = "\\begin{itemize}\n"
    for item in items:
        if item.startswith('- '):
            out += f"\\item {item[2:]}\n"
    out += "\\end{itemize}"
    return out

tex_content = re.sub(r'(?:^- .*?(?:\n|$)){2,}', convert_bullets, tex_content, flags=re.MULTILINE)

# Append figures placeholder as requested by the plan
figures = r"""
\begin{figure}[ht]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/fig01_spatial_clusters.pdf}
    \caption{\textit{Distribution of Spatial Clusters Across the UK.} Scatter plot mapping the 20 clusters derived via KMeans clustering on available geographic coordinates ($k=20$). Missing coordinates were excluded from this clustering process.}
    \label{fig:fig01}
\end{figure}

\begin{figure}[ht]
    \centering
    \includegraphics[width=0.9\textwidth]{figures/fig02_performance_metrics.pdf}
    \caption{\textit{Performance Comparison of Baseline and Final Improved CatBoost Models.} The panels display the Receiver Operating Characteristic (ROC) curve (left), Precision-Recall curve (center), and the Confusion Matrix for the Final Improved CatBoost (right). Minor improvements are visible in the ROC AUC, though not statistically significant.}
    \label{fig:fig02}
\end{figure}

\begin{figure}[ht]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/fig03_feature_importance.pdf}
    \caption{\textit{Top 20 Features by Native CatBoost Importance.} Feature importance scores for the Final Improved CatBoost model, highlighting the dominance of variables such as number of vehicles, number of casualties, and speed limit. Engineered spatial features contribute relatively little to the model's predictive power.}
    \label{fig:fig03}
\end{figure}

\begin{figure}[ht]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/fig04_shap_summary.pdf}
    \caption{\textit{SHAP Summary Plot for the Final Improved CatBoost.} The plot illustrates the directional impact of features on crash severity prediction. Each dot represents a single prediction; color indicates the feature's value (e.g., higher values in red), while horizontal position shows the impact on the model output (SHAP value).}
    \label{fig:fig04}
\end{figure}
"""

# Insert figures before discussion
tex_content = tex_content.replace("\\section{Discussion}", figures + "\n\\section{Discussion}")


tex_content += bib_str
tex_content += r"\end{document}"

with open("paper.tex", "w") as f:
    f.write(tex_content)
