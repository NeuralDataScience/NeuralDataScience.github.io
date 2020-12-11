#!/usr/bin/env python
# coding: utf-8

# # Plotting a Signle Sweep of Data

# In[1]:


#Import all necessay packages and initialize the cache as 'ctc' (cell types cache)
from allensdk.core.cell_types_cache import CellTypesCache

from allensdk.api.queries.cell_types_api import CellTypesApi

ctc = CellTypesCache(manifest_file='cell_types/manifest.json')

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt


# In this section 

# In[2]:


# redownload the metadata for our cells
all_cells = ctc.get_cells()
all_cells_df = pd.DataFrame(all_cells).set_index('id')
all_cells_df.head(3)


# At this point, you might have realized that this dataframe doesn't contain any data about the electrophysiology. In order to get information about the electrophysiological properties of these cells, we need to use the get_ephys_features() method on our instance of the cell types cache.

# Just as we did before, we will will assign the output of get_ephys_features() to a variable and then convert it into a pandas dataframe.

# In[3]:


ephys_features = pd.DataFrame(ctc.get_ephys_features()).set_index('specimen_id')
ephys_features.head()


# Again, we can combine our dataframe that contians the metadata of our cells with our electrophysiology dataframe to create one single dataframe.

# In[4]:


all_ephys_features = all_cells_df.join(ephys_features)
all_ephys_features.head()


# The get_ephys_data() method can download electrophysiology traces for a single cell in the database. This method returns a class instance with helper methods for retrieving stimulus and response traces out of an NWB file. In order to use this method, you must specify the id of the cell specimen whose electrophysiology you would like to download.

# In[5]:


cell_id_2 = 525011903
specimen_ephys_data = ctc.get_ephys_data(specimen_id = cell_id_2)
sweep_numbers = specimen_ephys_data.get_experiment_sweep_numbers()
print(sweep_numbers[0:10])
#specimen1_ephys.get_sweep_metadata(100)
#specimen1_ephys.get_spike_times(100)


# In[6]:


sweep_number = 100
sweep_data = specimen_ephys_data.get_sweep(sweep_number)


# Now that you've pulled down some data, chosen a cell, and chosen a sweep number, let's plot that data.

# In[7]:


# Get the stimulus trace (in amps) and convert to pA
stim_current = sweep_data['stimulus'] * 1e12

# Get the voltage trace (in volts) and convert to mV
response_voltage = sweep_data['response'] * 1e3

# Get the sampling rate and can create a time axis for our data
sampling_rate = sweep_data['sampling_rate'] # in Hz
timestamps = (np.arange(0, len(response_voltage)) * (1.0 / sampling_rate))

plt.plot(timestamps, response_voltage)
plt.ylabel('Cell Response (mV)')
plt.xlabel('Time (sec)')
plt.title('Cell 525011903, Sweep 100 AP')

plt.show()


# Without changing the limits on the x-axis, you won't be able to see individual action potentials. To modify the x-axis using `plt.xlim([min,max])` to specify the limits (replace min and max with numbers that make sense for this x-axis)

# For more information on the helper methods that can be used on this NwbDataSet instance, please click <a href="https://allensdk.readthedocs.io/en/latest/allensdk.core.nwb_data_set.html">here</a>

# In[ ]:




