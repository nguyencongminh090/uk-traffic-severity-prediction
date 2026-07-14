# Figure Plan

Based on the visualization standards and the data output from `UK_accidents.ipynb`, the following 4 figures have been selected for inclusion in the paper.

## 1. Spatial Clusters Map
- **Source Code**: Notebook cell #7 ("Spatial Clusters (KMeans, k=20) — Training Records")
- **Type**: Scatter plot (spatial map approximation)
- **Content**: Shows the 20 KMeans spatial clusters formed by latitude and longitude.
- **Section**: 3. Methodology (specifically 3.2. Spatial Feature Engineering)
- **Filename**: `figures/fig01_spatial_clusters.pdf`
- **Quality Assessment**: Needs formatting to remove the default `tab20` categorical palette (which violates colorblind safety standards) and replace it with an accessible discrete palette or viridis for density.
- **Caption**: \caption{\textit{Distribution of Spatial Clusters Across the UK.} Scatter plot mapping the 20 clusters derived via KMeans clustering on available geographic coordinates ($k=20$). Missing coordinates were excluded from this clustering process.}

## 2. Model Performance Metrics (ROC, PR, Confusion Matrix)
- **Source Code**: Notebook cell #4-6 ("ROC Curve, Precision-Recall Curve, Confusion Matrix — Baseline vs Final model")
- **Type**: Multi-panel plot (3 subplots)
- **Content**: ROC curves, Precision-Recall curves, and Confusion matrix comparing the baseline CatBoost against the final improved model.
- **Section**: 4. Experiments and Results
- **Filename**: `figures/fig02_performance_metrics.pdf`
- **Quality Assessment**: The baseline vs. improved ROC curves are excellent for visual comparison, but the subplots should be styled consistently (APA 7.0) with a colorblind-safe categorical palette (e.g., Tol's palette) instead of default Matplotlib colors.
- **Caption**: \caption{\textit{Performance Comparison of Baseline and Final Improved CatBoost Models.} The panels display the Receiver Operating Characteristic (ROC) curve (left), Precision-Recall curve (center), and the Confusion Matrix for the Final Improved CatBoost (right). Minor improvements are visible in the ROC AUC, though not statistically significant.}

## 3. Global Feature Importance
- **Source Code**: Notebook cell #1 ("Final Improved CatBoost — Top 20 Feature Importances")
- **Type**: Horizontal bar chart
- **Content**: Ranks the top 20 features by native CatBoost importance.
- **Section**: 4. Experiments and Results
- **Filename**: `figures/fig03_feature_importance.pdf`
- **Quality Assessment**: Needs a flat 2D style, standard APA typography, and a single solid color (e.g., `#0077BB` from the colorblind-safe palette) instead of "teal".
- **Caption**: \caption{\textit{Top 20 Features by Native CatBoost Importance.} Feature importance scores for the Final Improved CatBoost model, highlighting the dominance of variables such as number of vehicles, number of casualties, and speed limit. Engineered spatial features contribute relatively little to the model's predictive power.}

## 4. SHAP Value Summary
- **Source Code**: Notebook cell #2 ("SHAP Summary")
- **Type**: SHAP summary dot plot
- **Content**: Shows the directional impact of each feature on the model's prediction (e.g., higher speed limit increases fatal probability).
- **Section**: 5. Discussion
- **Filename**: `figures/fig04_shap_summary.pdf`
- **Quality Assessment**: The default SHAP red-blue colormap is diverging and generally acceptable, but could be swapped for a strictly colorblind-safe diverging map if required by the publisher. It is highly informative for the Discussion.
- **Caption**: \caption{\textit{SHAP Summary Plot for the Final Improved CatBoost.} The plot illustrates the directional impact of features on crash severity prediction. Each dot represents a single prediction; color indicates the feature's value (e.g., higher values in red), while horizontal position shows the impact on the model output (SHAP value).}
