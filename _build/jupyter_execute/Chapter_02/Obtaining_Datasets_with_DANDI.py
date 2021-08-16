#!/usr/bin/env python
# coding: utf-8

# # Obtaining Datasets with DANDI

# [DANDI](https://www.dandiarchive.org/) is an open source data archive for neuroscience datasets, called **Dandisets**. DANDI allows scientists to submit and download neural datasets to promote research collaboration and consistent and transparent data standards. DANDI also [provides a solution](https://www.dandiarchive.org/handbook/01_introduction/) to the difficulties that come from housing data in the many other general domains (i.e. Dropbox, Google Drive, etc.). Usefully for our purposes here, many of the datasets on DANDI are in NWB format.
# 
# There are two primary ways to work with Dandisets:
# 1. You can **download the datasets locally**, either via the [DANDI Web Application](https://gui.dandiarchive.org/#/dandiset) or using the DANDI Python client below. If you download via the website, you'll need to create an account.
# 2. You can **stream datasets directly** from DANDI (under development).
# 
# Below, we demonstrate how to do both of these. For additional information on either of these methods, please refer to the [DANDI documentation](https://gui.dandiarchive.org/). 

# ## Option 1: Downloading Dandisets using Python 

# First, we need to ensure that you have the [`DANDI` client](https://pypi.org/project/dandi/) installed on your computer. The cell below will try to import DANDI. If you have an old version of DANDI, it will prompt you to install a newer version. Type "Y" if you would like to install a new version (this is recommended). If you don't have DANDI at all, it will install the most recent version.

# In[1]:


try:
    import dandi
    if dandi.__version__>='0.26.0':
        print('DANDI installed & imported.')
    else:
        response = input('Old version of DANDI installed. Would you like to install a newer version of DANDI? (Y/N)')
        if response == 'Y':
            get_ipython().system('pip install --upgrade dandi')
except ImportError as e:
    get_ipython().system('pip install dandi')


# The cell below will download [this dataset](https://gui.dandiarchive.org/#/dandiset/000006) from DANDI. This dataset contains 32-channel extracellular recordings from mouse cortex.
# 
# <mark>**Note:** Downloading this dataset may take several minutes, depending on your internet connection.</mark>

# In[2]:


get_ipython().system('dandi download https://dandiarchive.org/dandiset/000006/draft')


# Once the cell above completes running, you will see a new folder 📁"00006" wherever you're running this notebook.

# ## Option 2: Streaming the Dandiset
# 
# **This is under development.**

# In[3]:


# Import necessary packages
from pynwb import NWBHDF5IO
from nwbwidgets import nwb2widget
import requests

...


# The following section will go over the the structure of an NWBFile and how to access data from this new file type. 
