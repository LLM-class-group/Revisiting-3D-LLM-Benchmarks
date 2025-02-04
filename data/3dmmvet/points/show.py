import numpy as np
from open3d import*

source_data = np.load('000.npy')[:,0:3]  #10000x3
point_cloud = open3d.geometry.PointCloud()
point_cloud.points = open3d.utility.Vector3dVector(source_data)
open3d.visualization.draw_geometries([point_cloud])
