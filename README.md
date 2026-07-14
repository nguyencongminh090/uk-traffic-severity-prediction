# Evaluating Spatial Feature Engineering in CatBoost for UK Traffic Accident Severity Prediction

> **Status:** Manuscript submitted · Springer LLNCS format · 12 pages

---

## Abstract

Traffic accidents remain a severe public safety challenge. Predicting accident severity helps authorities deploy timely interventions. While standard machine learning models effectively use administrative and environmental variables, integrating explicit spatial data remains challenging due to sparsity and dimensionality. This study develops a CatBoost framework evaluating the impact of explicit spatial features—KMeans coordinate clusters and distances to major cities—on predicting traffic fatalities in the United Kingdom.

Using a balanced dataset of **289,444 records**, we establish a baseline across five classification algorithms, with CatBoost achieving the highest ROC-AUC of **0.8132**. Subsequent ablation experiments reveal that injecting engineered spatial features yields **no statistically significant performance gain** (ROC-AUC 0.8136, *p* = 0.7644). We attribute this null result to severe coordinate sparsity (54% missing data) and the overlapping spatial proxy signals already embedded in standard administrative variables such as speed limits and police force zones.

**Keywords:** Traffic Accident Severity · Spatial Feature Engineering · CatBoost · Gradient Boosting · Class Imbalance · Machine Learning

---

## Research Questions

1. Do gradient boosting ensemble methods (CatBoost, XGBoost, LightGBM) outperform classical algorithms (Logistic Regression, Random Forest) on large-scale UK collision data?
2. Does integrating explicit spatial features—specifically KMeans coordinate clustering and Haversine distances to major cities—yield a statistically significant improvement in CatBoost's ability to predict traffic fatalities?

---

## Key Findings

| Finding | Result |
|---|---|
| Best baseline model | CatBoost (ROC-AUC = **0.8132**, Accuracy = **73.60%**) |
| Spatial feature impact (ROC-AUC) | 0.8132 → 0.8136 (+0.0004) |
| McNemar's test *p*-value | **0.7644** (not significant, α = 0.05) |
| Paired t-test on CV ROC-AUC | *p* = 0.3099 (not significant) |
| Coordinate missing rate | **54%** — primary cause of null spatial signal |
| Training time overhead (spatial) | 41.88s → 279.67s (**+568%** for negligible gain) |

> **Key Negative Result:** Spatial feature engineering provides **redundant information** when administrative variables (speed limit, police force, urban/rural area) already act as efficient geographic proxies, and when raw coordinate data is heavily incomplete.

---

## Repository Structure

```
uk-traffic-accidents-catboost/
│
├── paper.tex                  # Main LaTeX manuscript (Springer LLNCS)
├── references.bib             # BibTeX bibliography (24 references)
├── llncs.cls                  # Springer LLNCS document class
│
├── figures/
│   ├── fig01_spatial_clusters.pdf      # KMeans spatial cluster visualization
│   ├── fig02_performance_metrics.pdf   # ROC curve, Precision-Recall, Confusion Matrix
│   ├── fig03_feature_importance.pdf    # Top-20 CatBoost feature importances
│   └── fig04_shap_summary.pdf          # SHAP summary plot
│
├── UK_accidents.ipynb         # Main experimental notebook (full pipeline)
├── UK_accidents_local.ipynb   # Local execution variant
│
├── generate_tex.py            # Script: auto-generate LaTeX tables and figures
├── generate_figures.py        # Script: reproduce all paper figures
│
├── .agents/                   # Academic pipeline agents (ARS workflow)
├── .gitignore
└── README.md
```

---

## Methodology

### 1. Dataset

- **Source:** United Kingdom traffic accident records (`UK_accidents_balanced.csv`)
- **Size:** 289,444 samples · 44 features
- **Target variable:** Binary — `Fatal` (1) vs. `Non-Fatal` (0)
  - Original tri-class label (`Fatal / Serious / Slight`) collapsed: *Serious + Slight → Non-Fatal*
- **Class balance:** Perfectly balanced — 144,722 Fatal / 144,722 Non-Fatal
- **Train/Test split:** 80:20 stratified split → 231,555 training · 57,889 test samples

### 2. Preprocessing

| Step | Method |
|---|---|
| Leak removal | Dropped `enhanced_severity_collision`, `collision_injury_based`, `collision_index` |
| Numerical imputation | Median imputation |
| Categorical imputation | Sentinel label `"missing"` + label encoding |
| Coordinate handling | Sentinel value `−1` for 54% missing entries |

### 3. Spatial Feature Engineering

Five spatial features were engineered from latitude/longitude coordinates:

| Feature | Description |
|---|---|
| `spatial_cluster` | KMeans cluster assignment (*k* = 20); fitted on training set only |
| `grid_region_id` | Static 0.5° × 0.5° latitude/longitude grid mapping |
| `cluster_density` | Proportion of training samples per spatial cluster (traffic density proxy) |
| `dist_to_nearest_city_km` | Haversine distance to the nearest of 8 major UK cities |
| `nearest_city_zone` | Metropolitan zone identifier for the nearest city |

> **Note:** KMeans was fitted exclusively on training coordinates to prevent data leakage into the test set.

### 4. Models Evaluated

| Model | Type | Notes |
|---|---|---|
| Logistic Regression | Linear | Baseline linear classifier |
| Random Forest | Ensemble (Bagging) | 100 trees |
| XGBoost | Gradient Boosting | Chen & Guestrin (2016) |
| LightGBM | Gradient Boosting | Ke et al. (2017) |
| **CatBoost** | Gradient Boosting | Primary model — native categorical feature handling via ordered boosting |

CatBoost was selected as the primary framework due to its native support for high-cardinality categorical variables, using target statistics (ordered boosting) rather than naive label encoding.

### 5. Training Protocol

- **Validation split:** 15% of training set for early stopping
- **Early stopping:** 50-round patience threshold
- **Hyperparameter tuning:** Grid search over `depth`, `learning_rate`, `l2_leaf_reg`
- **Cross-validation:** 5-fold CV on CatBoost baseline for stability verification

### 6. Evaluation Metrics

- **Accuracy** — Overall classification rate
- **Precision / Recall / F1-Macro** — Per-class and macro-averaged
- **ROC-AUC** — Primary discriminative metric
- **McNemar's test** — Statistical significance of pairwise model comparison
- **Training / Inference time** — Computational cost analysis

---

## Results

### Baseline Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Time (s) |
|---|---|---|---|---|---|---|
| **CatBoost** | **0.7360** | 0.7271 | 0.7555 | 0.7410 | **0.8132** | 41.88 |
| XGBoost | 0.7358 | 0.7277 | 0.7537 | 0.7404 | 0.8130 | 16.48 |
| LightGBM | 0.7351 | 0.7262 | 0.7546 | 0.7401 | 0.8124 | 14.30 |
| Random Forest | 0.7300 | 0.7220 | 0.7480 | 0.7348 | 0.8066 | 121.81 |
| Logistic Regression | 0.6752 | 0.6834 | 0.6526 | 0.6677 | 0.7368 | 302.01 |

CatBoost 5-fold CV: mean ROC-AUC = **0.8119 ± 0.0019**

### CatBoost Ablation Study

| Configuration | Accuracy | F1-Score | ROC-AUC | Time (s) |
|---|---|---|---|---|
| 1. Baseline CatBoost | 0.7360 | 0.7410 | 0.8132 | 41.88 |
| 2. CatBoost + Spatial Features | 0.7350 | 0.7400 | 0.8132 | 169.05 |
| 3. Final Improved CatBoost | 0.7362 | 0.7410 | **0.8136** | 279.67 |

**Statistical Tests:**
- McNemar's χ² = 0.0898 → *p* = **0.7644** (not significant)
- Paired t-test on CV ROC-AUC → *p* = **0.3099** (not significant)

### Feature Importance

Top predictors by native CatBoost importance: `number_of_vehicles`, `number_of_casualties`, `speed_limit`. Engineered spatial features (`spatial_cluster`, `dist_to_nearest_city_km`) ranked substantially lower, consistent with the null effect finding.

---

## Discussion

The null result stems from two compounding data realities:

1. **Coordinate Sparsity (54%):** With more than half of geographic records absent and masked by a sentinel value, the spatial signal becomes severely diluted. The model effectively learns to ignore spatial cluster assignments that are absent for the majority of training examples.

2. **Administrative Variable Collinearity:** Features such as `police_force`, `urban_or_rural_area`, and `speed_limit` already encode geographic context at high resolution. A decision tree splitting on a 70-mph rural road governed by a specific regional police force has effectively localized the accident without requiring explicit coordinates. Injecting engineered spatial features introduces **redundant information** into an already well-specified feature space.

**Practical Implication:** Researchers should audit coordinate completeness *before* investing computational resources in Haversine distance calculations or KMeans spatial clustering. If coordinate missingness exceeds ~50%, standard administrative descriptors will provide an equivalent—and far more efficient—spatial proxy.

---

## Reproducing the Paper

### Prerequisites

- Python 3.9+
- TeX Live 2023+ (or any distribution with `pdflatex` and `splncs04.bst`)
- Jupyter Notebook / JupyterLab

### Python Dependencies

```bash
pip install pandas numpy scikit-learn catboost xgboost lightgbm matplotlib seaborn shap jupyter
```

### Data Setup

Place the preprocessed dataset in the working directory:
```
UK_accidents_balanced.csv   # 289,444 rows × 44 columns
```

> The raw dataset is not included in this repository. See the [UK Government Road Safety Data](https://www.data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-safety-data) for the source.

### Running the Experiment

```bash
# Full experimental pipeline
jupyter notebook UK_accidents.ipynb

# Reproduce figures
python generate_figures.py

# Regenerate LaTeX tables
python generate_tex.py
```

### Compiling the Manuscript

```bash
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex       # second pass for cross-references
```

Output: `paper.pdf` (12 pages, Springer LLNCS format)

---

## Citation

If you use this work, please cite:

```bibtex
@inproceedings{anonymous2026spatial,
  author    = {Anonymous Author(s)},
  title     = {Evaluating Spatial Feature Engineering in CatBoost for UK Traffic Accident Severity Prediction},
  booktitle = {Lecture Notes in Computer Science},
  publisher = {Springer},
  year      = {2026},
}
```

---

## References

Key references underpinning this work:

- Prokhorenkova et al. (2017) — *CatBoost: unbiased boosting with categorical features*. arXiv:1706.09516
- Chen & Guestrin (2016) — *XGBoost*. KDD 2016
- Ke et al. (2017) — *LightGBM: A Highly Efficient Gradient Boosting Decision Tree*. NeurIPS 2017
- Chawla et al. (2002) — *SMOTE: Synthetic Minority Over-sampling Technique*. JAIR
- Kazmi et al. (2020) — *Spatiotemporal Clustering and Analysis of Road Accident Hotspots*. The Computer Journal

Full bibliography: [`references.bib`](references.bib) (24 entries)

---

## License

This repository contains the manuscript source and reproduction scripts for a research paper under academic submission. Please contact the authors before reusing any portion of this work.
