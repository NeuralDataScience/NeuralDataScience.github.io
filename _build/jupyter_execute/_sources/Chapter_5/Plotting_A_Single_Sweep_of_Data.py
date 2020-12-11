#!/usr/bin/env python
# coding: utf-8

# # Plotting a Signle Sweep of Data

# In this section we will go over how to access electrophysiology data from our cells. Once downloaded, we will be able to plot our cells' electrophysiology features to compare characteristics across specimen. We will also learn how to download electrophysiology traces of single cells and plot single sweeps of these cells. 

# In[1]:


#Import the "Cell Types Cache" from the AllenSDK core package
from allensdk.core.cell_types_cache import CellTypesCache

#Import CellTypesApi, which will allow us to query the database.
from allensdk.api.queries.cell_types_api import CellTypesApi

# Import Toolkits 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
get_ipython().run_line_magic('matplotlib', 'inline')

# We'll then initialize the cache as 'ctc' (cell types cache)
ctc = CellTypesCache(manifest_file='cell_types/manifest.json')

print('Packages were successfully imported.')


# We will start by downloading the metadata for our cells once again. If you are still having trouble with `get_cells()` look through <a href="https://allensdk.readthedocs.io/en/latest/allensdk.core.cell_types_cache.html">the documentation for the CellTypesCache</a> for more information.

# In[2]:


# Redownload the metadata for all our cells
all_cells = ctc.get_cells()
all_cells_df = pd.DataFrame(all_cells).set_index('id')
all_cells_df.head(3)


# At this point, you might have realized that this dataframe doesn't contain any data about the electrophysiology of our cells either. In order to get information about the electrophysiological properties of these cells, we need to use the `get_ephys_features()` method on our instance of the cell types cache.

# Just as we did before with morphology, we will will assign the output of `get_ephys_features()` to a variable and store it as a pandas dataframe.

# In[3]:


# Download our electrophysiology data 
ephys_features = pd.DataFrame(ctc.get_ephys_features()).set_index('specimen_id')
ephys_features.head()


# Again, we can combine our dataframe that contians the metadata of our cells with our electrophysiology dataframe to create one single dataframe.

# In[4]:


# Combine our metadata with our electrophysiology data 
all_ephys_features = all_cells_df.join(ephys_features)
all_ephys_features.head()


# The `get_ephys_data()` method can download electrophysiology traces for a single cell in the database. This method returns a class instance with helper methods for retrieving stimulus and response traces out of an NWB file. In order to use this method, you must specify the id of the cell specimen whose electrophysiology you would like to download.

# The `get_experiment_sweep_numbers()` method downloads all of the sweep numbers for experiments in the file. Each sweep contains metadata and electrophysiology data.

# In[6]:


# Select cell id 
cell_id_2 = 525011903

# Get electrophysiological traces of our cell
specimen_ephys_data = ctc.get_ephys_data(specimen_id = cell_id_2)

# Retrieve sweep numbers for cell
sweep_numbers = specimen_ephys_data.get_experiment_sweep_numbers()
print(sweep_numbers[0:10])


# Now that we have sweep numbers to choose from, we can take a look at a sweep's metadata by calling `get_sweep_metadata()`. This return a dictionary contianing information such as stimulus paramaters and recording quality. 

# In[8]:


# Select a sweep number 
sweep_number = 100

# Retrieve metadata for selected sweep
specimen_metadata = specimen_ephys_data.get_sweep_metadata(sweep_number)
print(specimen_metadata)


# The `get_sweep()` downloads the stimulus, response, index_range, and sampling rate for a particular sweep.

# In[12]:


sweep_data = specimen_ephys_data.get_sweep(sweep_number)
print(sweep_data)


# Now that you've pulled down some data, chosen a cell, and chosen a sweep number, let's plot that data. We can look closer at the action potential by plotting the raw recording. 

# In[10]:


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
