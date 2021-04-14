#!/usr/bin/env python
# coding: utf-8

# # Working with Raw Data 
# 
# This section will serve as a tutorial on how to analyze and visualize data stored in the Allen Brain Mouse Connectivity Atlas. This section will cover how to download and visualize raw data as well as create projection matrices. 
# 
# ## Setup

# In[1]:


# Import common packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')
print('Packages imported.')


# In[2]:


# Import the MouseConnectivityCache
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache

# Create an instance of the class and assign it to a variable, mcc
mcc = MouseConnectivityCache(manifest_file='connectivity/mouse_connectivity_manifest.json')
print(mcc)


# As we showed in [the previous notebook](https://neuraldatascience.github.io/Chapter_8/Downloading_Experimental_Data.html), we can pull experiments based on the transgenic mouse line or the injection site. Below, we'll get a list of experiments where virus was injected into the visual cortex.

# In[3]:


# Grab the StructureTree instance
structure_tree = mcc.get_structure_tree()

# Select cortical experiments 
isocortex = structure_tree.get_structures_by_name(['Isocortex'])[0]
thalamus = structure_tree.get_structures_by_name(['Thalamus'])[0]

# Find injections into primary visual cortex 
VISp = structure_tree.get_structures_by_name(['Primary visual area'])[0]
VISp_experiments = mcc.get_experiments(cre=['Tlx3-Cre_PL56'],injection_structure_ids=[VISp['id']],dataframe=True)
print("%d Primary visual area experiments" % len(VISp_experiments))
VISp_experiments.head()


# ## Plot the projection density for an experiment 
# 
# Before we look at the calculated projection density for multiple brain areas, let's take a look at the raw data. 
# Using a feature of the MouseConnectivityCache, we can show an example of what an image of fluorescence would look like for a given experiment. The code below demonstrates how you can load the projection density for a particular experiment.

# In[4]:


# Define an experiment of interest 
experiment_id = VISp_experiments.index[1]

# Get the projection density: number of projecting pixels / voxel volume
projection_density, pd_info = mcc.get_projection_density(experiment_id)

# Injection density: number of projecting pixels in injection site / voxel volume
ind, ind_info = mcc.get_injection_density(experiment_id)


# Now that we have a `projection_density` object for the entire brain, we can project this onto one plane for visualization. Below, we'll create a maximum intensity image of the projections (left) as well as the injection site (right). 

# In[5]:


#Compute the maximum intensity projection of the projection data
pd_mip = projection_density.max(axis=0)
ind_mip = ind.max(axis=0)

#Show that slice of all volumes side-by-side
f, pr_axes = plt.subplots(1, 2, figsize=(15, 6))

pr_axes[0].imshow(pd_mip, cmap='hot', aspect='equal')
pr_axes[0].set_title(str(experiment_id)+ ' projection density')

pr_axes[1].imshow(ind_mip, cmap='hot', aspect='equal')
pr_axes[1].set_title(str(experiment_id) + ' injection density')

plt.show()


# ## Download and visualize gridded projection signal volumes
# Given the variability in injection sites and virus expression, often, we'll want to look across multiple experiments to see the consistency in projection patterns. To do, we can use the **ProjectStructureUnionizes API**. 
# 
# The ProjectionStructureUnionizes API data tells you how much signal there was in a given structure and experiment. In this data, the "signal" is the fluorescence from our viral tracers. This data contains the density of projecting signal, volume of projecting signal, and other information. [MouseConnectivityCache](https://alleninstitute.github.io/AllenSDK/allensdk.core.mouse_connectivity_cache.html) provides methods for querying and storing this data. To access to this signal projection data, you must call the [`get_structure_unionizes()`](https://alleninstitute.github.io/AllenSDK/unionizes.html) method on our MouseConnectivityCache instance.
# 
# *Note*: Since this is pulling quite a bit of data, it may take a minute or two.

# In[6]:


VISp_expt_IDs = VISp_experiments.index.tolist()

# Download projection signals for structure of interest 
structure_unionizes = mcc.get_structure_unionizes(experiment_ids = VISp_expt_IDs, 
                                                  is_injection=False,
                                                  structure_ids=[isocortex['id']],
                                                  include_descendants=True)

#print("%d Primary visual area non-injection, cortical structure unionizes" % len(structure_unionizes))

structure_unionizes.head()


# As you can see, `structure_unionizes` is a very large dataframe filled with all the signal projection data for our experiments of interest. We can filter this like any other dataframe. For example, we can filter the dataframe to only include experiments with a large projection density and volume. For the purposes of this lesson, we will consider any `projection_density` and `volume` greater than 0.3 to be *large*. 

# In[7]:


# Only include experiments that have a large projection density 
dense_unionizes = structure_unionizes[structure_unionizes['projection_density'] > .1 ]

# Only include experiments from the dense dataframe that have a large volume 
large_unionizes = dense_unionizes[dense_unionizes['volume'] > .1 ]

# create a dataframe that contains metadata from structure IDs within our large and dense df
large_structures = pd.DataFrame(structure_tree.nodes(large_unionizes['structure_id']))

print("%d large, dense, cortical, non-injection unionizes, %d structures" % ( len(large_unionizes), len(large_structures) ))

# return all large, dense, cortical, structure unionizes 
print(large_structures['name'])

large_unionizes.head()


# ## Build a structure-to-structure matrix of projection signal values

# The MouseConnectivityCache class provides a helper method for converting ProjectionStructureUnionize data for a set of experiments and structures into a matrix. This is done by calling [`get_projection_matrix`](https://alleninstitute.github.io/AllenSDK/allensdk.core.mouse_connectivity_cache.html#allensdk.core.mouse_connectivity_cache.MouseConnectivityCache.get_projection_matrix) on our MouseConnectivityCache instance. The method can take in arguements `experiment_ids`, `projection_structure_ids`, `hemisphere_ids`, `parameter`, and `dataframe` to further specify your matrix.
# 
# The code below demonstrates how to make a matrix of projection density values in auditory sub-structures for injections into VISp.

# In[8]:


ctx_children = structure_tree.child_ids([isocortex['id']])[0]

# Create your projection matrix 
pm = mcc.get_projection_matrix(experiment_ids = VISp_expt_IDs, 
                               projection_structure_ids = ctx_children,
                               hemisphere_ids= [2], # right hemisphere, ipsilateral
                               parameter = 'projection_density')

# These are just experiment ids
row_labels = pm['rows'] 

# These are the brain structures 
column_labels = [ col['label'] for col in pm['columns'] ]

matrix = pm['matrix']

# Plot your matrix 
fig, ax = plt.subplots(figsize=(15,15))
heatmap = ax.pcolor(matrix, cmap=plt.cm.afmhot)

# Put the major ticks at the middle of each cell
ax.set_xticks(np.arange(matrix.shape[1])+0.5, minor=False)
ax.set_yticks(np.arange(matrix.shape[0])+0.5, minor=False)

ax.set_xlim([0, matrix.shape[1]])
ax.set_ylim([0, matrix.shape[0]])          

# Want a more natural, table-like display
ax.invert_yaxis()
ax.xaxis.tick_top()

ax.set_xticklabels(column_labels, minor=False)
ax.set_yticklabels(row_labels, minor=False)
plt.show()


# ## Additional Resources 

# For more information on all the functions used to download the projection signals and create the projection matrices, please look at the <a href = 'https://alleninstitute.github.io/AllenSDK/allensdk.core.mouse_connectivity_cache.html'> original documentaion</a>. For information on how to create heat maps like the one created for the flourecense image, please visit the <a href = 'https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.imshow.html'> matplotlib documentation</a>.
