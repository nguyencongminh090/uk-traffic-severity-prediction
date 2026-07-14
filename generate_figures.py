import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score, precision_recall_curve
from sklearn.cluster import KMeans
from catboost import CatBoostClassifier
import shap

# Settings
RANDOM_STATE = 42
TARGET = "collision_severity"
N_SPATIAL_CLUSTERS = 20
GRID_SIZE_DEGREES = 0.5

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

# APA Styling
plt.style.use('default')
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 12,
    'axes.grid': False,
    'axes.spines.top': False,
    'axes.spines.right': False,
})
COLORBLIND_PALETTE = ['#332288', '#117733', '#44AA99', '#88CCEE', '#DDCC77', '#CC6677', '#AA4499', '#882255']
PRIMARY_COLOR = '#0077BB'

os.makedirs("figures", exist_ok=True)

# 1. Load Data & Preprocess
print("Loading data...")
df = pd.read_csv("dataset/UK_accidents_balanced.csv")
df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

leak_cols = ["enhanced_severity_collision", "collision_injury_based", "collision_adjusted_severity_serious", "collision_adjusted_severity_slight"]
id_cols = ["collision_index", "collision_ref_no", "date", "time", "local_authority_ons_district", "local_authority_highway", "local_authority_highway_current", "lsoa_of_accident_location"]
df_model = df.drop(columns=[c for c in leak_cols + id_cols if c in df.columns])

num_cols = df_model.select_dtypes(include=[np.number]).columns.tolist()
num_cols.remove(TARGET)
cat_cols = df_model.select_dtypes(exclude=[np.number]).columns.tolist()

for c in num_cols:
    df_model[c] = df_model[c].fillna(df_model[c].median())
for c in cat_cols:
    df_model[c] = df_model[c].fillna("missing")

from sklearn.preprocessing import LabelEncoder
for c in cat_cols:
    df_model[c] = LabelEncoder().fit_transform(df_model[c].astype(str))

df_model[TARGET] = df_model[TARGET].replace({2: 0, 3: 0})

X = df_model.drop(columns=[TARGET])
y = df_model[TARGET]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)

# 2. Spatial Feature Engineering
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))

train_coords = df.loc[X_train.index, ["latitude", "longitude"]].dropna()
kmeans_spatial = KMeans(n_clusters=N_SPATIAL_CLUSTERS, random_state=RANDOM_STATE, n_init=10).fit(train_coords)

def assign_spatial_cluster(idx):
    coords = df.loc[idx, ["latitude", "longitude"]]
    valid = coords.notna().all(axis=1)
    cluster = pd.Series(-1, index=idx, name="spatial_cluster")
    if valid.any(): cluster.loc[valid] = kmeans_spatial.predict(coords.loc[valid])
    return cluster.astype(int)

def assign_grid_region_id(idx):
    coords = df.loc[idx, ["latitude", "longitude"]]
    valid = coords.notna().all(axis=1)
    lat_bin = (coords["latitude"] // GRID_SIZE_DEGREES).astype("Int64").astype(str)
    lon_bin = (coords["longitude"] // GRID_SIZE_DEGREES).astype("Int64").astype(str)
    return (lat_bin + "_" + lon_bin).where(valid, "unknown").rename("grid_region_id")

def assign_spatial_zone(idx):
    coords = df.loc[idx, ["latitude", "longitude"]]
    valid = coords.notna().all(axis=1)
    dists = pd.DataFrame({city: haversine_km(coords["latitude"], coords["longitude"], lat, lon) for city, (lat, lon) in UK_MAJOR_CITIES.items()})
    nearest_dist = dists.min(axis=1).where(valid, -1).rename("dist_to_nearest_city_km")
    nearest_zone = dists.fillna(1e9).idxmin(axis=1).where(valid, "unknown").rename("nearest_city_zone")
    return nearest_dist, nearest_zone

spatial_cluster_train = assign_spatial_cluster(X_train.index)
spatial_cluster_test = assign_spatial_cluster(X_test.index)
grid_id_train = assign_grid_region_id(X_train.index)
grid_id_test = assign_grid_region_id(X_test.index)

cluster_density_map = (spatial_cluster_train.value_counts() / len(spatial_cluster_train)).to_dict()
cluster_density_train = spatial_cluster_train.map(cluster_density_map).rename("cluster_density")
cluster_density_test = spatial_cluster_test.map(cluster_density_map).fillna(0).rename("cluster_density")

dist_city_train, zone_train = assign_spatial_zone(X_train.index)
dist_city_test, zone_test = assign_spatial_zone(X_test.index)

X_train_spatial = X_train.drop(columns=["latitude", "longitude"]).copy()
X_test_spatial = X_test.drop(columns=["latitude", "longitude"]).copy()

spatial_feature_frames = {
    "spatial_cluster": (spatial_cluster_train.astype(str), spatial_cluster_test.astype(str)),
    "grid_region_id": (grid_id_train, grid_id_test),
    "cluster_density": (cluster_density_train, cluster_density_test),
    "dist_to_nearest_city_km": (dist_city_train, dist_city_test),
    "nearest_city_zone": (zone_train, zone_test),
}
for col, (tr, te) in spatial_feature_frames.items():
    X_train_spatial[col] = tr.values
    X_test_spatial[col] = te.values

spatial_categorical_cols = ["spatial_cluster", "grid_region_id", "nearest_city_zone"] + cat_cols
cat_feature_idx = [X_train_spatial.columns.get_loc(c) for c in spatial_categorical_cols if c in X_train_spatial.columns]

# 3. Train Models
print("Training Baseline CatBoost...")
baseline_model = CatBoostClassifier(iterations=500, depth=8, learning_rate=0.05, loss_function="Logloss", eval_metric="F1", verbose=False, random_seed=RANDOM_STATE)
baseline_model.fit(X_train, y_train)
baseline_proba = baseline_model.predict_proba(X_test)[:, 1]

print("Training Final Improved CatBoost...")
X_tr_sub, X_val, y_tr_sub, y_val = train_test_split(X_train_spatial, y_train, test_size=0.15, random_state=RANDOM_STATE, stratify=y_train)
best_params = {"depth": 8, "learning_rate": 0.05, "l2_leaf_reg": 5}
improved_model = CatBoostClassifier(iterations=1500, loss_function="Logloss", eval_metric="AUC", random_seed=RANDOM_STATE, verbose=False, **best_params)
improved_model.fit(X_tr_sub, y_tr_sub, eval_set=(X_val, y_val), cat_features=cat_feature_idx, early_stopping_rounds=50, use_best_model=True)
improved_pred = improved_model.predict(X_test_spatial)
improved_proba = improved_model.predict_proba(X_test_spatial)[:, 1]
improved_cm = confusion_matrix(y_test, improved_pred, labels=[0, 1])

# --- GENERATE FIGURES ---

print("Generating Fig 1: Spatial Clusters...")
plot_coords = df.loc[X_train.index, ["latitude", "longitude"]].copy()
plot_coords["cluster"] = spatial_cluster_train.values
plot_coords = plot_coords[plot_coords["cluster"] != -1]

fig1, ax1 = plt.subplots(figsize=(6, 8))
# Use viridis for accessibility
scatter = ax1.scatter(plot_coords["longitude"], plot_coords["latitude"], c=plot_coords["cluster"], cmap="viridis", s=4, alpha=0.6)
ax1.set_title("Spatial Clusters (KMeans, k=20)")
ax1.set_xlabel("Longitude")
ax1.set_ylabel("Latitude")
ax1.set_aspect("equal")
plt.colorbar(scatter, ax=ax1, label="Cluster ID")
fig1.tight_layout()
fig1.savefig("figures/fig01_spatial_clusters.pdf", format="pdf", bbox_inches="tight")
plt.close(fig1)


print("Generating Fig 2: Performance Metrics...")
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 4.5))

# ROC
for i, (label, proba) in enumerate([("Baseline CatBoost", baseline_proba), ("Improved CatBoost", improved_proba)]):
    fpr, tpr, _ = roc_curve(y_test, proba)
    axes2[0].plot(fpr, tpr, label=f"{label} (AUC={roc_auc_score(y_test, proba):.3f})", color=COLORBLIND_PALETTE[i*3])
axes2[0].plot([0, 1], [0, 1], "k--", alpha=0.4)
axes2[0].set_title("ROC Curve")
axes2[0].set_xlabel("False Positive Rate")
axes2[0].set_ylabel("True Positive Rate")
axes2[0].legend()

# Precision-Recall
for i, (label, proba) in enumerate([("Baseline CatBoost", baseline_proba), ("Improved CatBoost", improved_proba)]):
    prec, rec, _ = precision_recall_curve(y_test, proba)
    axes2[1].plot(rec, prec, label=label, color=COLORBLIND_PALETTE[i*3])
axes2[1].set_title("Precision-Recall Curve")
axes2[1].set_xlabel("Recall")
axes2[1].set_ylabel("Precision")
axes2[1].legend()

# Confusion Matrix
sns.heatmap(improved_cm, annot=True, fmt="d", cmap="Blues", cbar=False,
            xticklabels=["Non-Fatal", "Fatal"], yticklabels=["Non-Fatal", "Fatal"], ax=axes2[2])
axes2[2].set_title("Confusion Matrix (Improved)")
axes2[2].set_xlabel("Predicted")
axes2[2].set_ylabel("Actual")
# Fix borders for heatmap
for _, spine in axes2[2].spines.items():
    spine.set_visible(True)

fig2.tight_layout()
fig2.savefig("figures/fig02_performance_metrics.pdf", format="pdf", bbox_inches="tight")
plt.close(fig2)


print("Generating Fig 3: Feature Importance...")
final_importance = pd.Series(improved_model.get_feature_importance(), index=X_train_spatial.columns).sort_values(ascending=False)
fig3, ax3 = plt.subplots(figsize=(8, 7))
final_importance.head(20).sort_values().plot.barh(ax=ax3, color=PRIMARY_COLOR, width=0.7)
ax3.set_title("Top 20 Features by CatBoost Importance")
ax3.set_xlabel("Importance Score")
ax3.grid(axis='x', linestyle='--', alpha=0.7)
fig3.tight_layout()
fig3.savefig("figures/fig03_feature_importance.pdf", format="pdf", bbox_inches="tight")
plt.close(fig3)


print("Generating Fig 4: SHAP Summary...")
shap_sample = X_test_spatial.sample(min(2000, len(X_test_spatial)), random_state=RANDOM_STATE)
explainer = shap.TreeExplainer(improved_model)
shap_values = explainer.shap_values(shap_sample)

fig4 = plt.figure(figsize=(9, 6))
shap.summary_plot(shap_values, shap_sample, show=False)
plt.title("SHAP Summary Plot")
fig4.tight_layout()
fig4.savefig("figures/fig04_shap_summary.pdf", format="pdf", bbox_inches="tight")
plt.close(fig4)

print("All figures generated successfully.")
