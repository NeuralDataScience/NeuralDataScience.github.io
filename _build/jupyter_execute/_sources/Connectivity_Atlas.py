#!/usr/bin/env python
# coding: utf-8

# # Connectivity Atlas 

# This secion will serve as an intorduction to the Allen Brain Mouse Connectivity Atlas. 

# In[1]:


# Import necessary Toolkits
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')
import requests


# Much like before, we will `import` the MouseConnectivityCache module. This provides us tools to get information on the mouse connectivty database. We can then create an instance of our cache.

# In[2]:


#Import MouseConnectivityCache and convert it to mcc
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache
mcc = MouseConnectivityCache(manifest_file='connectivity/mouse_connectivity_manifest.json')
print(mcc)


# ## Download experimental metadata by trangenic line

# Now that we have our instance of the mouse connectivity cache, we can start downloading our experimental metadata. To do this, we will call `get_experiments()` on our connectivity instance. 

# In[3]:


#Gather all the experiments with Cre and WildType
all_experiments = mcc.get_experiments(dataframe=True)
mouse_exp_df = pd.DataFrame(all_experiments)
mouse_exp_df.head()


# This gives us metadata on all the expereiments in the dataset. Alternatively, you can specify within the method wether you would like to filter certain experiments by `transgenic_line`. Let's take a look at what trangenic lines are availabe to us. 

# In[4]:


trangenic_lines = mouse_exp_df['transgenic_line'].unique()
trangenic_lines


# Let's start by creating a dataframe that only contians experiments with the first three cre lines in the list above *(Penk-IRES2-Cre-neo, Gabrr3-Cre_KC112, Hdc-Cre_IM1)*. Remeber to copy the cre line of interest exactly, including the quotations. 

# In[5]:


# filter experiments from only the first 3 cre lines 
trangenic_line_exps = pd.DataFrame(mcc.get_experiments(cre = ['Penk-IRES2-Cre-neo', 
                                                              'Gabrr3-Cre_KC112', 
                                                              'Hdc-Cre_IM1']))

trangenic_line_exps = trangenic_line_exps.set_index('id')

# print the length of our dataframe 
print('The Dataframe is' + ' ' + str(len(trangenic_line_exps)) + ' ' + 'entries long')

# confirm the only cre lines are those that were specified 
print(trangenic_line_exps['transgenic_line'].unique())

trangenic_line_exps.head()


# ## Download experimental metadata by injection structure 

# We could also filter out the experiments by the `injection_structure_ids`. If the IDs of the injection structures are already known, one can input the list of ID numbers to filter out the experiments as so:

# In[6]:


# Primary Motor Area experiments have ID 985
MOp_df = pd.DataFrame(mcc.get_experiments(injection_structure_ids = [985])).set_index('id')
MOp_df.head()


# MouseConnectivityCache has a method for retrieving the adult mouse structure tree as an StructureTree class instance. The StructureTree class has many methods that allows you to access lists of brain structures through their ID, name, acronym, and many other properties. This is done by executing the `get_structure_tree()` method on your MouseConnectivityCache instance (`mcc`).  Below we will access information on the hypothalamus via its name by calling `get_structures_by_name()` on our StructureTree instance. 

# In[7]:


# grab the StructureTree instance
structure_tree = mcc.get_structure_tree()

# get info on hypothalamus by its name 
hypothalamus = structure_tree.get_structures_by_name(['Hypothalamus'])[0]
hypothalamus


# This gives us a dictionary with metadata about our brain structure of interest. For more inofrmation on the different methods to access information on brain structures, click <a href="https://alleninstitute.github.io/AllenSDK/allensdk.core.structure_tree.html">here</a>. 

# So far, we know that the Primary Motar Area is a brain structure available to us in our experiments, but what about the rest of the brain structures? How do we find what are all the brain structures availabe to us? To do so, we can take a look at the unique values under the `name` column, in our summary of brain structures. 

# **Note:** we will go over structure set ids, `get_structure_sets()`, and the `get_structures_by_set_id()` methods later in this notebook. We will just be using `get_structures_by_set_id()` to access our Summary Structures Data.

# In[8]:


# From the above table, "Brain - Summary Structures" has ID 167587189
summary_structures = structure_tree.get_structures_by_set_id([167587189])
summary_structures_df = pd.DataFrame(summary_structures)

# Determine how many different structures are within our experiments 
structure_name = summary_structures_df['name'].unique()
print("%d Total Available Brain Structures" % len(structure_name))

# print the first 20 brain structures in our data
print(structure_name[:19])


# We know that the Motar Cortex Area has ID 985, but what if we do not know the structure ID? That is not a hard probelm to fix. Like we did earlier, we can access a dictionary of metadata for our structure of interest using our StructureTree helper methods. 

# In[9]:


# get info on Ventral tegmental area by its name 
VTA = structure_tree.get_structures_by_name(['Ventral tegmental area'])[0]

# specify the strucure id by indexixing into the 'id' of `VTA`
VTA_df = pd.DataFrame(mcc.get_experiments(injection_structure_ids = [VTA['id']]))
VTA_df.head()


# ## Putting it All Together 

# Below is an example of how we can combine both filtering by Cre line and by injection structure to get a more refined set of data.

# In[10]:


# select cortical experiments 
isocortex = structure_tree.get_structures_by_name(['Isocortex'])[0]

# same as before, but restrict the cre line
rbp4_cortical_experiments = mcc.get_experiments(cre=[ 'Rbp4-Cre_KL100' ], 
                                                injection_structure_ids=[isocortex['id']])

# convert to a dataframe 
rbp4_cortical_df = pd.DataFrame(rbp4_cortical_experiments).set_index('id')
rbp4_cortical_df.head()


# As a convenience, structures are grouped in to named collections called "structure sets". These sets can be used to quickly gather a useful subset of structures from the tree. The criteria used to define structure sets are eclectic; a structure set might list:
# 
# - structures that were used in a particular project.
# - structures that coarsely partition the brain.
# - structures that bear functional similarity.
# 
# To see only structure sets relevant to the adult mouse brain, use the StructureTree:

# In[11]:


from allensdk.api.queries.ontologies_api import OntologiesApi

oapi = OntologiesApi()

# get the ids of all the structure sets in the tree
structure_set_ids = structure_tree.get_structure_sets()

# query the API for information on those structure sets
pd.DataFrame(oapi.get_structure_sets(structure_set_ids))


# As you can see from the table above, there are many different sets that our available brain structures can be grouped in. Below we will look into our Mouse Connectivity Summary data by specifying the set ID using the `get_structure_by_set_id()` method. 

# In[12]:


# From the above table, "Mouse Connectivity - Summary" has id 687527945
summary_connectivity = structure_tree.get_structures_by_set_id([687527945])
summary_connectivity_df = pd.DataFrame(summary_connectivity)
summary_connectivity_df.head()


# ## Download and visualize gridded projection signal volumes (raw data)

# The ProjectionStructureUnionizes API data tells you how much signal there was in a given structure and experiment. It contains the density of projecting signal, volume of projecting signal, and other information. MouseConnectivityCache provides methods for querying and storing this data. To access to this signal projection data, you must call the `get_structure_unionizes()` method on our MouseConnectivityCache instance.

# For more information on the outputs of `get_structure_unionizes()` please visit <a href="https://alleninstitute.github.io/AllenSDK/unionizes.html">here</a>. For documentation on `get_structure_unionizes()` and other MouseConnectivityCache helper methods, please click <a href="https://alleninstitute.github.io/AllenSDK/allensdk.core.mouse_connectivity_cache.html">here</a>

# In[13]:


# find wild-type injections into primary motor cortex 
VISp = structure_tree.get_structures_by_name(['Primary visual area'])[0]
VISp_experiments = mcc.get_experiments(cre=False, 
                                       injection_structure_ids=[VISp['id']])
print("%d Primary visual area experiments" % len(VISp_experiments))


structure_unionizes = mcc.get_structure_unionizes(experiment_ids = [exp['id'] for exp in 
                                                    VISp_experiments], 
                                                  is_injection=False,
                                                  structure_ids=[isocortex['id']],
                                                  include_descendants=True)

print("%d Primary visual area non-injection, cortical structure unionizes" % len(structure_unionizes))


# In[14]:


structure_unionizes.head()


# This is a very large dataframe filled with all the signal projection data for our experiments of interest. We can filter this like any other dataframe. For example, filter the dataframe to only include experiments with a large projection density and volume. For the purposes of this lesson, we will consider any `projection_density` and `volume` greater than 0.5 to be *large*. 

# In[15]:


# Only include experiments that have a large projection density 
dense_unionizes = structure_unionizes[structure_unionizes['projection_density'] > .5 ]

# Only include experiments from the dense dataframe that have a large volume 
large_unionizes = dense_unionizes[dense_unionizes['volume'] > .5 ]

# create a dataframe that contains metadata from structure IDs within our large and dense df
large_structures = pd.DataFrame(structure_tree.nodes(large_unionizes['structure_id']))

print("%d large, dense, cortical, non-injection unionizes, %d structures" % ( len(large_unionizes), len(large_structures) ))

# return all large, dense, cortical, structure unionizes 
print(large_structures['name'])

large_unionizes


# ## Build a structure-to-structure matrix of projection signal values

# The MouseConnectivityCache class provides a helper method for converting ProjectionStructureUnionize data for a set of experiments and structures into a matrix. This is done by calling `get_projection_matrix` on our MouseConnectivityCache instance. The method can take in arguements `experiment_ids`, `projection_structure_ids`, `hemisphere_ids`, `parameter`, and `dataframe` to further specify your matrix.

# The code below demonstrates how to make a matrix of projection density values in auditory sub-structures for cre-negative VISp experiments.

# In[16]:


# collect all experiment IDs from primary visual area experiments 
visp_experiment_ids = [ exp['id'] for exp in VISp_experiments ]

ctx_children = structure_tree.child_ids( [isocortex['id']] )[0]

# create your projection matrix 
pm = mcc.get_projection_matrix(experiment_ids = visp_experiment_ids, 
                               projection_structure_ids = ctx_children,
                               hemisphere_ids= [2], # right hemisphere, ipsilateral
                               parameter = 'projection_density')


row_labels = pm['rows'] # these are just experiment ids
column_labels = [ col['label'] for col in pm['columns'] ] 
matrix = pm['matrix']

# plot your matrix 
fig, ax = plt.subplots(figsize=(15,15))
heatmap = ax.pcolor(matrix, cmap=plt.cm.afmhot)

# put the major ticks at the middle of each cell
ax.set_xticks(np.arange(matrix.shape[1])+0.5, minor=False)
ax.set_yticks(np.arange(matrix.shape[0])+0.5, minor=False)

ax.set_xlim([0, matrix.shape[1]])
ax.set_ylim([0, matrix.shape[0]])          

# want a more natural, table-like display
ax.invert_yaxis()
ax.xaxis.tick_top()

ax.set_xticklabels(column_labels, minor=False)
ax.set_yticklabels(row_labels, minor=False)
plt.show()


# Using another feature of the MouseConnectivityCache, we can show an example of what an image of fluorescence would look like for a given experiment. The code below demonstrates how you can load the projection density for a particular experiment and plot it to see how it looks.

# In[17]:


# a VTA experiment w/ Cre line Erbb4-T2A-CreERT2
experiment_id = 127867804


# In[18]:


# projection density: number of projecting pixels / voxel volume
pd, pd_info = mcc.get_projection_density(experiment_id)


# In[20]:


# Injection density: number of projecting pixels in injection site / voxel volume
ind, ind_info = mcc.get_injection_density(experiment_id)


# In[21]:


# Data mask:
# Binary mask indicating which voxels contain valid data
dm, dm_info = mcc.get_data_mask(experiment_id)


# In[22]:


template, template_info = mcc.get_template_volume()


# In[23]:


annot, annot_info = mcc.get_annotation_volume()


# In[24]:


# In addition to the annotation volume, you can get binary masks for individual structures
# this is a binary mask for the VTA
VTA_mask, cm_info = mcc.get_structure_mask(314)


# In[25]:


#Compute the maximum intensity projection of the projection data
pd_mip = pd.max(axis=0)
ind_mip = ind.max(axis=0)

#Show that slice of all volumes side-by-side
f, pr_axes = plt.subplots(1, 2, figsize=(15, 6))

pr_axes[0].imshow(pd_mip, cmap='hot', aspect='equal')
pr_axes[0].set_title("VTA Erbb4-T2A-CreERT2-Cre projection density")

pr_axes[1].imshow(ind_mip, cmap='hot', aspect='equal')
pr_axes[1].set_title("VTA Erbb4-T2A-CreERT2-Cre injection site density")

plt.show()


# In[ ]:




