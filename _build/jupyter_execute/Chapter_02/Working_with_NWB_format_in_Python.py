#!/usr/bin/env python
# coding: utf-8

# # Working with NWB in Python
# 
# On the previous page, we demonstrated how to obtain a dataset with DANDI. Now that you have a dataset downloaded, let's take a close look at it so that we can understand how to work with these NWB files.
# 
# **Important**: This notebook will only work with the 2.10.0 version of the h5py package. The cell below will ensure that you have this version installed.
# 
# ## Setup

# In[3]:


# Import any necessary packages
from pynwb import NWBHDF5IO

# This will ensure that the correct version of the h5py package is installed
try:
    import h5py
    if h5py.__version__ == '2.10.0':
         print('h5py version ' + h5py.__version__ + ' already installed')
    else:
        print('h5py installed with an older version. some features may not work.')
except ImportError as e:
    get_ipython().system("pip install h5py == '2.10.0'")


# ## Read the NWB file
# 
# To access the data in our nwb file we must read the file. This is done in two steps:
# 
# 1. Assign our file as an NWBHDF5IO object
# 2. Read our file
# 
# The first step is done using the `NWBHDF5IO` class to create our `NWBHDF5IO` object and map our file to HDF5 format. Once we have done this, we can use the `read()` method to return our nwb file.
# 
# For more information on how to read NWB files, please visit the <a href = 'https://pynwb.readthedocs.io/en/stable/tutorials/general/file.html'> Reading an NWB file</a> section from the NWB Basics Tutorial. For more information on the NWBHDF5IO class, please visit the <a href = 'https://pynwb.readthedocs.io/en/stable/pynwb.html#pynwb.NWBHDF5IO'> pynwb package original documentation</a>.
# 
# **Note**: a downloaded dandiset may contain multiple NWB files that pertain to various subjects and multiple sessions for a given experiment. Make sure you specify the exact file path to the single NWB file you wish to read. 

# In[4]:


# read the NWB file
io = NWBHDF5IO('000006/sub-anm369962/sub-anm369962_ses-20170310.nwb', 'r')
nwb_file = io.read()
print('File found and read.')
print(type(nwb_file))


# ## File Hierarchy: Groups, Datasets, and Attributes¶

# The NWB file is composed of various Groups, Datasets, and Attributes. The data/datasets and cooresponding meta-data are encapsulated within these Groups. The `fields` attribute returns a dictionary contiaining the the Groups of our nwb file. The dictionary keys are the various Groups within the file which we will use to access our datasets.

# In[14]:


# Get the Groups for the nwb file 
nwb_fields = nwb_file.fields
print(nwb_fields.keys())


# If you wish to access the related publications of the experimental data that you just downloaded, you can do so by accessing the `related_publications` attribute of your NWB file object. You can plug in the doi: address that prints below into a browser window to check out the original publication describing this data.

# In[5]:


# Print the related publication
nwb_file.related_publications


# Each NWB file will also have information on where the experiment was conducted, what lab conducted the experiment, as well as a description of the experiment. These Groups can be accessed using `institution`, `lab`, and `experiment_description`, attributes on our nwb_file, respectively.

# In[12]:


# Get metadata from NWB file 
print('The experiment within this NWB file was conducted at ',nwb_file.institution,'.'      ,nwb_file.experiment_description)


# We can access datasets from each group in our nwb_file with the following syntax: `nwb_file.group`. This is no different than executing a method and/or attribute. Below we will demonstrate some of the useful groups within an `NWBFile` object. 

# The `acquisition` group contains datasets of acquisition data, mainly `TimeSeries` objects belonging to this NWBFile. 

# In[13]:


nwb_file.acquisition


# In this file, the acquisition group contains one dataset, `lick_times`. This dataset has one `Field`, `time_series`, which contains two time series objects, `lick_left_times` and `lick_right_times`. To access the actual data arrays of these objects we must first subset our dataset of interest from the group. We can then use `timestamps[:]` to return a list of timestamps for when the animal licked.

# In[15]:


# select our dataset of interest 
dataset = 'lick_times'
field = 'lick_right_times'
lick_r_dataset = nwb_file.acquisition[dataset][field]

# return first 10 values in data array 
lick_r_data_array = lick_r_dataset.timestamps[:10][:10]

print(lick_r_data_array)


# The `intervals` group contains all time interval tables from the experiment. We can look at the `description` field to understand what each contains.

# In[17]:


# example showing how to return meta data from groups in nwb file 
nwb_file.intervals


# Within the intervals group is the `trials` dataset which is a `DynamicTable` contianing intervals from our experimental trials. Each column in `trials` is a `VectorData` object which can all be assigned to a dataframe using `to_dataframe()`.

# In[18]:


# Select the group of interest from the nwb file 
intervals = nwb_file.intervals

# Subset the dataset from the group and assign it as a dataframe
interval_trials_df = intervals['trials'].to_dataframe()
interval_trials_df.head()


# In[19]:


interval_trials_df['response'].unique()


# The `description` attribute provides a short description on each column of the dataframe.

# In[17]:


# return the description of each col in our dataframe
for col in intervals['trials'].to_dataframe():
    print(col,':',intervals['trials'][col].description)


# The `units` group in our nwb_file contains the neural activity of our units, including spike data. Much like the `intervals` group, `units` is also a `DynamicTable` that can be assigned to a dataframe.

# In[18]:


units = nwb_file.units
units_df = units.to_dataframe()
units_df.head()


# The `electrodes` group contains metadata from the elctrodes used in the experimental trials. Also a `DynamicTable`, `electrodes` includes location of the electrodes, type of filtering, and which electrode group the electrode belongs to. 

# In[19]:


# electrode positions 
electrodes = nwb_file.electrodes
electrodes_df = electrodes.to_dataframe()
electrodes_df.head()


# ## Additional Resources 

# For an in depth explanation of all groups contained within an `NWBFile` object please visit the <a href = 'https://pynwb.readthedocs.io/en/stable/pynwb.file.html'> pynwb.file.NWBFile </a> section of the PyNWB documentation. 
