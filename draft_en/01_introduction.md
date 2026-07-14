# 1. Introduction

Traffic accidents remain a severe public safety challenge worldwide. When analyzing collision data, predicting accident severity helps authorities deploy timely interventions and allocate medical resources where they are most needed. We noticed that while conventional machine learning methods frequently predict crash severity using weather conditions, road types, and lighting, they often struggle to exploit direct spatial information—such as precise geographic coordinates or the localized clustering of accidents.

Fatal traffic risks do not distribute uniformly across a map. We hypothesized that variables like speed limits, urban versus rural zoning, and proximity to medical facilities correlate heavily with the exact accident location. Yet standard baseline models lack explicit features to represent this geographic variance natively.

To test whether explicit location data improves prediction, we developed a modified CatBoost framework integrating spatial feature engineering on a United Kingdom traffic accident dataset. By feeding latitude and longitude coordinates into the pipeline, we extracted spatial clusters and city-distance metrics. We selected CatBoost specifically to exploit its native capacity for processing the resulting high-cardinality categorical variables.

Our primary research question asks: Does integrating explicit spatial features—specifically coordinate clustering and distances to major cities—actually improve a CatBoost model's ability to predict traffic fatalities compared to standard machine learning baselines?
