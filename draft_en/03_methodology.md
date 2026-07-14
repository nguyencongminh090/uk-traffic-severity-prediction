# 3. Methodology

## 3.1. Data and Preprocessing

We conducted our analysis on a United Kingdom traffic accident dataset, stored as `UK_accidents_balanced.csv`. The raw dataset contained 289,444 samples across 44 features.

To frame the problem as binary classification, we restructured the original `collision_severity` target variable (which coded 1 for Fatal, 2 for Serious, and 3 for Slight). We merged the Serious and Slight categories into a single Non-Fatal class (labeled 0). This transformation yielded a perfectly balanced dataset containing exactly 144,722 Fatal samples and 144,722 Non-Fatal samples.

During preprocessing, we immediately stripped leak-prone identifiers such as `enhanced_severity_collision`, `collision_injury_based`, and `collision_index` to prevent data leakage. We imputed missing numerical values with the median, while assigning the explicit label "missing" to empty categorical fields, followed by standard label encoding. Spatial coordinates (latitude and longitude) were missing in approximately 54% of records and were handled separately by assigning a sentinel value. We then partitioned the data into a training set of 231,555 samples and a holdout test set of 57,889 samples using an 80:20 stratified split based on the target variable.

```python
# Target variable preprocessing
df_model[TARGET] = df_model[TARGET].replace({2: 0, 3: 0})

# Train and test set partitioning
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)
```

## 3.2. Spatial Feature Engineering

We wanted to capture how physical location influences accident severity. To do this, we extracted spatial features directly from the `latitude` and `longitude` columns. We quickly encountered a data quality issue: approximately 54% of the coordinate records were missing. Rather than attempting a complex imputation that might artificially distort the spatial distribution, we assigned a clear sentinel value of `-1` or `"unknown"` to these missing entries.

From the available coordinates, we engineered several new spatial dimensions:
- `spatial_cluster`: We ran a KMeans algorithm (k=20) on the coordinates. Crucially, we fitted the KMeans model strictly on the training set to prevent information bleeding into the test data.
- `grid_region_id`: We mapped coordinates to a static 0.5°×0.5° latitude/longitude grid.
- `cluster_density`: We calculated the proportion of training samples falling into each spatial cluster to proxy regional traffic density.
- `dist_to_nearest_city_km` and `nearest_city_zone`: We computed the Haversine distance to the closest of eight major UK cities and identified that specific metropolitan zone.

## 3.3. Baseline Evaluation

We evaluated nine classification models to establish a performance baseline for accident prediction:
- Linear: Logistic Regression
- Single Tree: Decision Tree
- Bagging Ensembles: Random Forest, Extra Trees
- Classical Boosting: AdaBoost, Gradient Boosting
- Modern GBDTs: XGBoost, LightGBM, CatBoost

## 3.4. Enhanced CatBoost Framework

Because CatBoost emerged as a strong candidate during baseline testing, we selected it as the foundation for our enhanced framework. We leveraged the library's native handling of categorical data by passing the categorical column names directly to the `cat_features` parameter. This directs CatBoost to calculate target statistics rather than relying on our naive integer encoding. We extracted a 15% validation subset from the training data and applied early stopping with a 50-round patience threshold to combat overfitting. Finally, we performed minor hyperparameter tuning across `depth`, `learning_rate`, and `l2_leaf_reg`.

## 3.5. Evaluation Metrics

We measured model performance using Accuracy, Recall, Precision, F1-Macro, and the Receiver Operating Characteristic Area Under the Curve (ROC-AUC). We also recorded training and inference times to quantify the computational trade-offs required by the spatial feature engineering process.
