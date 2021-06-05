#!/usr/bin/env python
# coding: utf-8

#  # Obtaining Raw Electrophysiology Data

# This section will teach you how to interact with the Neuropixels dataset, specifically how to download experimental sessions, return procesed data, and subset your data to contain only brain regions you are interested in. 
# 
# We will first need to import the `EcephysProjectCache` from the Allen SDK and create an instance of the class. The class is used to download the metadata and data for all sessions in the Neuropixels dataset. For the full list of methods, please visit the `allensdk.brain_observatory.ecephys.ecephys_project_cache` module documentation on the <a href = 'https://allensdk.readthedocs.io/en/v1.7.1/allensdk.brain_observatory.ecephys.ecephys_project_cache.html'>Allen SDK website</a>. We'll create an instance of `EcephysProjectCache` with a larger `timeout` value to ensure enough time is allowed for our session file to download below. 
# 
# Below we will execute `get_session_table()` on our `EcephysProjectCache` object which will return a dataframe with metadata on each session.

# In[1]:


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


# In[2]:


# # Import packages necessary to plot behavior
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')
import allensdk.brain_observatory.ecephys.visualization as ecvis

# Import the Neuropixels Cache
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache
from allensdk.brain_observatory.ecephys.ecephys_project_api import EcephysProjectWarehouseApi
from allensdk.brain_observatory.ecephys.ecephys_project_api.rma_engine import RmaEngine

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
# In this dataset, a `unit` referes to an individual neuron that was recorded in the session. The `unit_count` refers to the total number of neurons recorded in a particluar sesssion. As mentioned in the chapter introduction, three different genotypes were used alongside the wildtype for these experiments. You can find the genotype under `full_genotype`. Lastly, you can find what structures the data in a session was collected from under `ecephys_structure_acronyms`.
# 
# Below we will return the follwoing information on our sessions: 
# - how many sessions per genotype
# - the average number of units recorded per session
# - what brain structures were used in our sessions

# In[39]:


col_1 = 'full_genotype'
genotypes = sessions[col_1].value_counts()

col_2 = 'unit_count'
avg_units = sessions[col_2].mean()

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


# Let's say we only want sessions where the data has recordings from VISp. We can do the following to create a session list that we want.

# In[40]:


# Create a session list based on some criteria

session_list = []

for idx,structure_list in enumerate(sessions['ecephys_structure_acronyms']):
    if 'VISp' in structure_list:
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
# The `get_session_data` downloads the `NWB` data file of our experiment session and returns a session object that contains data and metadata for a single session. For a full list of methods and attributes for an ecephys session object, please visit the <a href = 'https://allensdk.readthedocs.io/en/v1.7.1/allensdk.brain_observatory.ecephys.ecephys_session.html'> Allen SDK session module documentation</a>. Here, we'll just take one session as an example.

# **Note**: The session files are very large files that will take some time to download depending on your connection speed. It is important that you do not stop the download as the cell is running becasue this will truncate the file and you will not be able to work with the data.

# In[41]:


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

# In[42]:


# Return units dataframe
units_df = session.units
units_df.head()


# To ensure that the recordings we use in our analysis are all reliable and of good quality, we will filter the data according to the signal-to-noise ratio (`snr`) and the `ISI_Violations` of our neurons. Below we will plot the distributions of both.

# In[43]:


# Signal to noise distribution
col_3 = 'snr'

plt.figure(figsize = [5,5])
plt.hist(units_df[col_3], bins=30)
plt.title(f'Distribution of {col_3}')
plt.xlabel('Signal to Noise Ratio')
plt.ylabel('Frequency')
plt.show()


# In[44]:


# ISI distribution 
col_4 = 'isi_violations'

plt.figure(figsize = [5,5])
plt.hist(units_df[col_4], bins=30)
plt.title('Distribution of ISI Violations')
plt.xlabel('Rate of Refractory Period Violations')
plt.ylabel('Frequency')
plt.show()


# For the purposes of this tutorial, we will focus on units with `snr` values greater than 2 and `ISI_violation` values less than 0.1.

# In[45]:


# Create dataframe from units that fit criteria
good_snr = units_df[units_df[col_3]>2]
good_units_df = good_snr[good_snr[col_4]<0.1]


print('Number of Recordings with good SNR and low ISI:')
print(len(good_units_df))
good_units_df.head()


# ## Obtaining Single Sction Potential Waveforms 

# Each session contains a dictionary of mean waveforms for all the units recorded in that session. They are stored inside a xarray DataArray where the `unit_id` are mapped to the mean spike waveform values. The dimensions of the DataArrays are `channel` and `time` which are recorded in microvolts and seconds, respectivley. For more information on `xarray.DataArray`, please visit the <a href = 'http://xarray.pydata.org/en/stable/generated/xarray.DataArray.html'> xarray original documentation</a>.
# 
# To access the mean spike waveforms for all units in a session, use the attribute `mean_waveforms` on your `EcephysSession` object. 

# In[46]:


all_mean_waveforms = session.mean_waveforms
print('Total number of waveforms:')
print(len(all_mean_waveforms))


# We can plot the mean waveforms of our units with the method `plot_mean_waveforms` from the ecephys visualization package. The method uses the `mean_waveforms` dictionary, `unit_id`'s, and `peak_channel_id`'s as arguments. For more information on this method, visit the `allensdk.brain_observatory.ecephys.visualization` package documentation on the <a href = 'https://allensdk.readthedocs.io/en/latest/allensdk.brain_observatory.ecephys.visualization.html'> Allen Brain Atlas website</a>.
# 
# Below we will compare mean waveforms from units of different brain areas. We will be looking at one wavefrom from the `CA1`, `LP`, `DG`, `VISp`. We first need to create a list of unit_id's for the units we are interested in. 

# In[47]:


# Assign Unit IDs of different brain areas of interest
col_of_interest = 'ecephys_structure_acronym'
CA1_unit_ids = good_units_df[good_units_df[col_of_interest] == 'CA1'].index
LP_unit_ids = good_units_df[good_units_df[col_of_interest] == 'LP'].index
DG_unit_ids = good_units_df[good_units_df[col_of_interest] == 'DG'].index
VISp_unit_ids = good_units_df[good_units_df[col_of_interest] == 'VISp'].index

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

# In[48]:


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


# In[ ]:




