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
print(type(nwb_file))


# ## File Hierarchy: Groups, Datasets, and Attributes

# The NWB file is composed of various Groups, Datasets, and Attributes. The data/datasets and cooresponding meta-data are encapsulated within these Groups. The `fields` attribute returns a dictionary contiaining the metadata of the Groups of our nwb file. The dictionary `keys` are the various Groups within the file which we will use to access our datasets.

# In[3]:


# nwb_file.fields


# In[4]:


# Get the Groups for the nwb file 
nwb_fields = nwb_file.fields
print(nwb_fields.keys())


# Each NWB file will have information on where the experiment was conducted, what lab conducted the experiment, as well as a description of the experiment. This information can be accessed using `institution`, `lab`, and `description`, attributes on our `nwb_file`, respectively. 

# In[5]:


# Get Meta-Data from NWB file 
print('The experiment within this NWB file was conducted at {} in the lab of {}. The experiment is detailed as follows: {}'.format(nwb_file.institution, nwb_file.lab, nwb_file.experiment_description))


# We can access metadata from each group in our `nwb_file` with the following syntax: `nwb_file.group`. This is no different than executing a method and/or attribute. The `acquisition` group contains datasets of acquisition data. We can look at the look at the `description` field in the metadata to understand what each dataset in the group contains. 

# In[6]:


# example showing how to return meta data from groups in nwb file 
# 'acquisition' is the first group in our file 
nwb_file.acquisition


# In this file, the acquisition group contains two different dataets, `lickPiezo` and `wheel_position`. To access the actual data array of these datasets we must first subset our dataset of interest from the group. We can then use `data[:]` to return our actual data array. 

# In[7]:


# select our dataset of interest 
dataset = 'lickPiezo'
lickPiezo_ds = nwb_file.acquisition[dataset]

# return first 20 values in data array 
lickPiezo_data_array = lickPiezo_ds.data[:20]

print(lickPiezo_data_array)


# The `processing` group in our `nwb_file` contains all of our processed data for scientific analysis. Within the procesing group there are mulitple subgroups that belong to the `behavior` module. `BehavioralEpochs`, `BehavioralEvents`, `BehavioralEvents`, and `PupilTracking` are seperate groups encapsulated within `behavior` and contain their own datasets. 

# In[8]:


# return meta data for prcessing group
nwb_file.processing


# If we subset `PupilTracking` from `behavior` we can see that it contains two datasets. We can do as we did before and subset our dataset of interst and return the actual data array by executing `data[:]`.

# In[9]:


# assign behavior group to variable 
behavior = nwb_file.processing['behavior']

# subset PupilTracking group from behavior group 
pupil_tracking = behavior['PupilTracking']
print(pupil_tracking)


# In[10]:


# subset the eye_xy_positions dataset
eye_xy_positions = pupil_tracking['eye_xy_positions']
print(eye_xy_positions)

# return firsy 10 entires in actual data array
print('\n Eye (x,y) positions:')
print(eye_xy_positions.data[:10])


# The `intervals` Group contains datasets from trials of our experiment, sub-experiments that were conducted, and/or epochs. For the example below, we will look into the `trials` dataset. You can return the `trials` data as a dataframe by using the `to_dataframe` method.

# In[11]:


# Select the group of interest 
intervals = nwb_file.intervals

# Subset the dataset from the group and assign it as a dataframe
interval_trials_df = intervals['trials'].to_dataframe()
interval_trials_df.head()


# The `description` attribute provides a short description on each column of the dataframe. 

# In[71]:


print(intervals['trials']['response_choice'].description)


# For more information on all the different Groups and hierarchal structure of an NWB file, please visit the <a href = 'https://nwb-schema.readthedocs.io/en/latest/format.html#nwb-n-file'> NWB:N file section</a> of the NWB Format documentation. For a list of all the attributes and methods for a `pynwb.file.NWBfile` obeject, please visit the <a href = 'https://pynwb.readthedocs.io/en/stable/pynwb.file.html'> module documentation</a>.

# ## Possible Analyses 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[75]:


# nwb_file


# In[14]:


# test cell 
nwb_file.session_description 


# In[55]:


# test cell
stimulus_dict = nwb_file.stimulus 
for key in stimulus_dict:
    print(key +':')
    print(stimulus_dict[key].description)
    print('\n')


# In[68]:


electrode_groups = nwb_file.electrode_groups

for key in electrode_groups:
    print(key + ':')
    print(electrode_groups[key].description)
    print(electrode_groups[key].location)
    print('\n')


# In[56]:


# electrode positions 
electrodes = nwb_file.electrodes
electrodes.to_dataframe().head()


# In[54]:


# description of each column in electrodes 
for col in electrodes.to_dataframe():
    print(col + ':')
    print(electrodes[col].description)
    print('\n')


# In[60]:


# all electrode locations 
electrode_df = electrodes.to_dataframe()
print(electrode_df['location'].unique())


# In[69]:


stimulus_dict[]


# In[74]:


# test cell
for col in intervals['trials'].to_dataframe():
    print(col +':')
    print(intervals['trials'][col].description)
    print('\n')


# In[ ]:




