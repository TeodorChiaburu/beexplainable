import scipy.io
import numpy as np
import pickle
from sklearn.decomposition import PCA

# Read ResNet activations from numpy file
mat_activations = np.load('../models/all/6_species/ResNet50_iNat_masked_bbox_6spec_2/Complete_Activations_insects.npy')

# Only keep 2048 activation points from the final CNN layer (java algorithm crashes when run on all activations)
mat_activations = mat_activations[:, -2048:]

reduce_dims, compute_new_pca = True, False
# Reduce dimensions with PCA
if reduce_dims:
    if compute_new_pca:
        pca = PCA(n_components = 50, whiten = True)
        res_concepts_pca = pca.fit_transform(mat_activations)
        with open('../models/all/6_species/ResNet50_iNat_masked_bbox_6spec_2/PCA_final_insects.pickle', 'wb') as f:
           pickle.dump(pca, f)
    else: # If already stored, load PCA projector
        with open('../models/all/6_species/ResNet50_iNat_masked_bbox_6spec_2/PCA_final_insects.pickle', 'rb') as f:
            pca = pickle.load(f)
        res_concepts_pca = pca.transform(mat_activations)

# Only keep top 10 PCs
res_concepts_pca = res_concepts_pca[:, :10]

labels = 30*[0.0] + 30*[1.0] + 30*[2.0] # labels were ordered alphabetically, see folder /Concepts_Bombus_vs_Andrena_StabDiff
scipy.io.savemat('../models/all/6_species/ResNet50_iNat_masked_bbox_6spec_2/Final_Activations_PCA10_insects.mat',
                 {'points': res_concepts_pca, 'labels': labels})