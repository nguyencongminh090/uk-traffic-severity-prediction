# Phase 8A: Claim-Reference Alignment Audit

### Claim #1
- **Text**: "Related Work ## 2.1 Traffic Accident Severity Prediction Accurately predicting the severity of traffic collisions remains a core challenge in transportation safety research."
- **Location**: 02_related_work.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #2
- **Text**: "Predictive models historically relied on statistical techniques to isolate factors contributing to fatal or severe outcomes [3]."
- **Location**: 02_related_work.md
- **Source type**: REF:[3]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #3
- **Text**: "Researchers have repeatedly demonstrated that algorithmic approaches outperform traditional logistic regression when forecasting collision severity [18, 20, 23]."
- **Location**: 02_related_work.md
- **Source type**: REF:[18, 20, 23]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #4
- **Text**: "Studies leveraging large-scale accident databases frequently build predictive pipelines targeting weather patterns, road geometry, and temporal indicators to classify crash outcomes [16]."
- **Location**: 02_related_work.md
- **Source type**: REF:[16]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #5
- **Text**: "For instance, spatiotemporal analyses confirm that accident hotspots correlate with localized urban features [11], yet many predictive models fail to integrate this spatial variance directly into their training matrices. ## 2.2 Gradient Boosting and Ensemble Methods for Tabular Data Tree-based ensemble architectures consistently dominate predictive tasks involving heterogeneous tabular datasets."
- **Location**: 02_related_work.md
- **Source type**: REF:[11]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #6
- **Text**: "Foundational implementations such as XGBoost [5] and LightGBM [12] introduced highly scalable boosting frameworks that mitigate overfitting while capturing deep feature interactions."
- **Location**: 02_related_work.md
- **Source type**: REF:[5, 12]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #7
- **Text**: "More recently, CatBoost [21] emerged as a specialized architecture optimized for native processing of high-cardinality categorical variables through ordered boosting and target-based encoding strategies."
- **Location**: 02_related_work.md
- **Source type**: REF:[21]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #8
- **Text**: "Investigations into highway collisions and pedestrian crashes routinely deploy XGBoost and LightGBM as primary evaluators [9, 13, 14, 24]."
- **Location**: 02_related_work.md
- **Source type**: REF:[9, 13, 14, 24]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #9
- **Text**: "Hybrid models extending XGBoost with Bayesian networks or optimization routines further refine severity classification [6, 25]."
- **Location**: 02_related_work.md
- **Source type**: REF:[6, 25]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #10
- **Text**: "Our framework specifically leverages CatBoost's categorical processing to handle the outputs of spatial clustering algorithms natively. ## 2.3 Spatial Feature Engineering in Predictive Modeling Geography inherently constrains traffic behavior, yet incorporating spatial dimensions into standard tabular classifiers introduces high dimensionality and sparsity."
- **Location**: 02_related_work.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #11
- **Text**: "Advanced deep learning architectures circumvent this by modeling road networks as dynamic spatial-temporal graphs [7, 22]."
- **Location**: 02_related_work.md
- **Source type**: REF:[7, 22]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #12
- **Text**: "Techniques like Kernel Density Estimation help identify risk clusters [11], but translating geographic coordinates directly into predictive features for boosting algorithms remains challenging due to data fragmentation."
- **Location**: 02_related_work.md
- **Source type**: REF:[11]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #13
- **Text**: "By extracting localized clusters and proximity metrics to major urban centers, we supply the CatBoost algorithm with explicit spatial structures without requiring continuous temporal sensing. ## 2.4 Handling Class Imbalance in Traffic Analysis Traffic accident datasets exhibit severe class imbalance, as fatal collisions constitute a very small minority of total recorded incidents."
- **Location**: 02_related_work.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #14
- **Text**: "Foundational techniques like SMOTE (Synthetic Minority Over-sampling Technique) [4] resolve this by synthesizing artificial minority samples within the feature space."
- **Location**: 02_related_work.md
- **Source type**: REF:[4]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #15
- **Text**: "The necessity of imbalance correction in crash severity prediction is well-documented [1, 2, 8]."
- **Location**: 02_related_work.md
- **Source type**: REF:[1, 2, 8]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #16
- **Text**: "Studies consistently validate that applying SMOTE or similar resampling strategies prevents minority class starvation [10, 19]."
- **Location**: 02_related_work.md
- **Source type**: REF:[10, 19]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #17
- **Text**: "Advanced treatments combine resampling with ensemble bagging or specialized loss functions to further stabilize classification [15, 17]."
- **Location**: 02_related_work.md
- **Source type**: REF:[15, 17]
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #18
- **Text**: "Methodology ## 3.1."
- **Location**: 03_methodology.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #19
- **Text**: "The raw dataset contained 289,444 samples across 44 features."
- **Location**: 03_methodology.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #20
- **Text**: "To frame the problem as binary classification, we restructured the original `collision_severity` target variable (which coded 1 for Fatal, 2 for Serious, and 3 for Slight)."
- **Location**: 03_methodology.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #21
- **Text**: "We merged the Serious and Slight categories into a single Non-Fatal class (labeled 0)."
- **Location**: 03_methodology.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #22
- **Text**: "This transformation yielded a perfectly balanced dataset containing exactly 144,722 Fatal samples and 144,722 Non-Fatal samples."
- **Location**: 03_methodology.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #23
- **Text**: "We then partitioned the data into a training set of 231,555 samples and a holdout test set of 57,889 samples using an 80:20 stratified split based on the target variable. ```python # Target variable preprocessing df_model[TARGET] = df_model[TARGET].replace({2: 0, 3: 0}) # Train and test set partitioning X_train, X_test, y_train, y_test = train_test_split(     X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y ) ``` ## 3.2."
- **Location**: 03_methodology.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #24
- **Text**: "We quickly encountered a data quality issue: approximately 54% of the coordinate records were missing."
- **Location**: 03_methodology.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #25
- **Text**: "Rather than attempting a complex imputation that might artificially distort the spatial distribution, we assigned a clear sentinel value of `-1` or `"unknown"` to these missing entries."
- **Location**: 03_methodology.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #26
- **Text**: "From the available coordinates, we engineered several new spatial dimensions: - `spatial_cluster`: We ran a KMeans algorithm (k=20) on the coordinates."
- **Location**: 03_methodology.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #27
- **Text**: "Crucially, we fitted the KMeans model strictly on the training set to prevent information bleeding into the test data. - `grid_region_id`: We mapped coordinates to a static 0.5°×0.5° latitude/longitude grid. - `cluster_density`: We calculated the proportion of training samples falling into each spatial cluster to proxy regional traffic density. - `dist_to_nearest_city_km` and `nearest_city_zone`: We computed the Haversine distance to the closest of eight major UK cities and identified that specific metropolitan zone. ## 3.3."
- **Location**: 03_methodology.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #28
- **Text**: "Baseline Evaluation We evaluated nine classification models to establish a performance baseline for accident prediction: - Linear: Logistic Regression - Single Tree: Decision Tree - Bagging Ensembles: Random Forest, Extra Trees - Classical Boosting: AdaBoost, Gradient Boosting - Modern GBDTs: XGBoost, LightGBM, CatBoost ## 3.4."
- **Location**: 03_methodology.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #29
- **Text**: "We extracted a 15% validation subset from the training data and applied early stopping with a 50-round patience threshold to combat overfitting."
- **Location**: 03_methodology.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #30
- **Text**: "Finally, we performed minor hyperparameter tuning across `depth`, `learning_rate`, and `l2_leaf_reg`. ## 3.5."
- **Location**: 03_methodology.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #31
- **Text**: "Evaluation Metrics We measured model performance using Accuracy, Recall, Precision, F1-Macro, and the Receiver Operating Characteristic Area Under the Curve (ROC-AUC)."
- **Location**: 03_methodology.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #32
- **Text**: "Experiments & Results We executed a two-stage experimental pipeline: first benchmarking the nine standard classifiers without spatial data, and then performing an ablation study on the CatBoost framework to isolate the impact of our engineered spatial features. ## 4.1."
- **Location**: 04_experiments_results.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #33
- **Text**: "Baseline Model Performance Table 1 details the predictive results of the nine baseline models trained exclusively on the raw, non-spatial feature set. **Table 1**: Baseline model performance comparison | Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time (s) | |---|---|---|---|---|---|---| | CatBoost | 0.7360 | 0.7271 | 0.7555 | 0.7410 | 0.8132 | 41.88 | | XGBoost | 0.7358 | 0.7277 | 0.7537 | 0.7404 | 0.8130 | 16.48 | | LightGBM | 0.7351 | 0.7262 | 0.7546 | 0.7401 | 0.8124 | 14.30 | | Gradient Boosting | 0.7305 | 0.7194 | 0.7560 | 0.7372 | 0.8068 | 163.60 | | Random Forest | 0.7300 | 0.7220 | 0.7480 | 0.7348 | 0.8066 | 121.81 | | Extra Trees | 0.7150 | 0.7085 | 0.7305 | 0.7193 | 0.7883 | 62.29 | | AdaBoost | 0.7115 | 0.7135 | 0.7067 | 0.7101 | 0.7873 | 55.98 | | Decision Tree | 0.7156 | 0.7045 | 0.7425 | 0.7230 | 0.7839 | 3.23 | | Logistic Regression | 0.6752 | 0.6834 | 0.6526 | 0.6677 | 0.7368 | 302.01 | The modern Gradient Boosted Decision Trees (CatBoost, XGBoost, and LightGBM) distinctly outperformed the linear Logistic Regression baseline, establishing a roughly 6% advantage in raw accuracy and an 0.08 margin in ROC-AUC."
- **Location**: 04_experiments_results.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #34
- **Text**: "CatBoost secured the highest overall ranking with an ROC-AUC of 0.8132."
- **Location**: 04_experiments_results.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #35
- **Text**: "To verify stability, we ran a 5-fold cross-validation routine on the CatBoost baseline."
- **Location**: 04_experiments_results.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #36
- **Text**: "The model returned a mean ROC-AUC of 0.8119 with a tight standard deviation of ±0.0019. ## 4.2."
- **Location**: 04_experiments_results.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #37
- **Text**: "Table 2 presents three CatBoost variants: the raw baseline, a version injected with the new spatial features, and a finalized version that added specific hyperparameter tuning. **Table 2**: CatBoost ablation study | Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time (s) | |---|---|---|---|---|---|---| | 1."
- **Location**: 04_experiments_results.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #38
- **Text**: "Baseline CatBoost | 0.7360 | 0.7271 | 0.7555 | 0.7410 | 0.8132 | 41.88 | | 2."
- **Location**: 04_experiments_results.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #39
- **Text**: "CatBoost + Spatial Features | 0.7350 | 0.7262 | 0.7542 | 0.7400 | 0.8132 | 169.05 | | 3."
- **Location**: 04_experiments_results.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #40
- **Text**: "Final Improved CatBoost | 0.7362 | 0.7278 | 0.7547 | 0.7410 | 0.8136 | 279.67 | We expected the spatial data to push the model's predictive boundary."
- **Location**: 04_experiments_results.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #41
- **Text**: "Introducing the spatial variables (Model 2) alongside parameter tuning (Model 3) lifted the ROC-AUC from 0.8132 only to 0.8136."
- **Location**: 04_experiments_results.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #42
- **Text**: "Simultaneously, the computational cost exploded, pushing training times from roughly 42 seconds to almost 280 seconds. ## 4.3."
- **Location**: 04_experiments_results.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #43
- **Text**: "Statistical Significance To determine if this tiny margin was statistically meaningful, we applied McNemar's test to compare the predictions of the Baseline and the Final Improved models directly on the test set."
- **Location**: 04_experiments_results.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #44
- **Text**: "We found 795 instances where only the baseline guessed correctly, compared to 808 instances where only the improved model guessed correctly."
- **Location**: 04_experiments_results.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #45
- **Text**: "The resulting chi-square statistic of 0.0898 yielded a p-value of 0.7644."
- **Location**: 04_experiments_results.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #46
- **Text**: "We followed this with a paired t-test on the cross-validation ROC-AUC scores, which returned a p-value of 0.3099."
- **Location**: 04_experiments_results.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #47
- **Text**: "We therefore conclude that adding explicit spatial features to this specific dataset produced no statistically significant improvement at the 0.05 alpha level."
- **Location**: 04_experiments_results.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #48
- **Text**: "As the statistical tests in Section 4 demonstrated, the spatial features failed to improve the model's predictive power."
- **Location**: 05_discussion.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #49
- **Text**: "With 54% of the geographic data missing and masked by a sentinel value, the spatial signal became heavily diluted."
- **Location**: 05_discussion.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #50
- **Text**: "Once the model splits a decision tree on a 70-mph rural road governed by a specific regional police force, it has already effectively localized the accident."
- **Location**: 05_discussion.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #51
- **Text**: "While the engineered spatial features did not boost predictive accuracy, this negative result clarifies a practical engineering constraint."
- **Location**: 05_discussion.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED

### Claim #52
- **Text**: "Our benchmarking confirmed that modern Gradient Boosted Decision Trees—CatBoost, XGBoost, and LightGBM—easily outcompete linear models and simple decision trees for this specific collision data."
- **Location**: 06_conclusion.md
- **Source type**: NOTEBOOK
- **Verification**: ✅ Match
- **Detail**: Matches known notebook output or verified reference.
- **Action**: KEEP

### Claim #53
- **Text**: "Extensive missing coordinate data (54%) crippled the spatial signal, while existing variables like speed limits and administrative zones already captured the necessary geographic context."
- **Location**: 06_conclusion.md
- **Source type**: UNSUPPORTED
- **Verification**: ❌ Not found
- **Detail**: Claim appears unsupported by explicit notebook outputs or references.
- **Action**: CITE_NEEDED
