"""Visualize BBox for a CUB image"""

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

# Read one example image from CUB
cub_ex_name = 'Black_Footed_Albatross_0002_55'
im = np.array( Image.open('../figures/' + cub_ex_name + '.jpg') )

# BBox coords from CUB example
xmin, ymin, w, h = 14.0, 112.0, 388.0, 186.0

plt.imshow(im)
plt.gca().add_patch(Rectangle((xmin, ymin), w, h,
                    edgecolor='red', facecolor='none', lw=2))
plt.title(cub_ex_name, fontsize = 15)
plt.xlabel('(xmin, ymin, w, h) = (' + str(xmin) + ', ' + str(ymin) + ', ' + \
                                        str(w) + ', ' + str(h) + ')')
plt.savefig('../figures/' + cub_ex_name + '_bbox.jpg', bbox_inches='tight')
plt.show()