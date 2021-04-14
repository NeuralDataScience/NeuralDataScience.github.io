#!/usr/bin/env python
# coding: utf-8

# # Large Scale Single Cell Electrophysiology & Behavior

# In[1]:


import matplotlib.pyplot as plt
import numpy as np

# This will ensure that the AllenSDK is installed.
# If not, it will install it for you.
try:
    import allensdk
    print('allensdk already installed.')
except ImportError as e:
    get_ipython().system('pip install allensdk')


# In[2]:


# Import the Neuropixels Cache
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache
from allensdk.brain_observatory.ecephys.ecephys_project_api import EcephysProjectWarehouseApi
from allensdk.brain_observatory.ecephys.ecephys_project_api.rma_engine import RmaEngine

# Import 2-Photon Cache
from allensdk.core.brain_observatory_cache import BrainObservatoryCache

# Assign where neuropixels data and 2-photon data will be stored
manifest_path = 'manifest.json' 
manifest_path2 = 'manifest2.json'

# Create the EcephysProjectCache object
cache = EcephysProjectCache(manifest=manifest_path,
                            fetch_api=EcephysProjectWarehouseApi(RmaEngine(scheme="http",host="api.brain-map.org",timeout= 50 * 60)))          

# Create an instance of the Brain Observatory cache
boc = BrainObservatoryCache(manifest_file= manifest_path2)

# Download our session data 
session = cache.get_session_data(719161530)
print('Session downloaded.')


# ## Units

# Now that we have downloaded the session file, we can begin to explore our session object. The `units` property of our session object returns a dataframe that contains the recorded activity of our individual neurons. There are many metrics stored within `units` that can be used in your potential analyses. Some key metrics include:
# 
# - **firing rate**: mean spike rate during the entire session
# - **presence ratio**: fraction of session when spikes are present
# - **ISI violations**: rate of refractory period violations
# - **Isolation distances**: distance to nearest cluster in Mihalanobis space
# - **d'**: classification accuracy based on LDA
# - **SNR**: signal to noise ratio
# - **Maximum drift**: Maximum change in spike depth during recording
# - **Cumulative drift**: Cumulative change in spike depth during recording

# In[3]:


units_df = session.units
units_df.head()


# Just like we did before in our sessions dataframe, we can return the brain structures that our session's data was recorded from as well as how many neurons were recorded per brain area. 

# In[4]:


col = 'ecephys_structure_acronym'

print('Available Brain Structures:')
print(units_df[col].unique())
print('\n Brain Structure Frequency:')
print(units_df[col].value_counts())


# To ensure that the recordings we use in our analysis are all of good quality, we will filter the data according to the signal-to-noise ratio (`snr`) and the `ISI_Violations` of our neurons. Below we will plot the distributions of both.

# In[5]:


# Signal to noise distribution
col_1 = 'snr'
plt.hist(units_df['snr'], bins=30)
plt.title('Distribution of SNR')
plt.xlabel('Signal to Noise Ratio')
plt.ylabel('Frequency')
plt.show()


# In[6]:


# ISI distribution 
col_2 = 'isi_violations'
plt.hist(units_df[col_2], bins=30)
plt.title('Distribution of ISI Violations')
plt.xlabel('Rate of Refractory Period Violations')
plt.ylabel('Frequency')
plt.show()


# For the purposes of this tutorial, we will use `snr` values greater than 1 and `ISI_violation` values less than 0.1, define our quality neurons. 

# In[7]:


good_snr = units_df[units_df['snr']>1]
low_isi = units_df[units_df['isi_violations']<0.1]
combined_df = low_isi.merge(good_snr)
print('Number of Recordings with good SNR and Low ISI:')
print(len(combined_df))
combined_df.head()


# ## Firing Rate

# *Explaining Firing Rate*

# In[8]:


import seaborn as sns


# In[9]:


plt.figure(figsize = (10,5))
sns.violinplot(y='firing_rate', x='ecephys_structure_acronym',data = combined_df)
plt.title('Violinplot of Firing Rates across Brain Structures')
plt.show()


# ## Running Speed 

# *explain run speed and 2 photon/neuropixels connectivity*

# In[10]:


rs = session.running_speed
rs.head()


# In[11]:


y = rs['velocity']
x = rs['start_time']

# Plot it
plt.figure(figsize=(14,5))
plt.plot(x,y)
plt.xlabel('Time (seconds)')
plt.ylabel('Speed')
plt.show()


# In[12]:


# Assign previous container ID
exp_container_id = 627823571
stim = ['drifting_gratings']

# Get experiments for our container id and stimuli of interest
experiments = boc.get_ophys_experiments(experiment_container_ids = [exp_container_id],
                                     stimuli = stim)

# Assign the experiment id 
experiment_id = experiments[0]['id']
experiment_data = boc.get_ophys_experiment_data(experiment_id)

# Assign timestamps and deltaF/F
ts, dff = experiment_data.get_dff_traces()
dff_mean =np.mean(dff, axis = 0)
dff_mean.shape

print('Data acquired.')


# In[13]:


bin_size = 5 
bin_stamps = np.arange(0,ts.max(),bin_size)
num_bins = len(bin_stamps)

run_bin = np.empty(num_bins)
response_bin = np.empty(num_bins)

for i in range(num_bins):
    
    # Get the values within our time bin and take a mean
    run_bin[i] = y[np.where([(ts>i*bin_size), (ts<(i+1)*bin_size)].mean() 
    response_bin[i] = dff_mean[np.where([(ts>i*bin_size), (ts<(i+1)*bin_size)].mean()


# In[ ]:




