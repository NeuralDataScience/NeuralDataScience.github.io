#!/usr/bin/env python
# coding: utf-8

# # Data for Single Cells 

# ## Plotting a single cell’s morphology & accessing the morphology data

# This section will serve as an introduction to the Allen Cell Types database. We'll work with the AllenSDK to see what information we can gain about our cells.
# 
# First, we'll `import` the CellTypesCache module. This module provides tools to allow us to get information from the cell types database. We're giving it a **manifest** filename as well. CellTypesCache will create this manifest file, which contains metadata about the cache. You can look under cell_types in your directory, and take a look at the file.
# 
# (If you're curious you can see the full documentation for the core package <a href="https://allensdk.readthedocs.io/en/latest/allensdk.core.html">here</a>.)
# 
# <b>Note</b>: In order to run the line below, you need to have the AllenSDK installed. You can find information on how to do that <a href="http://alleninstitute.github.io/AllenSDK/install.html">here</a>. If you're running this on the UCSD Datahub, the Allen SDK has already been installed for you.

# In[1]:


#Import the "Cell Types Cache" from the AllenSDK core package
from allensdk.core.cell_types_cache import CellTypesCache

#Import CellTypesApi, which will allow us to query the database.
from allensdk.api.queries.cell_types_api import CellTypesApi

# We'll then initialize the cache as 'ctc' (cell types cache)
ctc = CellTypesCache(manifest_file='cell_types/manifest.json')


# ### Step One: Get Cells & Manipulate Dataframe
# 
# The `get_cells` method downloads metadata for all cells in the database. The database contains human cells and mouse cells. Alternatively, one can filter out the database to only include cells collected from a certain species.
# Look through <a href="https://allensdk.readthedocs.io/en/latest/allensdk.core.cell_types_cache.html">the documentation for the CellTypesCache</a> for more information on the `get_cells` method.

# In[2]:


all_cells = ctc.get_cells()
print(all_cells)


# As you can see, the output for the metadata of our cells is messy and difficutlt to interpret. To make our data easier to read and work with, we can convert `all_cells` into a pandas datadrame.
# 

# Note: If you're having trouble with Pandas, it can help to look at <a href="https://pandas.pydata.org/pandas-docs/stable/user_guide/">the user guide</a>.

# In[3]:


import pandas as pd 

# Create a dataframe from 'all_cells' and re-assign the dataframe to a new variable
all_cells_df = pd.DataFrame(all_cells)

# '.head()'returns the first 5 rows of the dataframe instead of the entire dataframe
all_cells_df.head()


# If we look back at our dataframe, our rows don't have any useful information -- they're simply a list of indices starting from zero. We can reassign the row values by using the method `set_index`. You can assign any present column in the dataframe as the indices to be the indeces for the rows. Since each observation in the dataframe has a unique `id`, the `id` will be set as the index.

# In[4]:


all_cells_df = all_cells_df.set_index('id')
all_cells_df.head()


# As you may have noticed already, out current dataframe only contains metadeta about our cells and no information on the morphology or electrophysiolgy of our cells. In order to get information about the morphology of these cells, we need to use the `get_morphology_features()` method on our instance of the cell types cache.

# In[5]:


#morphology = ctc.get_morphology_features()

# downloads the morphology features and sets up the dataframe all in one line
morphology_df = pd.DataFrame(ctc.get_morphology_features()).set_index('specimen_id')
print('\nLength of dataframe:')
print(len(morphology_df))
morphology_df.head()


# Now we have two dataframes, one with the metadata for our cells (indexed by id) and another with the morphology data for all cells, also indexed by id. Usefully, these ids are unique to each cell, meaning we can match them across dataframes.
# 
# We can use either the `merge` or `join` pandas methods in order to pull all of this data into one dataframe. 
# 
# ![](http://www.datasciencemadesimple.com/wp-content/uploads/2017/09/join-or-merge-in-python-pandas-1.png)
# 
# There are different types of joins/merges you can do in pandas, illustrated <a href="http://www.datasciencemadesimple.com/join-merge-data-frames-pandas-python/">above</a>. Here, we want to do an **inner** merge, where we're only keeping entries with indices that are in both dataframes. We could do this merge based on columns, alternatively.
# 
# **Inner** is the default kind of join, so we do not need to specify it. And by default, join will use the 'left' dataframe, in other words, the dataframe that is executing the `join` method.
# 
# If you need more information, look at the <a href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.join.html">join</a> and <a href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html">merge</a> documentation: you can use either of these to unite your dataframes, though join will be simpler!

# In[6]:


meta_and_morph_df = all_cells_df.join(morphology_df)
meta_and_morph_df.head()


# In[7]:


meta_and_morph_df.columns


# You can also acesss morphology of a single cell by exectuing the `get_recontruction()` method on your instance of the cells type cache. To do so, you must specify what cell you want to recontruct by inputing a `specimen_id`. This method returns a class instance with methods for accessing morphology compartments. 

# In[8]:


single_cell_morphology = ctc.get_reconstruction(specimen_id = 478107198)

#help(single_cell_morphology)


# 

# In[9]:


single_cell_morphology.soma


# ## Plotting a single sweep of data

# At this point, you might have realized that this dataframe doesn't contain any data about the electrophysiology. In order to get information about the electrophysiological properties of these cells, we need to use the `get_ephys_features()` method on our instance of the cell types cache.

# Just as we did before, we will will assign the output of `get_ephys_features()` to a variable and then convert it into a pandas dataframe. 

# In[10]:


ephys_features = pd.DataFrame(ctc.get_ephys_features()).set_index('specimen_id')
ephys_features.head()


# Again, we can combine our dataframe that contians the metadata of our cells with our electrophysiology dataframe to create one single dataframe. 

# In[11]:


all_ephys_features = all_cells_df.join(ephys_features)
all_ephys_features.head()


# In[12]:


print(len(all_ephys_features))


# The `get_ephys_data()` method can download electrophysiology traces for a single cell in the database. This method returns a  class instance with helper methods for retrieving stimulus and response traces out of an NWB file. In order to use this method, you must specify the id of the cell specimen whose electrophysiology you would like to download. 

# In[13]:


specimen1_ephys = ctc.get_ephys_data(specimen_id = 525011903)
#specimen1_ephys.get_experiment_sweep_numbers()
#specimen1_ephys.get_sweep(100)
#specimen1_ephys.get_sweep_metadata(100)
#specimen1_ephys.get_spike_times(100)


# For more information on the helper methods that can be used on this NwbDataSet instance, please click <a href="https://allensdk.readthedocs.io/en/latest/allensdk.core.nwb_data_set.html">here</a>
