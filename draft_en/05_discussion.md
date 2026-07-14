# 5. Discussion

Traffic collision severity varies wildly across different geographies. A crash in a rural zone far from emergency medical services carries a different fatality risk profile than a low-speed collision in a dense urban grid. We designed the spatial feature engineering pipeline specifically to capture this geographic variance. By feeding the model distinct coordinate clusters (`spatial_cluster`) and exact distances to major cities (`dist_to_nearest_city_km`), we expected CatBoost's target-statistic engine to map specific geographic zones to their underlying empirical fatality rates.

The results entirely rejected our hypothesis. As the statistical tests in Section 4 demonstrated, the spatial features failed to improve the model's predictive power. 

We attribute this failure to two overlapping data realities. First, the dataset suffers from severe coordinate sparsity. With 54% of the geographic data missing and masked by a sentinel value, the spatial signal became heavily diluted. The model likely learned to ignore the spatial clusters because they were absent for more than half the training examples. 

Second, the raw dataset already contained variables like `police_force`, `urban_or_rural_area`, and `speed_limit`. Our results suggest that these existing administrative and environmental descriptors already act as highly efficient spatial proxies. Once the model splits a decision tree on a 70-mph rural road governed by a specific regional police force, it has already effectively localized the accident. Feeding it the exact latitude and longitude of that road provides redundant information. 

While the engineered spatial features did not boost predictive accuracy, this negative result clarifies a practical engineering constraint. Before researchers invest massive computational overhead into calculating Haversine distances and KMeans clusters for traffic data, they must ensure the raw geographic data is nearly complete. If half the coordinates are missing, standard administrative variables provide a perfectly adequate spatial proxy.
