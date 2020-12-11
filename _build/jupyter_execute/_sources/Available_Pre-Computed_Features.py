#!/usr/bin/env python
# coding: utf-8

# # Available Pre-Computed Features

# The Allen Institute also has many more precomputed features. Many of them give access to more information on the electrophysiology, morphology, and metadata on the cells available in the Allen. We will demonstrate some of these features below.

# In[1]:


#Import all the necessary packages and initalize an instance of the cache
import pandas as pd
from allensdk.core.cell_types_cache import CellTypesCache
from allensdk.api.queries.cell_types_api import CellTypesApi
ctc = CellTypesCache(manifest_file='cell_types/manifest.json')


# The `all_features` method can be used to access the morphology and electrophysiology of all the cells in the database and merges the two into a single table. This method can take into two optional inputs; `dataframe` and `require_reconstructon`.

# In[2]:


all_features = ctc.get_all_features(dataframe = True)
all_features.head()


# Since we set the `dataframe` parameter to `True`, the method returns our data as a nice and neat pandas dataframe. If set to `False`, the method returns a dictionary. We can all check to make sure all the columns are there by executing the `get_ephys_features` and `get_morphology_features` seperately and comparing the columns.

# In[3]:


all_features_columns = all_features.columns
all_features_columns


# In[4]:


# Store all ephys columns in a variable 
ephys = pd.DataFrame(ctc.get_ephys_features())
ephys_columns = ephys.columns

# Store all morphology columns in a variable 
morphology = pd.DataFrame(ctc.get_morphology_features())
morphology_columns = morphology.columns 

# Combine the two into one list
ephys_and_morphology = list(morphology_columns) + list(ephys_columns)

# Sort and Compare the columns to make sure they are all there 
print(list(all_features_columns).sort() == ephys_and_morphology.sort())


# By default, `get_all_features()` only returns ephys and morphology features for cells that have reconstructions. To access all cells regardless of reconstruction, set the parameter `require_recontruction` to `False`.

# The `get_ephys_data()` method can download electrophysiology traces for a single cell in the database. This method returns a  class instance with helper methods for retrieving stimulus and response traces out of an NWB file. In order to use this method, you must specify the id of the cell specimen whose electrophysiology you would like to download. 

# Below we have created a pandas dataframe from the data on human cells and set the row indices to be the `id` column. This will give us the metadata on human cells along and ID's to choose from. 

# In[5]:


human_df = pd.DataFrame(ctc.get_cells(species = [CellTypesApi.HUMAN])).set_index('id')
human_df.head(1)


# Now that we have some specimen ID's to choose from, we can execute the `get_ephys_data()` method on our CellTypesCache instance. Lets try to get the electropysiology data from the first entry in our dataframe and store it in a variable. 

# In[6]:


specimen1_ephys = ctc.get_ephys_data(specimen_id = 525011903)


# We now have a NwbDataSet instance with methods that can help us access electrophysiology traces from our specimen of interest. 

# In[7]:


specimen1_ephys.get_experiment_sweep_numbers()


# In[8]:


specimen1_ephys.get_sweep(100)


# In[9]:


specimen1_ephys.get_sweep(12)


# In[10]:


specimen1_ephys.get_sweep_metadata(100)


# In[11]:


specimen1_ephys.get_spike_times(100)


# There are also other helper methods such as `set_sweep_times()` and `set_sweep()` that allow you to overwrite in the NWB files. For more information on hwo to use these two methods, please visit <a href="https://allensdk.readthedocs.io/en/latest/allensdk.core.nwb_data_set.html">here</a>.
