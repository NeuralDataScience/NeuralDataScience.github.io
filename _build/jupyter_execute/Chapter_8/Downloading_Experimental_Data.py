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


# To access the mouse connectivity data through the SDK, we first need to `import` the [MouseConnectivityCache class](https://alleninstitute.github.io/AllenSDK/connectivity.html). This class caches metadata about the mouse connectivty database and provides methods needed to download and analyze the data. For a full list of methods for the Mouse Connectivity Class object, please visit the <a href = 'https://alleninstitute.github.io/AllenSDK/allensdk.core.mouse_connectivity_cache.html'> original documentation</a>.

# In[2]:


# Import the MouseConnectivityCache
import allensdk
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache

# Create an instance of the class and assign it to a variable, mcc
mcc = MouseConnectivityCache(manifest_file='manifest.json')
print(mcc)


# ## Download experimental metadata by transgenic line

# Now that we have our instance of the mouse connectivity cache, we can start downloading our experimental metadata. To do this, we will call `get_experiments()` on our connectivity instance. The method takes in the arguments `cre` and `injection_structure_ids`, to filter the downoaded data to match your given criteria. We'll use the argument `dataframe=True` to automatically assign this dowloaded data into a dataframe.

# In[3]:


#Dowload all the experiments, no filter
mouse_exp_df = mcc.get_experiments(dataframe=True)
mouse_exp_df.head()


# This gives us metadata on all the expereiments in the dataset. Alternatively, you can specify within the method wether you would like to filter certain experiments by `transgenic_line`. Let's take a look at what trangenic lines are available to us. 

# In[4]:


col = 'transgenic_line'
transgenic_lines = mouse_exp_df[col].unique()
print(transgenic_lines)


# Let's start by creating a dataframe that only contains experiments with the first three Cre lines in the list above *(Penk-IRES2-Cre-neo, Gabrr3-Cre_KC112, Hdc-Cre_IM1)*. You can change the Cre lines by changing the values in the list assigned to `transgenic_lines`. Remember to copy the Cre line of interest exactly, including the single quotes. We'll then use this list in the argument `cre = ` in our call to `get_experiments`.

# In[5]:


# Choose your Cre lines
transgenic_lines = ['Penk-IRES2-Cre-neo','Gabrr3-Cre_KC112','Hdc-Cre_IM1'] 

# Filter experiments from only the first 3 cre lines 
transgenic_line_df = mcc.get_experiments(cre = transgenic_lines, dataframe=True)

# Print the length of our dataframe 
print('There are' + ' ' + str(len(transgenic_line_df)) + ' ' + 'experiments in these Cre lines: \n' + str(transgenic_lines))

transgenic_line_df.head()


# ## Download experimental metadata by injection structure 

# In order to use the `injection_structure_ids` argument above, you need the structure IDs. The MouseConnectivityCache has a method for retrieving the adult mouse structure tree as an StructureTree class instance. The StructureTree class has many methods that allows you to access lists of brain structures through their ID, name, acronym, and many other properties. This is done by executing the `get_structure_tree()` method on your MouseConnectivityCache instance (`mcc`).
# 
# Below we will access information on the hypothalamus via its name by calling `get_structures_by_name()` on our StructureTree instance. 

# In[6]:


# Grab the StructureTree instance
structure_tree = mcc.get_structure_tree()

# Get info on hypothalamus by its name 
hypothalamus = structure_tree.get_structures_by_name(['Hypothalamus'])[0]
hypothalamus


# This gives us a dictionary with info about our brain structure of interest. The value stored within `id` is the injection strucuture id. We can download our experimental metadata by injection structure by inputting this value into `cre =` when calling `get_experiments`.

# In[7]:


# Hypothalamus experiments have ID 1097
injection_structure = hypothalamus['id']
hyp_df = mcc.get_experiments(injection_structure_ids = [injection_structure], 
                             dataframe=True)

hyp_df.head()


# ## Putting it All Together 

# Below is an example of how we can combine both filtering by Cre line and by injection structure to get a more refined set of data.

# In[8]:


# Choose desired structure 
hypothalamus = structure_tree.get_structures_by_name(['Hypothalamus'])[0]
injection_structure = hypothalamus['id']

# Choose your Cre lines
transgenic_lines = 'Hdc-Cre_IM1' 

# Filter experiments using cre line and injection structure 
penk_hypothalamus_exps = mcc.get_experiments(cre = [transgenic_lines],
                                            injection_structure_ids = [injection_structure])

# Assign as dataframe
penk_hypothalamus_df = pd.DataFrame(penk_hypothalamus_exps).set_index('id')
penk_hypothalamus_df


# ## Structure Tree

# So far, we know that the hypothalamus is a brain structure available to us in our experiments, but what about the rest of the brain structures? How do we find what are all the brain structures availabe to us? To do so, we can take a look at the unique values under the `name` column, in our summary of brain structures. 

# In[9]:


# From the above table, "Brain - Summary Structures" has ID 167587189
summary_structures = structure_tree.get_structures_by_set_id([167587189])
summary_structures_df = pd.DataFrame(summary_structures)

# Determine how many different structures are within our experiments 
structure_name = summary_structures_df['name'].unique()
print("%d Total Available Brain Structures" % len(structure_name))

# print the first 20 brain structures in our data
print(structure_name[:19])


# As a convenience, structures are grouped in to named collections called "structure sets". These sets can be used to quickly gather a useful subset of structures from the tree. The criteria used to define structure sets are eclectic; a structure set might list:
# 
# - structures that were used in a particular project.
# - structures that coarsely partition the brain.
# - structures that bear functional similarity.
# 
# To see only structure sets relevant to the adult mouse brain, use the StructureTree:

# In[10]:


from allensdk.api.queries.ontologies_api import OntologiesApi

oapi = OntologiesApi()

# get the ids of all the structure sets in the tree
structure_set_ids = structure_tree.get_structure_sets()

# query the API for information on those structure sets
pd.DataFrame(oapi.get_structure_sets(structure_set_ids))


# As you can see from the table above, there are many different sets that our available brain structures can be grouped in. Below we will look into our Mouse Connectivity Summary data by specifying the set ID using the `get_structure_by_set_id()` method. 

# In[11]:


# From the above table, "Mouse Connectivity - Summary" has id 687527945
summary_connectivity = structure_tree.get_structures_by_set_id([687527945])
summary_connectivity_df = pd.DataFrame(summary_connectivity)
summary_connectivity_df.head()


# For more information on the different methods to access information on brain structures as well as the StructureTree class, visit <a href="https://alleninstitute.github.io/AllenSDK/allensdk.core.structure_tree.html">here</a>. 

# In[ ]:




