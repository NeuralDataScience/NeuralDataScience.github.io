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
import matplotlib.patches as mpatches

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

# Return units dataframe with specified snr and isi
units_df = session.units
good_snr = units_df[units_df['snr']>2]
good_units_df = good_snr[good_snr['isi_violations']<0.1]




print('Session downloaded.')


# ## Firing Rate 

# In our dataframe, the mean spike rates for each unit can be found under the `firing_rate` column. Let, look at the distibution of firing rates across all brain areas using a violinplot. 

# In[9]:


plt.figure(figsize = (10,5))
sns.violinplot(y='firing_rate', x='ecephys_structure_acronym',data = good_units_df)
plt.title('Violinplot of Firing Rates across Brain Structures')
plt.show()


# ## Spike Times

# Our `EcephysSession` object contains spike times for each unit and they can be accessed via the `spike_times` attribute. This returns a dictionary where the `unit_id` of the neural units in our session are mapped to a list of spike times.  With this data, we are able to compare `spike_times` across units and across stimuli by plotting a rasterplot. 
# 
# We first need to select a unit to focus on. For the purposes of this notebook we will work units that were taken from the primary visual area (`VISp`). Below, we will assign the spike times of a unit from the `VISp` area. 

# In[10]:


# Assign the spike times
all_spike_times = session.spike_times

# Assign a list of unit ids for units in VISp brain area
VISp_unit_ids = good_units_df[good_units_df['ecephys_structure_acronym'] == 'VISp'].index.values

# Assign spike times of first VISp entry 
first_VISp_units_id = VISp_unit_ids[0]
first_VISp_spike_times = all_spike_times[first_VISp_units_id]

# Return length of spike times and values for for VISp entry 
print('Spikes found for unit ' + str(first_VISp_units_id) + ': ' + str(len(all_spike_times[first_VISp_units_id])))

print(first_VISp_spike_times)


# With these spike times, we are able to create a raster plot for our unit of interst. Below we will plot out the first 50 seconds of the session. 

# In[11]:


plt.figure(figsize=(15,4))
plt.plot(first_VISp_spike_times, np.repeat(0,len(first_VISp_spike_times)), '|')
plt.xlim(0,50)
plt.xlabel('Time (s)')
plt.show()


# A raster plot maybe difficult to see the overall firing activity of a unit becasue there are too man spikes. Instead of looking at each individual spike across time, we can bin our spikes into 1 second bins and plot the spike frequency of each bin. 

# In[12]:


# Assign total number of bins 
numbins = int(np.ceil(first_VISp_spike_times.max()))
binned_spikes = np.empty((numbins))

# Assign the frequency of spikes over time
for i in range(numbins):
    binned_spikes[i] = len(first_VISp_spike_times[(first_VISp_spike_times>i)&(first_VISp_spike_times<i+1)])
    

plt.figure(figsize=(20,5))
plt.plot(binned_spikes)
plt.xlabel('Time (s)')
plt.ylabel('FR (Hz)')
plt.show()


# The plot above is only for one unit in our session. We can also compare spike times across multiple units by plotting their spike times over each other. 

# In[78]:


# Plot first 10 VISp entries spike times
numunits = 10
visp_binned = np.empty((numunits, numbins))

for i in range(numunits):
    unit_id = VISp_unit_ids[i]
    spikes = all_spike_times[unit_id]
    for j in range(numbins):
        visp_binned[i,j] = len(spikes[(spikes>j)&(spikes<j+1)])
        
plt.figure(figsize=(20,10))
for i in range(numunits):
    plt.plot(i+(visp_binned[i,:]/50), color='gray')


# ## Stimulus Presentations

# The spike data can be sorted according to the type of stimulus that was presented to the mouse. You can access the different stimuli that were presented in the session by using the attribute `stimulus_names`. 

# In[30]:


# Stimuli presented in session
all_stims = session.stimulus_names
all_stims


# Each stimulus contains a set of parameters that were used when presented to the mouse. For example two gabors stimuli may be presented, but they may have differing temporal frequencies or different x and y positions. Ececuting the `stimulus_presentations` method on our session object will return a pandas dataframe with parameters for each stimulus as the columns which we can use to compare the resoponses of units to different stimulus presentations. 

# **Note**: Not all stimuli share the same parameters. If certain parameters do not apply to a stimulus, you will see a `null` value. 

# In[15]:


# Stimulus presentation dataframe 
stim_pres = session.stimulus_presentations
stim_pres.head()


# Each stimulus used in the session is presented to the mouse in various timeblocks. Using the `get_stimulus_epochs()` method will return a pandas dataframe containing the time periods where a single stimulus type was presented continuously. 

# In[16]:


# Continous timeblocks where only 1 type of stimulus was presented
# Could maybe use this w/ running speed
stim_timeblocks = session.get_stimulus_epochs()
stim_timeblocks.head()


# The timeblocks above allow us to compare neural activity of the units when a new stimulus is being presented. By using `plt.axvspan` we can divide our current plot to show when one stimulus ends and a new one begins. Plotting this over the firing rates of our units will reveal what `stimulus_name` elicited the highest neural activity. 

# In[42]:


plt.figure(figsize=(20,10))

# Plots firing rates 
for i in range(numunits):
    plt.plot(i+(visp_binned[i,:]/30.), color='gray')

# Plots rectangle blocks that indicate new stimulus presentation 
colors = ['red','blue','orange','purple', 'yellow', 'green', 'pink', 'violet']
for c, stim_name in enumerate(all_stims):
    stim = stim_timeblocks[stim_timeblocks['stimulus_name']==stim_name]
    for j in range(len(stim)):
        plt.axvspan(xmin=stim['start_time'].iloc[j], xmax=stim['stop_time'].iloc[j], color=colors[c], alpha=0.1)

# Legend showing stimulus timeblocks
colors_leg = []
for i in range(len(colors)):
    temp_color = mpatches.Patch(color = colors[i], label = (all_stims[i]))
    colors_leg.append(temp_color)  
plt.legend(handles = colors_leg)

plt.show()


# Alternatively, you could use the `get_stimulus_table()` method to return a subset of stimulus presentation by `stimulus_name`. The returned dataframe will only contain parameters that relate to the given `stimulus_name`. Below we will investigate how our neuronal units responded to a `natural_scenes` stimulus presentations.

# In[45]:


natural_scenes_df = session.get_stimulus_table(['natural_scenes'])
natural_scenes_df.head()


# We can look even further and check how the parameters of a stimulus affected the firing rate. In `natural_scenes` presentations, different frame/image was presented to the mouse. Below we will focus on the times that the first `frame` in our dataframe above, was presented in the session. 

# In[46]:


# Assign indices of dataframe
natural_scenes_ids = natural_scenes_df.index

# Assign first 'natural_scenes' image presented in the session
my_image = natural_scenes_df.loc[natural_scenes_ids[1], 'frame']

# Return the number of times this image was presented
print('Number of times frame ' + str(my_image)+ ' was presented in the session:')
print(len(natural_scenes_df[natural_scenes_df['frame']==my_image]))


# As you can see from the dataframe above, the `natural_scenes` presentations also cotain start and end times. We can do what we did before and use `plt.axvspan()` to plot the times when the images of interest was presented over the firing rates of our session. 

# In[49]:


plt.figure(figsize=(20,10))

# Assign a dataframe that only contains presentations of our image of interest
stim_subset = natural_scenes_df[natural_scenes_df['frame']==my_image]

# Offset the firing rates and plot them
for i in range(numunits):
    plt.plot(i+(visp_binned[i,:]/50), color='gray')

# Plot the times are image of interest was presented
for j in range(len(stim_subset)):
    plt.axvspan(xmin=stim_subset['start_time'].iloc[j], xmax=stim_subset['start_time'].iloc[j], color='r', alpha=0.5)

plt.title('Presentation of Image Frame ' + str(my_image))
plt.xlabel('Time (s)')
plt.ylabel('Units')
plt.xlim(5000,9000)
plt.show()


# You are not limited to only plotting the the times where a certain image was presented, nor are you limited to only plotting `natural_scenes` stimuli. You can create a similar graph with `gabors`, `flashes`, or any other availabe `stimulus_name`. For example, you can plot all the times when a `gabors` stimulus was presented at a cetain spatial frequncy, temporal frequency, or orientaion.    

# ## Running Speeds

# The running speed of the mice in our session have also been recorded and are available to you. You can acess the running speed by calling `running_speed` on our `EcephysSession` object. This will return a pandas dataframe that contains the `start_time`, `end_time`, and `velocity` of our session.

# In[51]:


running_speed = session.running_speed

plt.plot(running_speed['end_time'], running_speed['velocity'])
plt.title('Running Speed: Session 721123822')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (cm/s)')
plt.show()


# With the running speed, we can ask if their is correlation between the firing rates of our units and the velocity of our mouse. Similar to how we plotted above, we can plot the running speed of the session over the firing rates and see if increases in running speed align with more neural activity. 

# In[77]:


plt.figure(figsize=(20,10))
for i in range(numunits):
    plt.plot(i+20+(visp_binned[i,:]/10), color='gray')

plt.plot(running_speed['end_time'], (running_speed['velocity']*0.1))

for c, stim_name in enumerate(all_stims):
    stim = stim_timeblocks[stim_timeblocks['stimulus_name']==stim_name]
    for j in range(len(stim)):
        plt.axvspan(xmin=stim['start_time'].iloc[j], xmax=stim['stop_time'].iloc[j], color=colors[c], alpha=0.1)

plt.legend(handles = colors_leg)
plt.ylim(-10,50)
plt.show()


# ## Signal Correlations

# In[15]:


spf = flashes_histogram[0]
max_len = spf.shape[0]


# In[16]:


# get two spike trains in flashes activity
spike_train_1_flash=spf[:max_len, 0]
spike_train_2_flash=spf[:max_len, 9]


# In[17]:


fig, ax = plt.subplots(1, 2,figsize=(10,4))

ax[0].plot(spike_train_1_flash)
ax[0].set_ylabel('Spike count 1')
ax[0].set_xlabel('Time bins (10 ms)')

ax[1].plot(spike_train_2_flash)
ax[1].set_ylabel('Spike count 2')
ax[1].set_xlabel('Time bins (10 ms)')
plt.show()


# In[18]:


# compute the correlogram for spontaneous activity
xcorr_flashes = sp.signal.correlate(spike_train_1_flash,spike_train_2_flash)

# time steps
time_shift_flashes = np.arange(-len(xcorr_flashes)/2,len(xcorr_flashes)/2,1)


# In[19]:


plt.figure(figsize=(14,8))
plt.plot(time_shift_flashes,xcorr_flashes)
plt.ylabel('Signal correlation')
plt.xlabel('Time steps (10 ms)')
plt.title('Flashes Stimulus Presentation')
plt.show()


# In[25]:


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


# In[26]:


spike_statistics = session.conditionwise_spike_statistics(stimulus_presentation_ids = flashes_presentation_ids,
                                                          unit_ids = None)

spike_statistics.head()


# In[ ]:




