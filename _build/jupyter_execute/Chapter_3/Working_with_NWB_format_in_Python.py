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
# 
# - assign our file as an NWBHDF5IO object
# - read our file
# 
# The first step is done using the NWBHDF5IO class to create our NWBHDF5IO object and map our file to HDF5 format. Once we have done this, we can use the read() method to return our nwb file. For more information on how to read NWB files, please visit the Reading data from an NWB file section from the NWB Basics Tutorial. For more information on the NWBHDF5IO class, please visit the original documentation.

# In[2]:


# first read the file 
io = NWBHDF5IO('000006/sub-anm369962/sub-anm369962_ses-20170310.nwb', 'r')
nwb_file = io.read()
print(type(nwb_file))


# ## File Hierarchy: Groups, Datasets, and Attributes¶

# The NWB file is composed of various Groups, Datasets, and Attributes. The data/datasets and cooresponding meta-data are encapsulated within these Groups. The `fields` attribute returns a dictionary contiaining the metadata of the Groups of our nwb file. The dictionary keys are the various Groups within the file which we will use to access our datasets.

# In[3]:


# nwb_file.fields


# In[4]:


# Get the Groups for the nwb file 
nwb_fields = nwb_file.fields
print(nwb_fields.keys())


# Each NWB file will have information on where the experiment was conducted, what lab conducted the experiment, as well as a description of the experiment. This information can be accessed using `institution`, `lab`, and `experiment_description`, attributes on our nwb_file, respectively.

# In[5]:


# Get Meta-Data from NWB file 
print('The experiment within this NWB file was conducted at {} in the lab of {}. The experiment is detailed as follows: {}'.format(nwb_file.institution, nwb_file.lab, nwb_file.experiment_description))


# We can access metadata from each group in our nwb_file with the following syntax: `nwb_file.group`. This is no different than executing a method and/or attribute. Below we will demonstrate some of the useful groups within an `NWBFile` object. 

# The `acquisition` contains datasets of acquisition data, mainly `TimeSeries` objects belonging to this NWBFile. 

# In[6]:


nwb_file.acquisition


# In this file, the acquisition group contains two different dataets, `lick_left_times` and `lick_right_times` within `lick_times`. To access the actual data array of these datasets we must first subset our dataset of interest from the group. We can then use `data[:]` to return our actual data array.

# In[7]:


# select our dataset of interest 
subgroup = 'lick_times'
dataset = 'lick_right_times'
lick_r_dataset = nwb_file.acquisition[subgroup][dataset]

# return first 10 values in data array 
lick_r_data_array = lick_r_dataset.data[:10]

print(lick_r_data_array)


# The `intervals` group contains all time interval tables from the experiemnt. We can look at the description field in the metadata to understand what each dataset in the group contains.  

# In[8]:


# example showing how to return meta data from groups in nwb file 
nwb_file.intervals


# Within the intervals group is the `trials` dataset which is a `DynamicTable` contianing intervals from our experimental trials. Each column in `trials` is a `VectorData` object and the table can be assigned to a dataframe using `to_dataframe()`.

# In[9]:


# Select the group of interest from the nwb file 
intervals = nwb_file.intervals

# Subset the dataset from the group and assign it as a dataframe
interval_trials_df = intervals['trials'].to_dataframe()
interval_trials_df.head()


# The `description` attribute provides a short description on each column of the dataframe.

# In[10]:


# return the description of each col in our dataframe
for col in intervals['trials'].to_dataframe():
    print(col +':')
    print(intervals['trials'][col].description)
    print('\n')


# The `units` group in our nwb_file contains all our unit metadata including of our neural spike data for scientific analysis. Much like the `intervals` group, `units` is also a `DynamicTable` that can be assigned to a dataframe.

# In[11]:


units = nwb_file.units
units_df = units.to_dataframe()
units_df.head()


# The `electrodes` group contians metadata from the elctrodes used in the experimental trials. Also a `DynamicTable`, the data includes location of the electrodes, type of filtering, and the whats electrode group the electrode belongs to. 

# In[12]:


# electrode positions 
electrodes = nwb_file.electrodes
electrodes_df = electrodes.to_dataframe()
electrodes_df.head()


# For an in depth explanation of all groups contained within an `NWBFile` object please visit the <a href = 'https://pynwb.readthedocs.io/en/stable/pynwb.file.html'> pynwb.file.NWBFile </a> section of the PyNWB documentation. 

# ## Possible Analyses

# Now that we are familiar with the structure of an `NWBFile` as well as the groups encapsulated within it, we are ready to work with the data. 
# 
# The first group that we will look at is `units` becasue it contains information on our neural spikes. Let familiarize ourselves with our dataframe once again. 

# In[13]:


units = nwb_file.units
units_df = units.to_dataframe()
units_df.head()


# The `spike_times` column the times at which the recorded neuron fired. Each neuron has a list of spike times for their `spike_times` column. 

# In[14]:


# return the first 10 spike times for neurons 2-8
neural_data = units_df['spike_times'][1:8][:10]
neural_data


# A spike raster plot can be created using the funtion `plt.eventplot`. A spike raster plot displays the spiking of neurons overtime. In a spike raster plot, the y-axis corresponds to the neuron being recorded and the x-axis represents the time. Each horizontal line in the plot represents the spiking of a neuron. Spike raster plots are useful as they reveal firing rate correlations between groups of neurons. For more inormation on `plt.eventplot` please visit the <a href = 'https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.eventplot.html'> matplotlib documentation</a>. 

# In[15]:


# Set up our figure 
fig = plt.figure()

# Store our data
neural_data = units_df['spike_times'][1:6]

# Set different colors for each neuron 
color_codes = np.array([[0, 0, 0],

                        [1, 0, 0],

                        [0, 1, 0],

                        [0, 0, 1],

                        [1, 1, 0]])

# Plot our raster plot 
plt.eventplot(neural_data, color = color_codes)

# Set our axis limits to only include points in our data
plt.xlim([329.8, 332.8])

# Label our firgure 
plt.title('Spike raster plot')
plt.ylabel('Neuron')
plt.xlabel('Spike')

# Show our plot 
plt.show()


# The plot above is only contains neural spikes from a 3 second time interval. While there are many spikes to consider in this one graph, each neuron has much more than 3 seconds worth of spike recordings. If we do not set an axis limit on the raster plot, all of our spike recordings will be displayed at once and the figure would be unreadable. Instead we can create seperate raster plots in n-second time intervals. Below you can see how to create multiple with 3 second time intervals.

# In[16]:


# Create subplots for graphs and set sizing
fig, ax = plt.subplots(5,figsize=(15,15))

# Set initial x-axis limits
plot_limit = np.array([329.8, 332.8])

# Plot first 3 second interval 
ax[0].eventplot(neural_data, color = color_codes)
ax[0].set_xlim(plot_limit)

# Plot second 3 second interval 
ax[1].eventplot(neural_data, color = color_codes)
ax[1].set_xlim(plot_limit+3)

# Plot third 3 second interval 
ax[2].eventplot(neural_data, color = color_codes)
ax[2].set_xlim(plot_limit+6)

# Plot fourth 3 second interval 
ax[3].eventplot(neural_data, color = color_codes)
ax[3].set_xlim(plot_limit+9)

# Plot fifth 3 second intrval 
ax[4].eventplot(neural_data, color = color_codes)
ax[4].set_xlim(plot_limit+12)

plt.show()


# In[17]:


neurons = units_df[1:6]
neurons 


# In[18]:


units_df['cell_type'].unique()


# In[19]:


units_df['depth'].unique()


# In[20]:


units_df['electrodes'][40]


# In[21]:


nwb_file.electrodes

