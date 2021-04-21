#!/usr/bin/env python
# coding: utf-8

# # Large Scale Single Cell Electrophysiology & Behavior

# In[1]:


# This will ensure that the AllenSDK is installed.
# If not, it will install it for you.
try:
    import allensdk
    print('allensdk already installed.')
except ImportError as e:
    get_ipython().system('pip install allensdk')


# In[2]:


# Import necessary packages 
import numpy as np 
import pandas as pd 
import scipy as sp
import seaborn as sns
from scipy import signal
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Import the Neuropixels Cache
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache
from allensdk.brain_observatory.ecephys.ecephys_project_api import EcephysProjectWarehouseApi
from allensdk.brain_observatory.ecephys.ecephys_project_api.rma_engine import RmaEngine

# Import packages necessary to plot behavior
import allensdk.brain_observatory.ecephys.visualization as ecvis
from allensdk.brain_observatory.visualization import plot_running_speed

# Assign where neuropixels data and 2-photon data will be stored
manifest_path = 'manifest.json' 


# Create the EcephysProjectCache object
cache = EcephysProjectCache(manifest=manifest_path,
                            fetch_api=EcephysProjectWarehouseApi(RmaEngine(scheme="http",host="api.brain-map.org",timeout= 50 * 60)))          

# Download our session data 
session = cache.get_session_data(721123822)
print('Session downloaded.')


# ## Units

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

# In[3]:


# Return units dataframe
units_df = session.units
units_df.head()


# To ensure that the recordings we use in our analysis are all of good quality, we will filter the data according to the signal-to-noise ratio (`snr`) and the `ISI_Violations` of our neurons. Below we will plot the distributions of both.

# In[4]:


# Signal to noise distribution
col_1 = 'snr'
plt.hist(units_df['snr'], bins=30)
plt.title('Distribution of SNR')
plt.xlabel('Signal to Noise Ratio')
plt.ylabel('Frequency')
plt.show()


# In[5]:


# ISI distribution 
col_2 = 'isi_violations'
plt.hist(units_df[col_2], bins=30)
plt.title('Distribution of ISI Violations')
plt.xlabel('Rate of Refractory Period Violations')
plt.ylabel('Frequency')
plt.show()


# For the purposes of this tutorial, we will use `snr` values greater than 2 and `ISI_violation` values less than 0.1, define our good quality units. 

# In[6]:


# Create dataframe with our conditions of interest
good_snr = units_df[units_df['snr']>2]
good_units_df = good_snr[good_snr['isi_violations']<0.1]


print('Number of Recordings with good SNR and Low ISI:')
print(len(good_units_df))
good_units_df.head()


# Just like we did before in our sessions dataframe, we can return the brain structures that our session's data was recorded from as well as how many neurons were recorded per brain area. 

# In[7]:


col = 'ecephys_structure_acronym'

print('Available Brain Structures:')
print(good_units_df[col].unique())
print('\n Brain Structure Frequency:')
print(good_units_df[col].value_counts())


# ## Firing Rate 

# In our dataframe, the mean spike rates for each unit can be found under the `firing_rate` column. Let, look at the distibution of firing rates across all brain areas using a violinplot. 

# In[8]:


plt.figure(figsize = (10,5))
sns.violinplot(y='firing_rate', x='ecephys_structure_acronym',data = good_units_df)
plt.title('Violinplot of Firing Rates across Brain Structures')
plt.show()


# ## Waveforms 

# Each session contains a dictionary of mean waveforms for all the units recorded in that session. They are stored inside a xarray DataArray where the `unit_id` are mapped to the mean spike waveform values. The dimensions of the DataArrays are `channel` and `time` which are recorded in microvolts and seconds, respectivley. For more information on `xarray.DataArray`, please visit, <a href = 'http://xarray.pydata.org/en/stable/generated/xarray.DataArray.html'> here</a>.
# 
# To access the mean spike waveforms for all units in a session, use the attribute `mean_waveforms` on your `EcephysSession` object. 

# In[9]:


all_mean_waveforms = session.mean_waveforms
print('Total number of waveforms:')
print(len(all_mean_waveforms))


# We can plot the mean waveforms of our units with the method `plot_mean_waveforms` from the ecephys visualization package. The method uses the `mean_waveforms` dictionary, `unit_id`'s, and `peak_channel_id`'s as arguments. For more information on this method, visit <a href = 'https://allensdk.readthedocs.io/en/latest/allensdk.brain_observatory.ecephys.visualization.html'> here</a>.
# 
# Below we will compare mean waveforms from different brain areas. We will be looking at one wavefrom from the `CA1`, `LP`, `DG`, `VISp`. We first need to create a list of unit_id's for the waveforms we are interested in. 

# In[10]:


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

# In[11]:


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

print(uois_df['ecephys_structure_acronym'] )

plt.show()


# ## Stimulus Presentations

# The spike data can be sorted according to the type of stimulus that was presented to the mouse. You can access the different stimuli that were presented in the session by using the attribute `stimulus_names`. Each stimulus contains a set of parameters that were used when presented to the mouse. For example two gabors stimuli may be presented, but they may have differing temporal frequencies or different x and y positions. 
# 
# Ececuting the `stimulus_presentations` method on our session object will return a pandas dataframe with parameters for each stimulus as the columns which we can use to compare the resoponses of units to different stimulus presentations. 

# In[12]:


# Stimulus presentation dataframe 
stim_pres = session.stimulus_presentations

# Stimuli presented in session
all_stims = session.stimulus_names

# Continous timeblocks where only 1 type of stimulus was presented
# Could maybe use this w/ running speed
stim_timeblocks = session.get_stimulus_epochs()


all_stims


# In[13]:


stim_pres.head()


# In[14]:


stim_timeblocks.head()


# Alternatively, you could use the `get_stimulus_table()` method to return a subset of stimulus presentation by `stimulus_name`. Below we will investigate how our neuronal units responded to a `flashes` stimulus presentations.

# In[15]:


flashes_df = session.get_stimulus_table(['flashes'])
flashes_df.head()


# Our goal will be to plot the spike trains of a unit according to the `stimulus_presentation_id` that were presented. We can use `presentationwise_spike_counts` to build an array of spike counts. We will need to specify the `bin_edges` and `stimulus_presentation_ids` to execute this method. The duration of a presented stimulus is roughly 0.25 seconds, so we will create time bins of 0.01 seconds. 

# In[16]:


# Assign the duration of a presented stimulus
first_flashes_id = flashes_df.index[0]
first_flashes_duration = flashes_df.loc[first_flashes_id, 'duration']

# Create bins for our timestamps
time_step = 1/100
timestamps = np.arange(0.0, (first_flashes_duration + time_step), time_step)

timestamps


# In[17]:


# Build your array of spike counts
flashes_histogram = session.presentationwise_spike_counts(
    bin_edges = timestamps,
    stimulus_presentation_ids = flashes_df.index,
    unit_ids = None)

flashes_histogram


# We have created our time bins and built our array of spike counts and are ready to plot our neuorns' reponses to stimulus presentations. As you can see, `flashes_histogram` is not a normal array, it is an `xarray.DataArray` which we have not see before. An `xarray.DataArray` can be thought of as a NumPy array with labled axes and indices. An `xarray.DataArray` contains dimensions, which tell you what each axes in the array is, and coordiates which label each dimension. For more information on `xarray.DataArray` objects, please visit <a href = 'http://xarray.pydata.org/en/stable/generated/xarray.DataArray.html'> here</a>.
# 
# Below we plot the spike trains of the first unit in `flashes_histogram` for the first 10 `stimulus_presentation_ids`.

# In[18]:


# Plot the first unit's response to the first 10 presentations of flashes
for i in range(10):   
    plt.plot(flashes_histogram.time_relative_to_stimulus_onset, i+flashes_histogram[i,:,0])
plt.xlabel("Time (s)", fontsize=16)
plt.ylabel("Presentation", fontsize=16)
plt.title("Response of Unit 950907205")
plt.show()


# We can also plot the mean number of spikes of all the units across all presentations. Below we will take the mean of all spike counts for presentations of the flashes `stimulus_name`. We willl be using `xrplot` to plot our heatmap of mean spike counts. For information on how to use `xrplot`, please visit <a href = 'http://xarray.pydata.org/en/stable/plotting.html'> here</a>.

# In[19]:


# Assign the mean spike times of all units' responses to flashes presentations 
mean_flash_histogram = flashes_histogram.mean(dim = 'stimulus_presentation_id')
mean_flash_histogram.coords

import xarray.plot as xrplot
xrplot.imshow(darray=mean_flash_histogram, x="time_relative_to_stimulus_onset",
                                      y="unit_id")
plt.title('Mean Spike Counts on Flash Presentations')
plt.show()


# In[20]:


spf = flashes_histogram[0]
max_len = spf.shape[0]


# In[21]:


# get two spike trains in flashes activity
spike_train_1_flash=spf[:max_len, 0]
spike_train_2_flash=spf[:max_len, 9]


# In[22]:


fig, ax = plt.subplots(1, 2,figsize=(10,4))

ax[0].plot(spike_train_1_flash)
ax[0].set_ylabel('Spike count 1')
ax[0].set_xlabel('Time bins (10 ms)')

ax[1].plot(spike_train_2_flash)
ax[1].set_ylabel('Spike count 2')
ax[1].set_xlabel('Time bins (10 ms)')
plt.show()


# In[23]:


# compute the correlogram for spontaneous activity
xcorr_flashes = sp.signal.correlate(spike_train_1_flash,spike_train_2_flash)

# time steps
time_shift_flashes = np.arange(-len(xcorr_flashes)/2,len(xcorr_flashes)/2,1)


# In[24]:


plt.figure(figsize=(14,8))
plt.plot(time_shift_flashes,xcorr_flashes)
plt.ylabel('Signal correlation')
plt.xlabel('Time steps (10 ms)')
plt.title('Flashes Stimulus Presentation')
plt.show()


# ## Spike Times

# Our `EcephysSession` object contains spike time for each unit and they can be accessed via the `spike_times` attribute. With this data, we are able to compare spike times across units and across stimuli by plotting a rasterplot. 
# 
# We first need to select a unit to focus on. Below, we will assign the spike times of a unit from the CA1 area. 

# In[25]:


# Assign the first CA1 spike times array by subselecting with unit_id
all_spike_times = session.spike_times
first_CA1_spike_times = all_spike_times[first_CA1_units_ids]

# Return length of spike times and values
print('Spikes found for unit ' + str(first_CA1_units_ids) + ': ' + str(len(all_spike_times[first_CA1_units_ids])))

print(first_CA1_spike_times)


# We can sort the neural spikes according to what stimulus stimulus was presented in the session in order to look for any correlation in nerual activity. The `presentationwise_spike_counts()` method returns an array of spike counts according to the stimulus presented and the onset time. You will need to specify the presentation_ids when calling the method. 
# 
# Once we have our spike count array, we can create a rasterplot using `raster_plot()`. For more information on how to use `raster_plot()`, please visit<a href = 'https://allensdk.readthedocs.io/en/latest/allensdk.brain_observatory.ecephys.visualization.html'> here</a>.

# In[26]:


# Return presentation ids from stimulus presentation dataframe for 'flashes' stimulus
flashes_presentation_ids = stim_pres.loc[(stim_pres['stimulus_name'] == 'flashes')].index.values


times = session.presentationwise_spike_times(
    stimulus_presentation_ids=flashes_presentation_ids,
    unit_ids= None)

# Assign the stimulus presentation id
first_flashes_presentation_id = times['stimulus_presentation_id'].values[0]

# Assign recording times for 'flashes' stimulus presentations
plot_times = times[times['stimulus_presentation_id'] == first_flashes_presentation_id]

# Assign Raster plot 
ecvis.raster_plot(plot_times, title = 'Raster Plot for stimulus presentation 3647')

plt.show()

print('Parameters for presentation 3647')
stim_pres.loc[first_flashes_presentation_id]


# In[27]:


spike_statistics = session.conditionwise_spike_statistics(stimulus_presentation_ids = flashes_presentation_ids,
                                                          unit_ids = None)

spike_statistics.head()


# ## Running Speeds

# In[ ]:




