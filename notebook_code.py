# Cell 0
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, f1_score
)
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier
!pip install catboost
from catboost import CatBoostClassifier
from xgboost import XGBClassifier

RANDOM_STATE = 42
TARGET = "collision_severity"

# 1.Load data
df = pd.read_csv("/content/UK_accidents_balanced.csv")
print(f"Loaded data: {df.shape[0]:,} rows x {df.shape[1]} columns")

# Shuffle toàn bộ dataset
df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

# 2. Drop columns that either identify the record or leak the target
leak_cols = [
    "enhanced_severity_collision",
    "collision_injury_based",
    "collision_adjusted_severity_serious",
    "collision_adjusted_severity_slight",
]
id_cols = [
    "collision_index", "collision_ref_no", "date", "time",
    "local_authority_ons_district", "local_authority_highway",
    "local_authority_highway_current", "lsoa_of_accident_location",
]

drop_cols = leak_cols + id_cols
df_model = df.drop(columns=[c for c in drop_cols if c in df.columns])

# 3. Handle missing values

num_cols = df_model.select_dtypes(include=[np.number]).columns.tolist()
num_cols.remove(TARGET)
cat_cols = df_model.select_dtypes(exclude=[np.number]).columns.tolist()

for c in num_cols:
    df_model[c] = df_model[c].fillna(df_model[c].median())
for c in cat_cols:
    df_model[c] = df_model[c].fillna("missing")

# 4. Encode remaining categorical columns

for c in cat_cols:
    df_model[c] = LabelEncoder().fit_transform(df_model[c].astype(str))


# 4b. Gộp nhãn: 2,3 -> 0 (chỉ giữ 1 = Fatal, còn lại = 0)

df_model[TARGET] = df_model[TARGET].replace({2: 0, 3: 0})
print("Phân bố nhãn sau khi gộp:")
print(df_model[TARGET].value_counts())


# 5. Train / test split

X = df_model.drop(columns=[TARGET])
y = df_model[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)
print(f"Train: {X_train.shape[0]:,} rows | Test: {X_test.shape[0]:,} rows")


# 6. Train Models

# Logistic Regression
model1 = LogisticRegression(
    max_iter=5000,
    class_weight="balanced",
    random_state=42
)
model1.fit(X_train, y_train)

# Random Forest
model2 = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    min_samples_leaf=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
model2.fit(X_train, y_train)

# XGBoost
model3 = XGBClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42
)
model3.fit(X_train, y_train)

# LightGBM
model4 = LGBMClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=10,
    class_weight="balanced",
    random_state=42
)
model4.fit(X_train, y_train)

# CatBoost
model5 = CatBoostClassifier(
    iterations=500,
    depth=8,
    learning_rate=0.05,
    loss_function="Logloss",
    eval_metric="F1",
    verbose=False,
    random_seed=42
)
model5.fit(X_train, y_train)


# 7. Evaluate

models = {
    "Logistic Regression": model1,
    "Random Forest": model2,
    "XGBoost": model3,
    "LightGBM": model4,
    "CatBoost": model5
}

for name, model in models.items():

    print("\n" + "=" * 60)
    print(f"{name} RESULTS")
    print("=" * 60)

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average="macro")

    print(f"Accuracy   : {acc:.4f}")
    print(f"F1 Macro   : {f1_macro:.4f}")

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=["Non-Fatal (0)", "Fatal (1)"]
    ))

    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    print(cm)

    # Feature Importance
    if hasattr(model, "feature_importances_"):

      print("\nTop 15 Feature Importances:")

      importance = pd.Series(
        model.feature_importances_,
        index=X.columns
      ).sort_values(ascending=False)

      print(importance.head(15))
results = []

for name, model in models.items():

    y_pred = model.predict(X_test)

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "F1 Macro": f1_score(y_test, y_pred, average="macro")
    })

results = pd.DataFrame(results)

print("\nModel Comparison")
print(results.sort_values("F1 Macro", ascending=False))
# Cell 3
import matplotlib.pyplot as plt
# --- Missing value rates (computed on the untouched `df`, before the pipeline's fillna) ---
missing_rates = (df[df_model.columns].isna().mean() * 100).sort_values(ascending=False)
missing_rates = missing_rates[missing_rates > 0]

fig, ax = plt.subplots(figsize=(8, max(4, len(missing_rates) * 0.3)))
missing_rates.sort_values().plot.barh(ax=ax, color="indianred")
ax.set_xlabel("Missing (%)")
ax.set_title("Missing Value Rate by Column (before imputation)")
plt.tight_layout()
plt.show()

print(missing_rates)

# Cell 4
# --- Target distribution: original 3-class severity vs. the binary Fatal/Non-Fatal modeling target ---
severity_labels = {1: "Fatal", 2: "Serious", 3: "Slight"}

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

df[TARGET].map(severity_labels).value_counts().plot.bar(ax=axes[0], color="steelblue")
axes[0].set_title("Original collision_severity (3 classes)")
axes[0].set_ylabel("Count")
axes[0].tick_params(axis="x", rotation=0)

y.map({0: "Non-Fatal", 1: "Fatal"}).value_counts().plot.bar(ax=axes[1], color=["#4C72B0", "#C44E52"])
axes[1].set_title("Modeling Target: Fatal vs Non-Fatal")
axes[1].set_ylabel("Count")
axes[1].tick_params(axis="x", rotation=0)

plt.tight_layout()
plt.show()

print("Modeling target proportions:")
print(y.value_counts(normalize=True).rename("proportion"))

# Cell 5
# --- Fatal rate by key variables (original, human-readable categories from `df`) ---
key_vars = ["speed_limit", "weather_conditions", "road_type", "light_conditions", "urban_or_rural_area"]
overall_fatal_rate = (df[TARGET] == 1).mean()

fig, axes = plt.subplots(len(key_vars), 1, figsize=(8, 4 * len(key_vars)))
for ax, col in zip(axes, key_vars):
    rate = df.groupby(col)[TARGET].apply(lambda s: (s == 1).mean()).sort_values(ascending=False)
    rate.plot.bar(ax=ax, color="darkorange")
    ax.set_title(f"Fatal Rate by {col}")
    ax.set_ylabel("Fatal rate")
    ax.axhline(overall_fatal_rate, color="black", linestyle="--", linewidth=1, label="Overall fatal rate")
    ax.legend()

plt.tight_layout()
plt.show()

# Cell 6
# --- Geographic distribution of accidents by severity (raw lat/lon, before imputation) ---
geo = df[["latitude", "longitude", TARGET]].dropna()

fig, ax = plt.subplots(figsize=(7, 9))
for sev, color, label in [(1, "red", "Fatal"), (2, "orange", "Serious"), (3, "steelblue", "Slight")]:
    subset = geo[geo[TARGET] == sev]
    ax.scatter(subset["longitude"], subset["latitude"], s=2, alpha=0.15, color=color, label=label)

ax.set_title(f"Geographic Distribution of Accidents by Severity (n={len(geo):,} with known coordinates)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_aspect("equal")
ax.legend(markerscale=8)
plt.tight_layout()
plt.show()

# Cell 8
# --- Additional imports for the extended ML section (Parts 1-5) ---
import time
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    ExtraTreesClassifier, AdaBoostClassifier, GradientBoostingClassifier
)
from sklearn.cluster import KMeans
from sklearn.metrics import (
    precision_score, recall_score, roc_auc_score, roc_curve, precision_recall_curve
)

sns.set_style("whitegrid")


def train_and_evaluate(name, model, X_tr, y_tr, X_te, y_te,
                        fit_kwargs=None, already_fitted=False, train_time=None):
    """
    Reusable train/evaluate routine shared by Part 1, Part 3 (ablation) and Part 4.

    If already_fitted=True, `model` is assumed pre-trained (used for the Improved
    CatBoost model, whose training involves early stopping / a validation set and
    therefore happens outside this helper) and `train_time` must be supplied.
    """
    fit_kwargs = fit_kwargs or {}

    if not already_fitted:
        start = time.time()
        model.fit(X_tr, y_tr, **fit_kwargs)
        train_time = time.time() - start

    start = time.time()
    y_pred = model.predict(X_te)
    inference_time = time.time() - start

    y_proba = (
        model.predict_proba(X_te)[:, 1] if hasattr(model, "predict_proba") else y_pred
    )

    cm = confusion_matrix(y_te, y_pred, labels=[0, 1])

    metrics = {
        "Model": name,
        "Accuracy": accuracy_score(y_te, y_pred),
        "Precision": precision_score(y_te, y_pred, zero_division=0),
        "Recall": recall_score(y_te, y_pred, zero_division=0),
        "F1-Score": f1_score(y_te, y_pred),
        "ROC-AUC": roc_auc_score(y_te, y_proba),
        "Training Time (s)": train_time,
        "Inference Time (s)": inference_time,
    }
    return metrics, model, y_pred, y_proba, cm


def print_model_report(name, metrics, cm):
    """Console report shared across all sections."""
    print("\n" + "=" * 60)
    print(f"{name} RESULTS")
    print("=" * 60)
    for k in ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]:
        print(f"{k:<12}: {metrics[k]:.4f}")
    print(f"{'Train Time':<12}: {metrics['Training Time (s)']:.2f}s")
    print(f"{'Infer Time':<12}: {metrics['Inference Time (s)']:.4f}s")
    print("Confusion Matrix ([[TN, FP], [FN, TP]]):")
    print(cm)

# Cell 9
# --- Model registry: consistent RANDOM_STATE, reused train/test split ---
baseline_model_registry = {
    "Logistic Regression": LogisticRegression(
        max_iter=5000, class_weight="balanced", random_state=RANDOM_STATE
    ),
    "Decision Tree": DecisionTreeClassifier(
        max_depth=12, min_samples_leaf=5, class_weight="balanced", random_state=RANDOM_STATE
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=300, max_depth=20, min_samples_leaf=5,
        class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1
    ),
    "Extra Trees": ExtraTreesClassifier(
        n_estimators=300, max_depth=20, min_samples_leaf=5,
        class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1
    ),
    "AdaBoost": AdaBoostClassifier(
        n_estimators=200, learning_rate=0.5, random_state=RANDOM_STATE
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=200, max_depth=4, learning_rate=0.05,
        subsample=0.8, random_state=RANDOM_STATE
    ),
    "XGBoost": XGBClassifier(
        n_estimators=500, learning_rate=0.05, max_depth=8,
        subsample=0.8, colsample_bytree=0.8, objective="binary:logistic",
        eval_metric="logloss", random_state=RANDOM_STATE, n_jobs=-1
    ),
    "LightGBM": LGBMClassifier(
        n_estimators=500, learning_rate=0.05, max_depth=10,
        class_weight="balanced", random_state=RANDOM_STATE
    ),
    "CatBoost (Baseline)": CatBoostClassifier(
        iterations=500, depth=8, learning_rate=0.05,
        loss_function="Logloss", eval_metric="F1",
        verbose=False, random_seed=RANDOM_STATE
    ),
}

baseline_results = []
baseline_fitted_models = {}
baseline_confusion_matrices = {}

for name, model in baseline_model_registry.items():
    metrics, fitted_model, y_pred, y_proba, cm = train_and_evaluate(
        name, model, X_train, y_train, X_test, y_test
    )
    print_model_report(name, metrics, cm)

    baseline_results.append(metrics)
    baseline_fitted_models[name] = fitted_model
    baseline_confusion_matrices[name] = cm

baseline_comparison_df = pd.DataFrame(baseline_results).sort_values(
    "ROC-AUC", ascending=False
).reset_index(drop=True)

# Cell 10
print("\nFinal Model Comparison (Part 1 — Baseline & Advanced Models)")
display_cols = ["Model", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC",
                 "Training Time (s)", "Inference Time (s)"]
baseline_comparison_df_display = baseline_comparison_df[display_cols].round(4)
print(baseline_comparison_df_display.to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(
    data=baseline_comparison_df, x="ROC-AUC", y="Model",
    hue="Model", palette="viridis", legend=False, ax=ax
)
ax.set_title("Part 1 — Model Comparison by ROC-AUC")
ax.set_xlim(0.5, 1.0)
plt.tight_layout()
plt.show()

baseline_comparison_df_display

# Cell 12
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.base import clone

CV_FOLDS = 5
cv_splitter = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

cv_records = []
for name, model in baseline_model_registry.items():
    cv_result = cross_validate(
        clone(model), X_train, y_train, cv=cv_splitter,
        scoring=["accuracy", "f1", "roc_auc"], n_jobs=1
    )
    cv_records.append({
        "Model": name,
        "Accuracy": f"{cv_result['test_accuracy'].mean():.4f} ± {cv_result['test_accuracy'].std():.4f}",
        "F1-Score": f"{cv_result['test_f1'].mean():.4f} ± {cv_result['test_f1'].std():.4f}",
        "ROC-AUC": f"{cv_result['test_roc_auc'].mean():.4f} ± {cv_result['test_roc_auc'].std():.4f}",
        "ROC-AUC (raw folds)": cv_result["test_roc_auc"],
    })
    print(f"{name}: ROC-AUC = {cv_result['test_roc_auc'].mean():.4f} ± {cv_result['test_roc_auc'].std():.4f}")

cv_results_df = pd.DataFrame(cv_records)
print(f"\n{CV_FOLDS}-Fold Cross-Validation Results (training set only)")
print(cv_results_df[["Model", "Accuracy", "F1-Score", "ROC-AUC"]].to_string(index=False))
cv_results_df[["Model", "Accuracy", "F1-Score", "ROC-AUC"]]

# Cell 14
# Model complexity summary: a simple, model-agnostic proxy (n_estimators/trees, max depth)
def get_model_complexity(model):
    n_estimators = getattr(model, "n_estimators", None) or getattr(model, "tree_count_", None) or 1
    depth = getattr(model, "max_depth", None) or getattr(model, "depth", None)
    return n_estimators, depth

complexity_records = []
for name, model in baseline_fitted_models.items():
    n_est, depth = get_model_complexity(model)
    complexity_records.append({"Model": name, "Estimators/Trees": n_est, "Max Depth": depth})
complexity_df = pd.DataFrame(complexity_records)

cost_df = baseline_comparison_df.merge(complexity_df, on="Model")
cost_display_cols = ["Model", "ROC-AUC", "Training Time (s)", "Inference Time (s)",
                      "Estimators/Trees", "Max Depth"]
print(cost_df[cost_display_cols].to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(cost_df["Training Time (s)"], cost_df["ROC-AUC"], s=80, color="purple")
for _, row in cost_df.iterrows():
    ax.annotate(row["Model"], (row["Training Time (s)"], row["ROC-AUC"]),
                fontsize=8, xytext=(4, 4), textcoords="offset points")
ax.set_xlabel("Training Time (s)")
ax.set_ylabel("ROC-AUC")
ax.set_title("Accuracy vs. Computational Cost Trade-off")
plt.tight_layout()
plt.show()

# Cell 16
# --- Spatial Feature Engineering (fit only on training data — no leakage) ---
# NOTE: X_train / X_test already contain a median-imputed 'latitude'/'longitude'
# from the shared preprocessing pipeline. Here we go back to the *raw*, un-imputed
# coordinates in `df` (same row index as X_train/X_test) so spatial statistics are
# not distorted by the ~54% of rows that would otherwise sit on one imputed point.

N_SPATIAL_CLUSTERS = 20
GRID_SIZE_DEGREES = 0.5  # ~35-55km grid cells across the UK

UK_MAJOR_CITIES = {
    "London": (51.5074, -0.1278),
    "Birmingham": (52.4862, -1.8904),
    "Manchester": (53.4808, -2.2426),
    "Leeds": (53.8008, -1.5491),
    "Glasgow": (55.8642, -4.2518),
    "Edinburgh": (55.9533, -3.1883),
    "Liverpool": (53.4084, -2.9916),
    "Bristol": (51.4545, -2.5879),
}


def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance (km) between two coordinates (vectorized)."""
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


def assign_spatial_cluster(idx, kmeans_model):
    """1. Location Cluster: KMeans cluster id. -1 sentinel = missing coordinates."""
    coords = df.loc[idx, ["latitude", "longitude"]]
    valid = coords.notna().all(axis=1)
    cluster = pd.Series(-1, index=idx, name="spatial_cluster")
    if valid.any():
        cluster.loc[valid] = kmeans_model.predict(coords.loc[valid])
    return cluster.astype(int)


def assign_grid_region_id(idx):
    """2. Grid-based Region ID: deterministic lat/lon binning, no fitting required."""
    coords = df.loc[idx, ["latitude", "longitude"]]
    valid = coords.notna().all(axis=1)
    lat_bin = (coords["latitude"] // GRID_SIZE_DEGREES).astype("Int64").astype(str)
    lon_bin = (coords["longitude"] // GRID_SIZE_DEGREES).astype("Int64").astype(str)
    grid_id = (lat_bin + "_" + lon_bin).where(valid, "unknown")
    return grid_id.rename("grid_region_id")


def assign_spatial_zone(idx):
    """4. Spatial Zone Feature: distance (km) to, and name of, the nearest major UK city."""
    coords = df.loc[idx, ["latitude", "longitude"]]
    valid = coords.notna().all(axis=1)
    dists = pd.DataFrame({
        city: haversine_km(coords["latitude"], coords["longitude"], lat, lon)
        for city, (lat, lon) in UK_MAJOR_CITIES.items()
    })
    nearest_dist = dists.min(axis=1).where(valid, -1).rename("dist_to_nearest_city_km")
    nearest_zone = dists.fillna(1e9).idxmin(axis=1).where(valid, "unknown").rename("nearest_city_zone")
    return nearest_dist, nearest_zone


# Fit KMeans on TRAIN coordinates only
train_coords = df.loc[X_train.index, ["latitude", "longitude"]].dropna()
kmeans_spatial = KMeans(n_clusters=N_SPATIAL_CLUSTERS, random_state=RANDOM_STATE, n_init=10)
kmeans_spatial.fit(train_coords)

spatial_cluster_train = assign_spatial_cluster(X_train.index, kmeans_spatial)
spatial_cluster_test = assign_spatial_cluster(X_test.index, kmeans_spatial)

grid_id_train = assign_grid_region_id(X_train.index)
grid_id_test = assign_grid_region_id(X_test.index)

# 3. Cluster Density: relative frequency of each cluster, computed on TRAIN ONLY,
#    then mapped onto both splits (unseen clusters in test -> 0 density)
cluster_density_map = (spatial_cluster_train.value_counts() / len(spatial_cluster_train)).to_dict()
cluster_density_train = spatial_cluster_train.map(cluster_density_map).rename("cluster_density")
cluster_density_test = spatial_cluster_test.map(cluster_density_map).fillna(0).rename("cluster_density")

dist_city_train, zone_train = assign_spatial_zone(X_train.index)
dist_city_test, zone_test = assign_spatial_zone(X_test.index)

print(f"Fitted KMeans on {len(train_coords):,} training records with valid coordinates "
      f"({len(train_coords) / len(X_train):.1%} of the training set).")
print("Spatial cluster distribution (train):")
print(spatial_cluster_train.value_counts().sort_index())

# Cell 18
# --- Assemble spatially-augmented feature sets ---
# Raw (already median-imputed) latitude/longitude are dropped in favour of the
# engineered spatial features above, which handle missingness explicitly.
X_train_spatial = X_train.drop(columns=["latitude", "longitude"]).copy()
X_test_spatial = X_test.drop(columns=["latitude", "longitude"]).copy()

spatial_feature_frames = {
    "spatial_cluster": (spatial_cluster_train.astype(str), spatial_cluster_test.astype(str)),
    "grid_region_id": (grid_id_train, grid_id_test),
    "cluster_density": (cluster_density_train, cluster_density_test),
    "dist_to_nearest_city_km": (dist_city_train, dist_city_test),
    "nearest_city_zone": (zone_train, zone_test),
}
for col, (train_vals, test_vals) in spatial_feature_frames.items():
    X_train_spatial[col] = train_vals.values
    X_test_spatial[col] = test_vals.values

# Native categorical handling: tell CatBoost to treat these columns as categories
# (not ordinal numbers), instead of relying on the LabelEncoder integers as-is.
spatial_categorical_cols = ["spatial_cluster", "grid_region_id", "nearest_city_zone"] + cat_cols
cat_feature_idx = [
    X_train_spatial.columns.get_loc(c) for c in spatial_categorical_cols
    if c in X_train_spatial.columns
]

print(f"X_train_spatial shape: {X_train_spatial.shape}")
print(f"Categorical features passed natively to CatBoost ({len(cat_feature_idx)}): "
      f"{spatial_categorical_cols}")

# Cell 20
# --- Train/validation split (test set stays untouched until final evaluation) ---
X_tr_sub, X_val, y_tr_sub, y_val = train_test_split(
    X_train_spatial, y_train, test_size=0.15,
    random_state=RANDOM_STATE, stratify=y_train
)

# --- Lightweight hyperparameter search, scored on the validation set ---
catboost_param_grid = [
    {"depth": 6, "learning_rate": 0.05, "l2_leaf_reg": 3},
    {"depth": 8, "learning_rate": 0.05, "l2_leaf_reg": 5},
    {"depth": 8, "learning_rate": 0.03, "l2_leaf_reg": 5},
    {"depth": 10, "learning_rate": 0.05, "l2_leaf_reg": 7},
]

tuning_records = []
best_val_auc, best_params = -np.inf, None

for params in catboost_param_grid:
    candidate = CatBoostClassifier(
        iterations=1000, loss_function="Logloss", eval_metric="AUC",
        random_seed=RANDOM_STATE, verbose=False, **params
    )
    candidate.fit(
        X_tr_sub, y_tr_sub, eval_set=(X_val, y_val),
        cat_features=cat_feature_idx, early_stopping_rounds=50, use_best_model=True
    )
    val_auc = roc_auc_score(y_val, candidate.predict_proba(X_val)[:, 1])
    tuning_records.append({**params, "val_AUC": val_auc, "best_iteration": candidate.get_best_iteration()})

    if val_auc > best_val_auc:
        best_val_auc, best_params = val_auc, params

tuning_df = pd.DataFrame(tuning_records).sort_values("val_AUC", ascending=False)
print("Hyperparameter search results (validation set):")
print(tuning_df.to_string(index=False))
print(f"\nSelected params: {best_params}")

# --- Refit final model with the best params, early stopping on the same validation set ---
start = time.time()
improved_catboost = CatBoostClassifier(
    iterations=1500, loss_function="Logloss", eval_metric="AUC",
    random_seed=RANDOM_STATE, verbose=False, **best_params
)
improved_catboost.fit(
    X_tr_sub, y_tr_sub, eval_set=(X_val, y_val),
    cat_features=cat_feature_idx, early_stopping_rounds=50, use_best_model=True
)
improved_catboost_train_time = time.time() - start

print(f"\nBest iteration: {improved_catboost.get_best_iteration()} "
      f"(of {improved_catboost.tree_count_} trees kept)")
print(f"Training time: {improved_catboost_train_time:.2f}s")

improved_metrics, improved_catboost, improved_y_pred, improved_y_proba, improved_cm = train_and_evaluate(
    "Improved CatBoost (Spatial + Tuned)", improved_catboost,
    None, None, X_test_spatial, y_test,
    already_fitted=True, train_time=improved_catboost_train_time
)
print_model_report("Improved CatBoost (Spatial + Tuned)", improved_metrics, improved_cm)

# Cell 22
# --- Sensitivity Analysis: does the choice of k (KMeans) / grid size change results much? ---
def build_spatial_features(idx_train, idx_test, n_clusters, grid_size):
    """Rebuild spatial_cluster + grid_region_id for a given (k, grid_size) — reuses the
    same leakage-safe, fit-on-train-only logic as the main Part 2 pipeline."""
    coords_train = df.loc[idx_train, ["latitude", "longitude"]].dropna()
    km = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init=10).fit(coords_train)

    def _cluster(idx):
        coords = df.loc[idx, ["latitude", "longitude"]]
        valid = coords.notna().all(axis=1)
        c = pd.Series(-1, index=idx)
        if valid.any():
            c.loc[valid] = km.predict(coords.loc[valid])
        return c.astype(int).astype(str)

    def _grid(idx):
        coords = df.loc[idx, ["latitude", "longitude"]]
        valid = coords.notna().all(axis=1)
        lat_bin = (coords["latitude"] // grid_size).astype("Int64").astype(str)
        lon_bin = (coords["longitude"] // grid_size).astype("Int64").astype(str)
        return (lat_bin + "_" + lon_bin).where(valid, "unknown")

    return _cluster(idx_train), _cluster(idx_test), _grid(idx_train), _grid(idx_test)


def evaluate_spatial_config(n_clusters, grid_size):
    sc_tr, sc_te, g_tr, g_te = build_spatial_features(X_train.index, X_test.index, n_clusters, grid_size)

    Xtr = X_train.drop(columns=["latitude", "longitude"]).copy()
    Xte = X_test.drop(columns=["latitude", "longitude"]).copy()
    Xtr["spatial_cluster"], Xte["spatial_cluster"] = sc_tr.values, sc_te.values
    Xtr["grid_region_id"], Xte["grid_region_id"] = g_tr.values, g_te.values

    cat_idx = [Xtr.columns.get_loc(c) for c in ["spatial_cluster", "grid_region_id"] + cat_cols]

    model = CatBoostClassifier(
        iterations=300, depth=8, learning_rate=0.05, loss_function="Logloss",
        eval_metric="AUC", verbose=False, random_seed=RANDOM_STATE
    )
    model.fit(Xtr, y_train, cat_features=cat_idx)
    return roc_auc_score(y_test, model.predict_proba(Xte)[:, 1])


# Vary number of KMeans clusters (grid size fixed at the Part 2 default)
k_values = [5, 10, 20, 30, 50]
k_sensitivity_df = pd.DataFrame(
    [{"k": k, "ROC-AUC": evaluate_spatial_config(k, GRID_SIZE_DEGREES)} for k in k_values]
)

# Vary grid size in degrees (k fixed at the Part 2 default)
grid_values = [0.1, 0.25, 0.5, 1.0, 2.0]
grid_sensitivity_df = pd.DataFrame(
    [{"grid_size": g, "ROC-AUC": evaluate_spatial_config(N_SPATIAL_CLUSTERS, g)} for g in grid_values]
)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(k_sensitivity_df["k"], k_sensitivity_df["ROC-AUC"], marker="o")
axes[0].axvline(N_SPATIAL_CLUSTERS, color="gray", linestyle="--", label="Chosen k")
axes[0].set_xlabel("Number of KMeans clusters (k)")
axes[0].set_ylabel("Test ROC-AUC")
axes[0].set_title("Sensitivity to k")
axes[0].legend()

axes[1].plot(grid_sensitivity_df["grid_size"], grid_sensitivity_df["ROC-AUC"], marker="o", color="darkorange")
axes[1].axvline(GRID_SIZE_DEGREES, color="gray", linestyle="--", label="Chosen grid size")
axes[1].set_xlabel("Grid size (degrees)")
axes[1].set_ylabel("Test ROC-AUC")
axes[1].set_title("Sensitivity to grid size")
axes[1].legend()

plt.tight_layout()
plt.show()

print(k_sensitivity_df)
print(grid_sensitivity_df)

# Cell 24
# 1. Baseline CatBoost — reuse the already-trained Part 1 model, no retraining needed
baseline_cb_metrics = next(r for r in baseline_results if r["Model"] == "CatBoost (Baseline)")
baseline_cb_metrics = {**baseline_cb_metrics, "Model": "1. Baseline CatBoost"}

# 2. CatBoost + Spatial Features only — same hyperparameters as the Part 1 baseline,
#    trained on the spatially-augmented features, no early stopping / tuning
catboost_spatial_only = CatBoostClassifier(
    iterations=500, depth=8, learning_rate=0.05,
    loss_function="Logloss", eval_metric="F1",
    verbose=False, random_seed=RANDOM_STATE
)
spatial_only_metrics, catboost_spatial_only, _, _, spatial_only_cm = train_and_evaluate(
    "2. CatBoost + Spatial Features", catboost_spatial_only,
    X_train_spatial, y_train, X_test_spatial, y_test,
    fit_kwargs={"cat_features": cat_feature_idx}
)
print_model_report("2. CatBoost + Spatial Features", spatial_only_metrics, spatial_only_cm)

# 3. Final Improved CatBoost — from Part 2
final_metrics = {**improved_metrics, "Model": "3. Final Improved CatBoost"}

ablation_df = pd.DataFrame([baseline_cb_metrics, spatial_only_metrics, final_metrics])
ablation_display_cols = ["Model", "Accuracy", "Precision", "Recall", "F1-Score",
                          "ROC-AUC", "Training Time (s)", "Inference Time (s)"]
ablation_df = ablation_df[ablation_display_cols].round(4)

print("\nAblation Study — CatBoost Variants")
print(ablation_df.to_string(index=False))
ablation_df

# Cell 26
# 1. McNemar's test — Baseline CatBoost vs Final Improved CatBoost, held-out test set
from scipy.stats import chi2, ttest_rel


def mcnemar_test(y_true, pred_a, pred_b):
    """Continuity-corrected McNemar's test on paired classifier predictions."""
    correct_a = (pred_a == y_true)
    correct_b = (pred_b == y_true)
    only_a_correct = int(np.sum(correct_a & ~correct_b))
    only_b_correct = int(np.sum(~correct_a & correct_b))
    if only_a_correct + only_b_correct == 0:
        return 0.0, 1.0, only_a_correct, only_b_correct
    stat = (abs(only_a_correct - only_b_correct) - 1) ** 2 / (only_a_correct + only_b_correct)
    p_value = 1 - chi2.cdf(stat, df=1)
    return stat, p_value, only_a_correct, only_b_correct


baseline_test_pred = baseline_fitted_models["CatBoost (Baseline)"].predict(X_test)
mcnemar_stat, mcnemar_p, n_only_baseline, n_only_improved = mcnemar_test(
    y_test.values, baseline_test_pred, improved_y_pred
)

print("McNemar's Test — Baseline CatBoost vs. Final Improved CatBoost")
print(f"Only Baseline correct : {n_only_baseline}")
print(f"Only Improved correct : {n_only_improved}")
print(f"chi2 statistic = {mcnemar_stat:.4f}, p-value = {mcnemar_p:.4g}")
print("=> Statistically significant difference (p < 0.05)" if mcnemar_p < 0.05
      else "=> No statistically significant difference at the 0.05 level")

# Cell 27
# 2. Paired t-test — original features vs. spatial features, same 5-fold CV splits
def cv_roc_auc_scores(X, y, cat_features, splitter, iterations=300):
    scores = []
    for train_idx, val_idx in splitter.split(X, y):
        X_tr, X_va = X.iloc[train_idx], X.iloc[val_idx]
        y_tr, y_va = y.iloc[train_idx], y.iloc[val_idx]
        m = CatBoostClassifier(
            iterations=iterations, depth=8, learning_rate=0.05,
            loss_function="Logloss", eval_metric="AUC",
            verbose=False, random_seed=RANDOM_STATE
        )
        m.fit(X_tr, y_tr, cat_features=cat_features)
        scores.append(roc_auc_score(y_va, m.predict_proba(X_va)[:, 1]))
    return np.array(scores)


sig_splitter = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
baseline_cat_idx = [X_train.columns.get_loc(c) for c in cat_cols]

baseline_fold_auc = cv_roc_auc_scores(X_train, y_train, baseline_cat_idx, sig_splitter)
spatial_fold_auc = cv_roc_auc_scores(X_train_spatial, y_train, cat_feature_idx, sig_splitter)

t_stat, t_p_value = ttest_rel(spatial_fold_auc, baseline_fold_auc)

print(f"Baseline CatBoost  CV ROC-AUC: {baseline_fold_auc.mean():.4f} ± {baseline_fold_auc.std():.4f}  {baseline_fold_auc.round(4)}")
print(f"Spatial CatBoost   CV ROC-AUC: {spatial_fold_auc.mean():.4f} ± {spatial_fold_auc.std():.4f}  {spatial_fold_auc.round(4)}")
print(f"\nPaired t-test: t = {t_stat:.4f}, p = {t_p_value:.4g}")
print("=> Statistically significant improvement from spatial features (p < 0.05)" if t_p_value < 0.05
      else "=> No statistically significant improvement from spatial features at the 0.05 level")

# Cell 29
# 1. Feature Importance (Final Improved CatBoost)
final_importance = pd.Series(
    improved_catboost.get_feature_importance(),
    index=X_train_spatial.columns
).sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 8))
final_importance.head(20).sort_values().plot.barh(ax=ax, color="teal")
ax.set_title("Final Improved CatBoost — Top 20 Feature Importances")
ax.set_xlabel("Importance")
plt.tight_layout()
plt.show()

# Cell 30
# 2 & 3. SHAP Summary & Bar plots (sampled test rows for speed)
!pip install shap --quiet
import shap

shap_sample = X_test_spatial.sample(min(2000, len(X_test_spatial)), random_state=RANDOM_STATE)
explainer = shap.TreeExplainer(improved_catboost)
shap_values = explainer.shap_values(shap_sample)

shap.summary_plot(shap_values, shap_sample, show=False)
plt.title("SHAP Summary — Final Improved CatBoost")
plt.tight_layout()
plt.show()

shap.summary_plot(shap_values, shap_sample, plot_type="bar", show=False)
plt.title("SHAP Feature Importance (mean |SHAP value|)")
plt.tight_layout()
plt.show()

# Cell 31
# 4-6. ROC Curve, Precision-Recall Curve, Confusion Matrix — Baseline vs Final model
baseline_cb_model = baseline_fitted_models["CatBoost (Baseline)"]
baseline_proba = baseline_cb_model.predict_proba(X_test)[:, 1]

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# ROC
for label, proba in [("Baseline CatBoost", baseline_proba), ("Improved CatBoost", improved_y_proba)]:
    fpr, tpr, _ = roc_curve(y_test, proba)
    axes[0].plot(fpr, tpr, label=f"{label} (AUC={roc_auc_score(y_test, proba):.3f})")
axes[0].plot([0, 1], [0, 1], "k--", alpha=0.4)
axes[0].set_title("ROC Curve")
axes[0].set_xlabel("False Positive Rate")
axes[0].set_ylabel("True Positive Rate")
axes[0].legend()

# Precision-Recall
for label, proba in [("Baseline CatBoost", baseline_proba), ("Improved CatBoost", improved_y_proba)]:
    prec, rec, _ = precision_recall_curve(y_test, proba)
    axes[1].plot(rec, prec, label=label)
axes[1].set_title("Precision-Recall Curve")
axes[1].set_xlabel("Recall")
axes[1].set_ylabel("Precision")
axes[1].legend()

# Confusion Matrix (final model)
sns.heatmap(
    improved_cm, annot=True, fmt="d", cmap="Blues",
    xticklabels=["Non-Fatal (0)", "Fatal (1)"],
    yticklabels=["Non-Fatal (0)", "Fatal (1)"], ax=axes[2]
)
axes[2].set_title("Confusion Matrix — Final Improved CatBoost")
axes[2].set_xlabel("Predicted")
axes[2].set_ylabel("Actual")

plt.tight_layout()
plt.show()

# Cell 32
# 7. Spatial Cluster Visualization (scatter over lat/lon as a lightweight UK map)
plot_coords = df.loc[X_train.index, ["latitude", "longitude"]].copy()
plot_coords["cluster"] = spatial_cluster_train.values
plot_coords = plot_coords[plot_coords["cluster"] != -1]  # drop "unknown location" sentinel

fig, ax = plt.subplots(figsize=(7, 9))
scatter = ax.scatter(
    plot_coords["longitude"], plot_coords["latitude"],
    c=plot_coords["cluster"], cmap="tab20", s=4, alpha=0.5
)
ax.set_title(f"Spatial Clusters (KMeans, k={N_SPATIAL_CLUSTERS}) — Training Records")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_aspect("equal")
plt.colorbar(scatter, ax=ax, label="Cluster ID")
plt.tight_layout()
plt.show()

# Cell 34
# Error rate by key variables (original, human-readable categories from `df`, aligned to X_test.index)
error_df = df.loc[X_test.index, ["weather_conditions", "road_type", "light_conditions", "urban_or_rural_area"]].copy()
error_df["actual"] = y_test.values
error_df["predicted"] = improved_y_pred
error_df["correct"] = error_df["actual"] == error_df["predicted"]
error_df["spatial_cluster"] = spatial_cluster_test.values

for col in ["weather_conditions", "road_type", "light_conditions", "urban_or_rural_area"]:
    error_rate = (1 - error_df.groupby(col)["correct"].mean()).sort_values(ascending=False)
    print(f"\nError rate by {col}:")
    print(error_rate.round(4))

# Cell 35
# Spatial bias check: accuracy per spatial_cluster (excludes the "unknown location" sentinel)
cluster_perf = error_df[error_df["spatial_cluster"] != -1].groupby("spatial_cluster").agg(
    accuracy=("correct", "mean"),
    n=("correct", "size"),
    fatal_rate=("actual", "mean"),
).reset_index().sort_values("accuracy")

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(cluster_perf["spatial_cluster"].astype(str), cluster_perf["accuracy"], color="mediumseagreen")
ax.axhline(improved_metrics["Accuracy"], color="black", linestyle="--", label="Overall test accuracy")
ax.set_xlabel("Spatial Cluster")
ax.set_ylabel("Accuracy")
ax.set_title("Final Improved CatBoost — Accuracy by Spatial Cluster (bias check)")
ax.legend()
plt.tight_layout()
plt.show()

print(cluster_perf.round(4).to_string(index=False))

