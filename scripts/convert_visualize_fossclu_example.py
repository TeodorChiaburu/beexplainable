import scipy.io
import numpy as np
import matplotlib.pyplot as plt

mat_before = scipy.io.loadmat('../../FOSSCLU/example.mat')
mat_after  = scipy.io.loadmat('../../FOSSCLU/example_result.mat')

original_points = mat_before['test_r_12d_5c_2']
original_labels = mat_before['test_r_12d_5c_2_gold'][0]
projected_points = mat_after['points'][:, :2]
rot_mat = mat_after['rot_matrix']
test_projected_points = np.matmul(rot_mat.T, original_points.T).T[:, :2]
projected_labels = mat_after['labels'][0] # they just get permuted

##############################
# There are 5 clusters in total
# The Algorithm found a proper 2D-subspace where these clusters are well separated.
# To visualize the projection, filter the first two rows of the projected matrix
# and apply labels as in returned label vector
k = 5
spec_col = ['b', 'r', 'darkgreen', 'orange', 'black']
classes = ['C1', 'C2', 'C3', 'C4', 'C5']

fig = plt.figure(figsize = (15,10))
for i in range(k):
  plt.scatter(x = projected_points[np.where(np.array(projected_labels) == i), 0],
              y = projected_points[np.where(np.array(projected_labels) == i), 1],
              marker = 'o', c = spec_col[i])
plt.legend(classes, fontsize = 15, markerscale = 2)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.title('Returned projected points', fontsize = 15)
plt.grid()
plt.show()

fig = plt.figure(figsize = (15,10))
for i in range(k):
  plt.scatter(x = test_projected_points[np.where(np.array(original_labels) == i), 0],
              y = test_projected_points[np.where(np.array(original_labels) == i), 1],
              marker = 'o', c = spec_col[i])
plt.legend(classes, fontsize = 15, markerscale = 2)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.title('Recomputed projected points', fontsize = 15)
plt.grid()
plt.show()