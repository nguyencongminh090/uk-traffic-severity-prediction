# Audit Summary & Action Items

This document consolidates all findings from the Phase 8 Quality Audit (8A–8E) into a prioritized action list.

## 🔴 CRITICAL (Must fix before any further work)

### 1. Fabricated Models in Results
- **Location**: `04_experiments_results.md` (Table 1 and surrounding text)
- **Issue**: The draft reports training 9 models (including Extra Trees, AdaBoost, Decision Tree, and Gradient Boosting).
- **Ground Truth**: The Jupyter Notebook (`UK_accidents.ipynb`) only trained 5 models (Logistic Regression, Random Forest, XGBoost, LightGBM, CatBoost).
- **Fix Required**: Remove the 4 fabricated models from Table 1 and update any text comparing "nine baseline models" to "five baseline models".
- **Source Finding**: 8E-Finding#1, 8C-Inconsistency#1

### 2. Unsupported Claims in Claim Alignment
- **Location**: `04_experiments_results.md`
- **Issue**: Performance metrics for the 4 fabricated models have no source in the notebook outputs.
- **Fix Required**: Removing the models (per Critical #1) will resolve this.
- **Source Finding**: 8A-Claim-Alignment

## 🟡 MAJOR (Should fix before LaTeX conversion)

### 3. Novel Fact Introduced in Conclusion
- **Location**: `06_conclusion.md` (mentions "Extensive missing coordinate data (54%)")
- **Issue**: While true (verified against the notebook's missing value plot), this specific statistic is never introduced in the Methodology or Data sections.
- **Fix Required**: Add a sentence to the Methodology (Data Preprocessing) section establishing the 54% missing rate for spatial coordinates, so the Conclusion does not introduce novel evidence.
- **Source Finding**: 8C-Inconsistency#2

## 🟢 MINOR (Nice to fix)

### 4. Citation Ordering
- **Location**: `02_related_work.md`
- **Issue**: Citations appear out of numerical sequence (e.g., `[3]`, then `[18, 20, 23]`, then `[16]`). This occurred because the `.bib` was sorted alphabetically. While acceptable in many styles, LLNCS `splncs04` can handle this, but some reviewers prefer sequential appearance.
- **Fix Required**: No strict fix required if relying on `splncs04` default alphabetical sorting, but monitor for LaTeX formatting warnings.
- **Source Finding**: 8B-Citation Integrity

### 5. AI Filler Phrases
- **Location**: `02_related_work.md`
- **Issue**: Phrases like "remains a core challenge in transportation safety research."
- **Fix Required**: Keep as-is since it is cited properly, but be cautious of adding more unanchored fluff during revisions.
- **Source Finding**: 8E-Finding#2
