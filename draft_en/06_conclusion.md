# 6. Conclusion

We developed and evaluated a machine learning pipeline to predict traffic accident severity across the United Kingdom, specifically attempting to improve performance by engineering explicit spatial risk features. 

Our benchmarking confirmed that modern Gradient Boosted Decision Trees—CatBoost, XGBoost, and LightGBM—easily outcompete linear models and simple decision trees for this specific collision data. CatBoost handled the dataset's high-cardinality categorical variables particularly well. Yet our core experiment yielded a clear negative result: injecting explicit spatial clusters and city-distance metrics into the model failed to generate any statistically significant performance gains. Extensive missing coordinate data (54%) crippled the spatial signal, while existing variables like speed limits and administrative zones already captured the necessary geographic context.

For traffic safety authorities allocating resources, this suggests that extracting complex spatial geometries from crash records is unnecessary if those records already contain basic administrative and roadway descriptors. 

Future research should revisit this spatial framework using datasets with near-total coordinate completeness. We suspect that combining precise, unbroken spatial data with temporal variables—or mining the raw textual narratives from police crash reports—could eventually unlock the predictive gains we failed to realize here.
