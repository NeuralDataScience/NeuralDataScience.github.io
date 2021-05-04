#!/usr/bin/env python
# coding: utf-8

#  # Obtaining Raw Electrophysiology Data

# This section will teach you how to interact with the Neuropixels dataset, specifically how to download experimental sessions, return procesed data, and subset your data to contain only brain regions you are interested in. 
# 
# We will first need to import the `EcephysProjectCache` from the Allen SDK and create an instance of the class. The class is used to download the metadata and data for all sessions in the Neuropixels dataset. For the full list of methods, please visit the <a href = 'https://allensdk.readthedocs.io/en/v1.7.1/allensdk.brain_observatory.ecephys.ecephys_project_cache.html'> original documentation</a>.
# 
# Below we will execute `get_session_table()` on our `EcephysProjectCache` object which will return a dataframe with metadata on each session. 

# In[1]:


# Import necessary packages 
import numpy as np 
import pandas as pd 
import scipy as sp
import seaborn as sns
from scipy import signal
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Import packages necessary to plot behavior
import allensdk.brain_observatory.ecephys.visualization as ecvis
from allensdk.brain_observatory.visualization import plot_running_speed

# Import the Neuropixels Cache
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache

# Assign where data will be stored
manifest_path = 'manifest.json' 

# Create the EcephysProjectCache object
cache = EcephysProjectCache(manifest=manifest_path)

# Return all sessions available in this dataset
sessions = cache.get_session_table()
print('Total number of sessions: ' + str(len(sessions)))
sessions.head()


# A few columns that we may want to pay attention to for future analysis are the `full_genotype`, `unit_count`, and `ecephys_structure_acronyms`. 
# 
# In this dataset, a `unit` referes to an individual neuron that was recorded in the session. The `unit_count` refers to the total number of neurons recorded in a particluar sesssion. As mentioned in the chapter introduction, three different genotypes were used alongside the wildtype for these experiments. You can find the genotype under `full_genotype`. Lastly, you can find what structures the data in a session was collected from under `ecephys_structure_acronyms`.
# 
# Below we will return the follwoing information on our sessions: 
# - how many sessions per genotype
# - the average number of units recorded per session
# - what brain structures were used in our sessions

# In[2]:


genotypes = sessions['full_genotype'].value_counts()

avg_units = sessions['unit_count'].mean()

brain_areas = []

for idx,structure in sessions.iterrows():
    for i in structure['ecephys_structure_acronyms']:
        if i not in brain_areas:
            brain_areas.append(i)
        else:
            continue

print('Genotype Count:')
print(genotypes)

print('\n Average Units:')
print(avg_units)

print('\n All brain areas:')
print(brain_areas)


# Let's say we only want sessions where the data has recordings from CA1. We can do the following to create a session list that we want.

# In[3]:


# Create a session list based on some criteria

session_list = []

for idx,structure_list in enumerate(sessions['ecephys_structure_acronyms']):
    if 'CA1' in structure_list:
        session_list.append(sessions.index[idx])   
        
print('There are '+str(len(session_list))+' sessions that meet this criteria:')
print(session_list)


# ## Downloading a Single Session & the Structure of Session Files

# Now, we can use the session list to get the data we want. Unfortunately, it looks like we can only extract one experiment as a time, so if you want to do this for multiple experiments, you'll need to loop over the `get_session_data` method for your entire session_list. For example, your workflow might be:
# 
# 1. Extract one session.
# 2. Look for units recorded from your brain region of interest in that session.
# 3. Extract whatever metric you're interested in (e.g., firing rate).
# 4. Append those values to a list of firing rates.
# 5. Loop back around to the next session.
# 
# The `get_session_data` downloads the `NWB` data file of our experiment session and returns a session object that contains data and metadata for a single session. For a full list of methods and attributes for an ecephys session object, please visit the <a href = 'https://allensdk.readthedocs.io/en/v1.7.1/allensdk.brain_observatory.ecephys.ecephys_session.html'> original dcumentation</a>. Here, we'll just take one session as an example.

# **Note**: The session files are very large files that will take some time to download depending on your connection speed. It is important that you do not stop the download as the cell is running becasue this will truncate the file and you will not be able to work with the data. The cell block below creates a new instance of `EcephysProjectCache` with a larger `timeout` value to ensure enough time is allowed for the file to download. 

# In[4]:


from allensdk.brain_observatory.ecephys.ecephys_project_api import EcephysProjectWarehouseApi
from allensdk.brain_observatory.ecephys.ecephys_project_api.rma_engine import RmaEngine

cache = EcephysProjectCache(manifest=manifest_path,
                            fetch_api=EcephysProjectWarehouseApi(RmaEngine(scheme="http",host="api.brain-map.org",timeout= 50 * 60)))          


# In[5]:


# Download our session data 
session = cache.get_session_data(session_list[1])
print('Session downloaded.')


# ## Obtaining Single Units

# Now that we have downloaded the single session file, we can begin to explore our `EcephysSession` object. The `units` property of our session object returns a dataframe that contains the recorded activity of sorted neurons from a mouse brain. There are many metrics stored within `units` that can be used in your potential analyses. Some key metrics include:
# 
# - **firing rate**: mean spike rate during the entire session
# - **presence ratio**: fraction of session when spikes are present
# - **ISI violations**: rate of refractory period violations
# - **peak_channel_id**: channel in which peak-to-trough amplitutde is maximized
# - **d'**: classification accuracy based on LDA
# - **SNR**: signal to noise ratio
# - **Maximum drift**: Maximum change in spike depth during recording
# - **Cumulative drift**: Cumulative change in spike depth during recording
# 
# For a full list of methods and attributes that can be called on an `EcephysSession` object, please see <a href = 'https://allensdk.readthedocs.io/en/v1.7.1/allensdk.brain_observatory.ecephys.ecephys_session.html'> here</a>.

# In[6]:


# Return units dataframe
units_df = session.units
units_df.head()


# To ensure that the recordings we use in our analysis are all of good quality, we will filter the data according to the signal-to-noise ratio (`snr`) and the `ISI_Violations` of our neurons. Below we will plot the distributions of both.

# In[7]:


# Signal to noise distribution
col_1 = 'snr'
plt.hist(units_df['snr'], bins=30)
plt.title('Distribution of SNR')
plt.xlabel('Signal to Noise Ratio')
plt.ylabel('Frequency')
plt.show()


# In[8]:


# ISI distribution 
col_2 = 'isi_violations'
plt.hist(units_df[col_2], bins=30)
plt.title('Distribution of ISI Violations')
plt.xlabel('Rate of Refractory Period Violations')
plt.ylabel('Frequency')
plt.show()


# For the purposes of this tutorial, we will use `snr` values greater than 2 and `ISI_violation` values less than 0.1, define our good quality units. 

# In[9]:


# Create dataframe with our conditions of interest
good_snr = units_df[units_df['snr']>2]
good_units_df = good_snr[good_snr['isi_violations']<0.1]


print('Number of Recordings with good SNR and Low ISI:')
print(len(good_units_df))
good_units_df.head()


# Just like we did before in our sessions dataframe, we can return the brain structures that our session's data was recorded from as well as how many neurons were recorded per brain area. 

# In[10]:


col = 'ecephys_structure_acronym'

print('Available Brain Structures:')
print(good_units_df[col].unique())
print('\n Brain Structure Frequency:')
print(good_units_df[col].value_counts())


# ## Obtaining Single Sction Potential Waveforms 

# Each session contains a dictionary of mean waveforms for all the units recorded in that session. They are stored inside a xarray DataArray where the `unit_id` are mapped to the mean spike waveform values. The dimensions of the DataArrays are `channel` and `time` which are recorded in microvolts and seconds, respectivley. For more information on `xarray.DataArray`, please visit, <a href = 'http://xarray.pydata.org/en/stable/generated/xarray.DataArray.html'> here</a>.
# 
# To access the mean spike waveforms for all units in a session, use the attribute `mean_waveforms` on your `EcephysSession` object. 

# In[11]:


all_mean_waveforms = session.mean_waveforms
print('Total number of waveforms:')
print(len(all_mean_waveforms))


# We can plot the mean waveforms of our units with the method `plot_mean_waveforms` from the ecephys visualization package. The method uses the `mean_waveforms` dictionary, `unit_id`'s, and `peak_channel_id`'s as arguments. For more information on this method, visit <a href = 'https://allensdk.readthedocs.io/en/latest/allensdk.brain_observatory.ecephys.visualization.html'> here</a>.
# 
# Below we will compare mean waveforms from different brain areas. We will be looking at one wavefrom from the `CA1`, `LP`, `DG`, `VISp`. We first need to create a list of unit_id's for the waveforms we are interested in. 

# In[12]:


# Assign Unit IDs of different brain areas of interest
CA1_unit_ids = good_units_df[good_units_df['ecephys_structure_acronym'] == 'CA1'].index
LP_unit_ids = good_units_df[good_units_df['ecephys_structure_acronym'] == 'LP'].index
DG_unit_ids = good_units_df[good_units_df['ecephys_structure_acronym'] == 'DG'].index
VISp_unit_ids = good_units_df[good_units_df['ecephys_structure_acronym'] == 'VISp'].index

# Return first entry of our brain areas of interst
first_CA1_units_ids = CA1_unit_ids[0]
first_LP_units_ids = LP_unit_ids[0]
first_DG_units_ids = DG_unit_ids[1]
first_VISp_units_ids = VISp_unit_ids[0]
uois_ids = [first_CA1_units_ids, first_LP_units_ids, first_DG_units_ids, first_VISp_units_ids]

# Return dataframe
uois_df = good_units_df.loc[uois_ids]

uois_df


# Using the `unit_ids`, we can create our own dictionary that maps our ids of interest to the `mean_waveforms` array,

# In[13]:


# Create dictionary of waveforms that only include units of interest
waveforms_oi = {}
for ids in uois_ids:
    waveforms_oi[ids] = all_mean_waveforms[ids]

# Create dictionary of peak channels that only include units of interest
peak_channels_oi = {}
for ids in uois_ids:
    peak_channels_oi[ids] = good_units_df.loc[ids, 'peak_channel_id']

# Plot mean waveforms
fig = ecvis.plot_mean_waveforms(waveforms_oi, uois_ids, peak_channels_oi)
legend_list = list(uois_df['ecephys_structure_acronym'] )
plt.legend(legend_list)


plt.show()


# In[ ]:




