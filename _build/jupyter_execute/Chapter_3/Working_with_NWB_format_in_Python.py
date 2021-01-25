#!/usr/bin/env python
# coding: utf-8

# # Working with NWB in Python 

# In[1]:


import numpy as np
import pandas as pd 
from matplotlib import pyplot as plt
from pynwb import NWBHDF5IO


# ## Reading our NWB file

# To access the data in our nwb file we must read the file. This is done in two steps:
# - assign our file as an `NWBHDF5IO` object
# - read our file 
# 
# The first step is done using the `NWBHDF5IO` class to create our `NWBHDF5IO` object and map our file to HDF5 format. Once we have done this, we can use the `read()` method to return our nwb file. For more information on how to read NWB files, please visit the *Reading data from an NWB file* section from the <a href = 'https://pynwb.readthedocs.io/en/latest/tutorials/general/file.html'> NWB Basics Tutorial</a>. For more information on the `NWBHDF5IO` class, please visit the <a href = 'https://pynwb.readthedocs.io/en/latest/pynwb.html#pynwb.NWBHDF5IO'> original documentation</a>.

# In[2]:


# first read the file 
io = NWBHDF5IO('000017/sub-Cori/sub-Cori_ses-20161214T120000.nwb', 'r')
nwb_file = io.read()
nwb_file


# In[3]:


# dictionary of all neurodata_type objects in the NWBFile
print(nwb_file.objects)


# In[4]:


# loop though objections dictionary 
# returns the obeject ID along with the type 
# and the object name 
for obj in nwb_file.objects.values():
    print('%s: %s "%s"' % (obj.object_id, obj.neurodata_type, obj.name))


# ## File Hierarchy: Groups, Datasets, and Attributes

# The NWB file is composed of various Groups, Datasets, and Attributes. The data/datasets and cooresponding meta-data are encapsulated within these Groups. The `fields` attribute returns a dictionary contiaining the metadata of the Groups of our nwb file. The dictionary `keys` are the various Groups within the file which we will use to access our datasets.

# In[5]:


# nwb_file.fields


# In[6]:


# Get the Groups for the nwb file 
nwb_fields = nwb_file.fields
print(nwb_fields.keys())


# Each NWB file will have information on where the experiment was conducted, what lab conducted the experiment, as well as a description of the experiment. This information can be accessed using `institution`, `lab`, and `description`, attributes on our `nwb_file`, respectively. 

# In[7]:


# Get Meta-Data from NWB file 
print('The experiment within this NWB file was conducted at {} in the lab of {}. The experiment is detailed as follows: {}'.format(nwb_file.institution, nwb_file.lab, nwb_file.experiment_description))


# We can access metadata from each group in our `nwb_file` with the following syntax: `nwb_file.group`. This is no different than executing a method and/or attribute. The `acquisition` group contains datasets of acquisition data. We can look at the look at the `description` field in the metadata to understand what each dataset in the group contains. 

# In[8]:


# example showing how to return meta data from groups in nwb file 
# 'acquisition' is the first group in our file 
nwb_file.acquisition


# In this file, the acquisition group contains two different dataets, `lickPiezo` and `wheel_position`. To access the actual data array of these datasets we must first subset our dataset of interest from the group. We can then use `data[:]` to return our actual data array. 

# In[9]:


# select our dataset of interest 
dataset = 'lickPiezo'
lickPiezo_ds = nwb_file.acquisition[dataset]

# return data array 
lickPiezo_data_array = wheel_pos_in.data[:20]

print(lickPiezo_data_array)


# In[12]:


# testing out each key for nwb file 
# 'units' seems to return data that was recorded 
nwb_file.processing['behavior']


# The `trials` Group contains data from our experimental trials such as start/stop time, response time, feedback time, etc. You can return the trials data as a dataframe by using the `to_dataframe` method.

# In[34]:


# trials table
trials = nwb_file.trials
trials_df = trials.to_dataframe()
trials_df.head()


# The `intervals` group also contains a `trials` dataset and can be used to access the experimental trials similar to what was accomplished in the cell above. 

# In[18]:


# Select the group of interest 
intervals = nwb_file.intervals

# Subset the dataset from the group and assign it as a dataframe
interval_trials_df = intervals['trials'].to_dataframe()
interval_trials_df.head()


# The `description` attribute provides a short description on each column of the dataframe. 

# In[22]:


print(intervals['trials']['feedback_type'].description)


# In[23]:


# test cell 
nwb_file.intervals


# In[ ]:




