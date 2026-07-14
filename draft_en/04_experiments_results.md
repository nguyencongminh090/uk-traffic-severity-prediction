# 4. Experiments & Results

We executed a two-stage experimental pipeline: first benchmarking the five standard classifiers without spatial data, and then performing an ablation study on the CatBoost framework to isolate the impact of our engineered spatial features.

## 4.1. Baseline Model Performance

Table 1 details the predictive results of the five baseline models trained exclusively on the raw, non-spatial feature set.

**Table 1**: Baseline model performance comparison
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time (s) |
|---|---|---|---|---|---|---|
| CatBoost | 0.7360 | 0.7271 | 0.7555 | 0.7410 | 0.8132 | 41.88 |
| XGBoost | 0.7358 | 0.7277 | 0.7537 | 0.7404 | 0.8130 | 16.48 |
| LightGBM | 0.7351 | 0.7262 | 0.7546 | 0.7401 | 0.8124 | 14.30 |
| Random Forest | 0.7300 | 0.7220 | 0.7480 | 0.7348 | 0.8066 | 121.81 |
| Logistic Regression | 0.6752 | 0.6834 | 0.6526 | 0.6677 | 0.7368 | 302.01 |

The modern Gradient Boosted Decision Trees (CatBoost, XGBoost, and LightGBM) distinctly outperformed the linear Logistic Regression baseline, establishing a roughly 6% advantage in raw accuracy and an 0.08 margin in ROC-AUC. CatBoost secured the highest overall ranking with an ROC-AUC of 0.8132. 

To verify stability, we ran a 5-fold cross-validation routine on the CatBoost baseline. The model returned a mean ROC-AUC of 0.8119 with a tight standard deviation of ±0.0019.

## 4.2. Ablation Study

We then ran an ablation sequence to isolate what the spatial features actually added to the model. Table 2 presents three CatBoost variants: the raw baseline, a version injected with the new spatial features, and a finalized version that added specific hyperparameter tuning.

**Table 2**: CatBoost ablation study
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time (s) |
|---|---|---|---|---|---|---|
| 1. Baseline CatBoost | 0.7360 | 0.7271 | 0.7555 | 0.7410 | 0.8132 | 41.88 |
| 2. CatBoost + Spatial Features | 0.7350 | 0.7262 | 0.7542 | 0.7400 | 0.8132 | 169.05 |
| 3. Final Improved CatBoost | 0.7362 | 0.7278 | 0.7547 | 0.7410 | 0.8136 | 279.67 |

We expected the spatial data to push the model's predictive boundary. Instead, the metrics barely moved. Introducing the spatial variables (Model 2) alongside parameter tuning (Model 3) lifted the ROC-AUC from 0.8132 only to 0.8136. Simultaneously, the computational cost exploded, pushing training times from roughly 42 seconds to almost 280 seconds.

## 4.3. Statistical Significance

To determine if this tiny margin was statistically meaningful, we applied McNemar's test to compare the predictions of the Baseline and the Final Improved models directly on the test set. We found 795 instances where only the baseline guessed correctly, compared to 808 instances where only the improved model guessed correctly. The resulting chi-square statistic of 0.0898 yielded a p-value of 0.7644. We followed this with a paired t-test on the cross-validation ROC-AUC scores, which returned a p-value of 0.3099. We therefore conclude that adding explicit spatial features to this specific dataset produced no statistically significant improvement at the 0.05 alpha level.
