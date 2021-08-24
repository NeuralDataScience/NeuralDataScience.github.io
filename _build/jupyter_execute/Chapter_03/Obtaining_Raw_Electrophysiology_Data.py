#!/usr/bin/env python
# coding: utf-8

# # Obtaining  Electrophysiology Data from the AllenSDK
#  
# The [Visual Coding - Neuropixels dataset from the Allen Institute of Brain Sciences](https://portal.brain-map.org/explore/circuits/visual-coding-neuropixels) records spiking activity in the visual system of the mouse brain. At the time of writing, this dataset contains a total of 58 experiment sessions from Neuropixels probes in the cortex, hippocampus, and thalamus. There are three different trangenic mouse lines used in the experiments alongside the wild-type mice, which mark three different inhibitory cell types. The stimuli presented in this dataset range from natural scenes to drifting gratings. 
# 
# In this chapter you will learn how to download and sort through the Neuropixels dataset. Once you learn the basics, you will learn how to perform possible analyses to explain the neural activity within, as well as how to use optogenetics to identify different cell types within the data. 
# 
# This section will teach you how to interact with the Allen Institute Neuropixels dataset, specifically how to download experimental sessions, return processed data, and subset your data to contain only brain regions you are interested in. 
# 
# First things first, let's make sure you have the AllenSDK installed. See the [Allen Institute website](https://alleninstitute.github.io/AllenSDK/install.html) for information on installing it, otherwise, the cell below will do it for you.

# In[20]:


# This will ensure that the AllenSDK is installed.
# If not, it will install it for you.
try:
    import allensdk
    if allensdk.__version__ == '2.11.2':
        print('allensdk already installed.')
    else:
        print('incompatible version of allensdk installed')
except ImportError as e:
    get_ipython().system('pip install allensdk')


# We will first need to import the `EcephysProjectCache` from the Allen SDK and create an instance of the class. The class is used to download the metadata and data for all sessions in the Neuropixels dataset. For the full list of methods, please visit the `allensdk.brain_observatory.ecephys.ecephys_project_cache` module documentation on the <a href = 'https://allensdk.readthedocs.io/en/v1.7.1/allensdk.brain_observatory.ecephys.ecephys_project_cache.html'>Allen SDK website</a>. We'll create an instance of `EcephysProjectCache` with a larger `timeout` value to ensure enough time is allowed for our session file to download below. 
# 
# Below we will execute `get_session_table()` on our `EcephysProjectCache` object which will return a dataframe with metadata on each session.

# In[21]:


# # Import packages necessary to plot behavior
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')

# Import allensdkd brain observatory packages
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache
from allensdk.brain_observatory.ecephys.ecephys_project_api import EcephysProjectWarehouseApi
from allensdk.brain_observatory.ecephys.ecephys_project_api.rma_engine import RmaEngine
import allensdk.brain_observatory.ecephys.visualization as ecvis

# Assign where data will be stored
manifest_path = 'manifest.json' 

# Create the EcephysProjectCache object
cache = EcephysProjectCache(manifest=manifest_path,
                            fetch_api=EcephysProjectWarehouseApi(RmaEngine(scheme="http",host="api.brain-map.org",timeout= 50 * 60)))    

# Return all sessions available in this dataset
sessions = cache.get_session_table()
print('Total number of sessions: ' + str(len(sessions)))
sessions.head()


# A few columns that we may want to pay attention to for future analysis are the `full_genotype`, `unit_count`, and `ecephys_structure_acronyms`. 
# 
# In this dataset, a `unit` referes to an individual neuron that was recorded in the session. The `unit_count` refers to the total number of neurons recorded in a particular sesssion. As mentioned in the chapter introduction, three different genotypes of mice were used alongside the wildtype mice for these experiments. You can find the genotype under `full_genotype`. Lastly, you can find what structures the data in a session was collected from under `ecephys_structure_acronyms`.
# 
# Below we will return the following information on our sessions: 
# - how many sessions per genotype
# - the average number of units recorded per session
# - what brain structures were used in our sessions

# In[22]:


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

print('\nAverage Units:',avg_units)

print('\nAll brain areas:')
print(brain_areas)


# Let's say we only want sessions where the data has recordings from primary visual cortex (VISp). We can do the following to create a session list that we want.

# In[23]:


session_list = []

for idx,structure_list in enumerate(sessions['ecephys_structure_acronyms']):
    if 'VISp' in structure_list:
        session_list.append(sessions.index[idx])   
        
print('There are '+str(len(session_list))+' sessions that meet this criteria:')
print(session_list)


# ## Downloading a Single Session & the Structure of Session Files

# Now, we can use the session list to get the data we need. Unfortunately, we can only extract one experiment at a time, so if you want to do this for multiple experiments, you'll need to loop over the `get_session_data` method for your entire session_list. For example, your workflow might be:
# 
# 1. Extract one session.
# 2. Look for units recorded from your brain region of interest in that session.
# 3. Extract whatever metric you're interested in (e.g., firing rate).
# 4. Append those values to a list of firing rates.
# 5. Loop back around to the next session.
# 
# The `get_session_data` downloads the `NWB` data file of our experiment session and returns a session object that contains data and metadata for a single session. For a full list of methods and attributes for an ecephys session object, please visit the <a href = 'https://allensdk.readthedocs.io/en/v1.7.1/allensdk.brain_observatory.ecephys.ecephys_session.html'> Allen SDK session module documentation</a>. Here, we'll just take one session as an example.

# **Note**: The session files are very large files that will take some time to download depending on your connection speed. It is important that you do not stop the download as the cell is running because this will truncate the file and you will not be able to work with the data.

# In[33]:


# Download our single session data 
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
# For a full list of methods and attributes that can be called on an `EcephysSession` object, please review the original documentation for the <a href = 'https://allensdk.readthedocs.io/en/v1.7.1/allensdk.brain_observatory.ecephys.ecephys_session.html'> ecephys_session module</a>.

# In[26]:


# Return units dataframe
units_df = session.units
units_df.head()


# To ensure that the recordings we use in our analysis are all reliable and of good quality, we will filter the data according to the signal-to-noise ratio (`snr`) and the `ISI_Violations` of our neurons. Below we will plot the distributions of both.

# In[27]:


fig,ax = plt.subplots(1,2,figsize=(10,3))

# Signal to noise distribution
ax[0].hist(units_df['snr'], bins=30)
ax[0].set_xlabel('Signal to Noise Ratio')
ax[0].set_ylabel('Frequency')

# ISI Violations
ax[1].hist(units_df['isi_violations'], bins=30)
ax[1].set_xlabel('Rate of Refractory Period Violations')
ax[1].set_ylabel('Frequency')

plt.show()


# For the purposes of this tutorial, we will focus on units with `snr` values greater than 2 and `ISI_violation` values less than 0.1.

# In[30]:


# Create dataframe from units that fit criteria
good_snr = units_df[units_df['snr']>2]
good_units_df = good_snr[good_snr['isi_violations']<0.1]

print('Number of units with good SNR and low ISI:',len(good_units_df))
good_units_df.head()


# ## Obtaining Single Action Potential Waveforms 

# Each session contains a dictionary of mean waveforms for all the units recorded in that session. They are stored inside a xarray DataArray where the `unit_id` are mapped to the mean spike waveform values. The dimensions of the DataArrays are `channel` and `time` which are recorded in microvolts and seconds, respectivley. For more information on `xarray.DataArray`, please visit the <a href = 'http://xarray.pydata.org/en/stable/generated/xarray.DataArray.html'> xarray original documentation</a>.
# 
# To access the mean spike waveforms for all units in a session, use the attribute `mean_waveforms` on your `EcephysSession` object. 

# In[29]:


all_mean_waveforms = session.mean_waveforms
print('Total number of waveforms:',len(all_mean_waveforms))


# We can plot the mean waveforms of our units with the method `plot_mean_waveforms` from the ecephys visualization package. The method uses the `mean_waveforms` dictionary, `unit_id`'s, and `peak_channel_id`'s as arguments. For more information on this method, visit the `allensdk.brain_observatory.ecephys.visualization` package documentation on the <a href = 'https://allensdk.readthedocs.io/en/latest/allensdk.brain_observatory.ecephys.visualization.html'> Allen Brain Atlas website</a>.
# 
# Below we will compare mean waveforms from units of different brain areas. We will be looking at one wavefrom from the `CA1`, `LP`, `DG`, `VISp`. We first need to create a list of unit_id's for the units we are interested in. 

# In[31]:


# Assign Unit IDs of different brain areas of interest
CA1_unit_ids = good_units_df[good_units_df['ecephys_structure_acronym'] == 'CA1'].index
LP_unit_ids = good_units_df[good_units_df['ecephys_structure_acronym'] == 'LP'].index
DG_unit_ids = good_units_df[good_units_df['ecephys_structure_acronym'] == 'DG'].index
VISp_unit_ids = good_units_df[good_units_df['ecephys_structure_acronym'] == 'VISp'].index

# Return first entry of our brain areas of interst
first_CA1_units_ids = CA1_unit_ids[0]
first_LP_units_ids = LP_unit_ids[0]
first_DG_units_ids = DG_unit_ids[0]
first_VISp_units_ids = VISp_unit_ids[0]
uoi_ids = [first_CA1_units_ids, first_LP_units_ids, first_DG_units_ids, first_VISp_units_ids]

# Return dataframe
uoi_df = good_units_df.loc[uoi_ids]

uoi_df


# Using the `unit_ids`, we can create our own dictionary that maps our units of interest to their `mean_waveforms` array.

# In[32]:


# Create dictionary of waveforms that only include units of interest
waveforms_oi = {}
for ids in uoi_ids:
    waveforms_oi[ids] = all_mean_waveforms[ids]

# Create dictionary of peak channels that only include units of interest
peak_channels_oi = {}
for ids in uoi_ids:
    peak_channels_oi[ids] = good_units_df.loc[ids, 'peak_channel_id']

# Plot mean waveforms
ecvis.plot_mean_waveforms(waveforms_oi, uoi_ids, peak_channels_oi)

legend_list = list(uoi_df['ecephys_structure_acronym'] )
plt.legend(legend_list)
plt.show()


# ### Additional Resources
# 
# * [Allen Institute Tutorial Notebook](https://allensdk.readthedocs.io/en/latest/_static/examples/nb/ecephys_session.html)
