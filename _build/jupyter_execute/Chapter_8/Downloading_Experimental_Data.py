#!/usr/bin/env python
# coding: utf-8

# # Downloading Experimental Data 

# This section will serve as a turorial on how to access and downlaod experimental data from the Allen Brain Mouse Connectivity Atlas. In this tutorial you will learn to download metadata by transgenic line and by injection struture. You will also learn about the importance of structure sets as well as the StructureTree class. By the end of this tutorial you will be ready to use this downloaded data for possible analyses.  

# In[1]:


# Import common packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')
print('Packages imported.')


# To work with the connectivity data through the SDK, we first need to `import` the [MouseConnectivityCache class](https://alleninstitute.github.io/AllenSDK/connectivity.html). This module provides metadata about the mouse connectivty database and will enable us to work with the data.

# In[2]:


# Import the MouseConnectivityCache
import allensdk
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache

# Create an instance of the class and assign it to a variable, mcc
mcc = MouseConnectivityCache(manifest_file='connectivity/mouse_connectivity_manifest.json')
print(mcc)


# ## Download experimental metadata by transgenic line

# Now that we have our instance of the mouse connectivity cache, we can start downloading our experimental metadata. To do this, we will call `get_experiments()` on our connectivity instance. We'll use the argument `dataframe=True` to automatically make this a dataframe when it is created. 

# In[3]:


# Gather all the experiments with transgenic as well as wildtype mice
mouse_exp_df = mcc.get_experiments(dataframe=True)
mouse_exp_df.head()


# This gives us metadata on all the expereiments in the dataset. Alternatively, you can specify within the method wether you would like to filter certain experiments by `transgenic_line`. Let's take a look at what trangenic lines are available to us. 

# In[4]:


transgenic_lines = mouse_exp_df['transgenic_line'].unique()
print(transgenic_lines)


# Let's start by creating a dataframe that only contains experiments with the first three Cre lines in the list above *(Penk-IRES2-Cre-neo, Gabrr3-Cre_KC112, Hdc-Cre_IM1)*. You can change the Cre lines by changing the values in the list assigned to `transgenic_lines`. Remember to copy the Cre line of interest exactly, including the single quotes. We'll then use this list in the argument `cre = ` in our call to `get_experiments`.

# In[5]:


# Choose your Cre lines
transgenic_lines = ['Penk-IRES2-Cre-neo','Gabrr3-Cre_KC112','Hdc-Cre_IM1'] 

# Filter experiments from only the first 3 cre lines 
transgenic_line_df = mcc.get_experiments(cre = transgenic_lines, dataframe=True)

# Print the length of our dataframe 
print('There are' + ' ' + str(len(transgenic_line_df)) + ' ' + 'experiments in these Cre lines: ' + str(transgenic_lines))

transgenic_line_df.head()


# ## Download experimental metadata by injection structure 

# We can also filter out the experiments by the `injection_structure_ids`. If the IDs of the injection structures are already known, one can input the list of ID numbers to filter out the experiments as so:

# In[6]:


# Primary Motor Area experiments have ID 985
MOp_df = mcc.get_experiments(injection_structure_ids = [985], dataframe=True)
MOp_df.head()


# ## Get structure IDs
# 
# In order to use the `injection_structure_ids` argument above, you need the structure IDs. The MouseConnectivityCache has a method for retrieving the adult mouse structure tree as an StructureTree class instance. The StructureTree class has many methods that allows you to access lists of brain structures through their ID, name, acronym, and many other properties. This is done by executing the `get_structure_tree()` method on your MouseConnectivityCache instance (`mcc`).
# 
# Below we will access information on the hypothalamus via its name by calling `get_structures_by_name()` on our StructureTree instance. 

# In[7]:


# Grab the StructureTree instance
structure_tree = mcc.get_structure_tree()

# Get info on hypothalamus by its name 
hypothalamus = structure_tree.get_structures_by_name(['Hypothalamus'])[0]
hypothalamus


# This gives us a dictionary with metadata about our brain structure of interest. 

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


# ## Additional Resources 

# For more information on the different methods to access information on brain structures as well as the StructureTree class, visit <a href="https://alleninstitute.github.io/AllenSDK/allensdk.core.structure_tree.html">here</a>. 

# In[ ]:




