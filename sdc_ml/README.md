### An investigation of automatic inference of Skydiving stages from sensor data (Gps, Barometer)


#### The problem
A skydiving trip is split into the following activities in order: walking --> plane --> free-fall --> canopy --> walking. The problem is the following: given sensor data collected during a skydiving trip can we assign a label on each datapoint depending on the activity that was taking place at the time?

The data are of the following form:
 - Gps datapoint: (timepoint, latitude, longitude)
 - Barometer datapoint: (timepoint, altitude)

What attributes should we use?
Vertical and ground speeds should be able to distinguish between the stages.

An unsupervised method would be the best choice here so we started with the simplest k-means one. In terms of kmeans our goal becomes to cluster the data-points into k=4 groups (walking, plane, free-fall, canopy). It would also be interesting to experiment with other methods.

#### Code
- `data_processing.py` gets the data and computes the speeds
- `ml.py` has the implementation of a simple k-means clustering algorithm
- `utils.py` has some utilities for plotting, post-processing (removing outliers , finding the time intervals of the clusters etc.)



