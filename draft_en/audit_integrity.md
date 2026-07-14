# Phase 8E: Integrity & Anti-Leakage Check

### Finding #1
- **File**: `04_experiments_results.md`
- **Issue**: Hallucinated Models
- **Evidence**: Table 1 lists 9 models: CatBoost, XGBoost, LightGBM, Gradient Boosting, Random Forest, Extra Trees, AdaBoost, Decision Tree, Logistic Regression.
- **Ground Truth**: The Jupyter Notebook (`UK_accidents.ipynb`) only trains 5 models: Logistic Regression, Random Forest, XGBoost, LightGBM, and CatBoost.
- **Severity**: 🔴 CRITICAL (Fabrication)
- **Action**: Delete rows corresponding to Gradient Boosting, Extra Trees, AdaBoost, and Decision Tree from Table 1. Re-calculate rankings if mentioned in text.

### Finding #2
- **File**: `02_related_work.md`
- **Issue**: Synthetic general knowledge phrases without citation
- **Evidence**: "Accurately predicting the severity of traffic collisions remains a core challenge in transportation safety research."
- **Ground Truth**: While true, this borders on AI-filler text. However, it is immediately followed by a citation `[3]`, making it acceptable as an intro sentence.
- **Severity**: 🟢 MINOR
- **Action**: Keep, but monitor for similar un-anchored filler.
