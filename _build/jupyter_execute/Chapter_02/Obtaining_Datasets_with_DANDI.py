#!/usr/bin/env python
# coding: utf-8

# # Obtaining Datasets with DANDI

# [DANDI](https://www.dandiarchive.org/) is an open source data archive for cellular neurophysiology datasets. DANDI allows the submission and download of neural datasets to promote research collaboration and consistent and transparent data standards. DANDI also provides a solution to the difficulties that come from housing data in the many other general domains (i.e. Dropbox, Google Drive, etc.). Usefully for our purposes here, many of the datasets on DANDI are in NWB format.

# ## Downloading DANDIsets 

# First, we need to ensure that you have the [`DANDI` client](https://pypi.org/project/dandi/) installed on your computer. The cell below will try to import dandi, and if that fails, it will install it. 

# In[7]:


try:
    import dandi
    if dandi.__version__ == '0.18.0':
        print('DANDI installed & imported.')
    else:
        print('older version of DANDI installed, this may cause issues')
except ImportError as e:
    get_ipython().system('pip install dandi==0.18.0')


# All available **Dandisets** can be found on the <a href = 'https://gui.dandiarchive.org/#/'> DANDI Web Application</a>. You will need to create an account with DANDI before downloading any Dandiset to your local device. The cell below will download [this dataset](https://gui.dandiarchive.org/#/dandiset/000006) from DANDI. This dataset contains 32-channel extracellular recordings from muouse cortex.
# 
# Downloading this dataset may take several minutes, depending on your internet connection and the size of the files.

# In[2]:


get_ipython().system('dandi download https://dandiarchive.org/dandiset/000006/draft')


# ## Reading our NWB file

# To access the data in our nwb file we must read the file. This is done in two steps:
# 
# - assign our file as an NWBHDF5IO object
# - read our file
# 
# The first step is done using the NWBHDF5IO class to create our NWBHDF5IO object and map our file to HDF5 format. Once we have done this, we can use the `read()` method to return our nwb file. For more information on how to read NWB files, please visit the <a href = 'https://pynwb.readthedocs.io/en/stable/tutorials/general/file.html'> Reading an NWB file</a> section from the NWB Basics Tutorial. For more information on the NWBHDF5IO class, please visit the <a href = 'https://pynwb.readthedocs.io/en/stable/pynwb.html#pynwb.NWBHDF5IO'> pynwb package original documentation</a>.
# 
# **Note**: a downloaded dandiset may contain multiple NWB files that pertain to various subjects and multiple sessions for a given experiment. Make sure you specify the exact file path to the single NWB file you wish to read. 

# In[8]:


from pynwb import NWBHDF5IO

# Read 1 session file from 1 subject from our Dandiset 
io = NWBHDF5IO('000006/sub-anm369962/sub-anm369962_ses-20170309.nwb', 'r')
nwb_file = io.read()
print(type(nwb_file))


# If you wish to access the related publications of the experimental data that you just downloaded, you can do so by executing the `related_publications` method on your NWB file object. You can plug what prints in the single quotes below into a browswer window to check out the original publication describing this data.

# In[10]:


nwb_file.related_publications


# Each NWB file will also have information on where the experiment was conducted, what lab conducted the experiment, as well as a description of the experiment. These Groups can be accessed using `institution`, `lab`, and `experiment_description`, attributes on our nwb_file, respectively.

# In[12]:


# Get Meta-Data from NWB file 
print('The experiment within this NWB file was conducted at {} in the lab of {}.     The experiment is detailed as follows: {}'    .format(nwb_file.institution, nwb_file.lab, nwb_file.experiment_description))


# The following section will go over the the structure of an NWBFile and how to access data from this new file type. 
