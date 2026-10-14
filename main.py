import laspy
import numpy as np
from numpy.lib.recfunctions import append_fields
from scipy.spatial import cKDTree

las = laspy.read(r"data\matched_las\q48121H7311.laz")

las_points = las.points.array
data = np.zeros(len(las_points))
las_points = append_fields(las_points, "height_above_ground", data)
class_1_mask = las.classification == 1
class_2_mask = las.classification == 2
dataset_1 = np.vstack((las.x, las.y, las.z)).transpose()
dataset_1 = dataset_1[class_1_mask]
dataset_2 = np.vstack((las.x, las.y, las.z)).transpose()
dataset_2 = dataset_2[class_2_mask]
tree = cKDTree(dataset_2)
k_neighbors = 4
distances, indices = tree.query(dataset_1[100], k=k_neighbors)
print("stop")
