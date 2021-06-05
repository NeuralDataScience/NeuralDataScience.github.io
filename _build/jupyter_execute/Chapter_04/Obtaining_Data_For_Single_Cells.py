#!/usr/bin/env python
# coding: utf-8

# # Obtaining Data for Single Cells 

# This section will serve as an introduction to the Allen Cell Types database. We'll work with the AllenSDK to see what information we can gain about our cells.
# 
# First, let's make sure you have an updated version of the Allen Institute Database installed. If you do not have the version below, this cell will install it for you. There is more information on installing the AllenSDK in the <a href="http://alleninstitute.github.io/AllenSDK/install.html">install guide</a>. 

# In[1]:


# This will ensure that the AllenSDK is installed.
# If not, it will install it for you.
try:
    import allensdk
    if allensdk.__version__ == '2.11.2':
        print('allensdk already installed.')
    else: 
        print('incompatible version of allensdk installed')
        get_ipython().system('pip install allensdk==2.11.2')
except ImportError as e:
    get_ipython().system('pip install allensdk==2.11.2')


# Next, we'll `import` the CellTypesCache module. This module provides tools to allow us to access information from the Allen Cell Types database. We're passing it a **manifest** filename as well. CellTypesCache will store the data in the path specified by the manifest filename. You can look under cell_types in your directory, and take a look at the file.
# 
# If you're curious, you can see the full source documentation for the core package on the <a href="https://allensdk.readthedocs.io/en/latest/allensdk.core.html">Allen Brain Atlas website</a>

# In[2]:


# Import the "Cell Types Cache" from the AllenSDK core package
from allensdk.core.cell_types_cache import CellTypesCache

# Import CellTypesApi, which will allow us to query the database.
from allensdk.api.queries.cell_types_api import CellTypesApi

# Import packages 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')

# We'll then initialize the cache as 'ctc' (cell types cache)
ctc = CellTypesCache(manifest_file='cell_types/manifest.json')

print('Packages were successfully imported.')


# ## Get Available Cells

# The `get_cells()` method downloads metadata for cells in the database. The database contains human cells and mouse cells. By default, `get_cells()` downloads metadata for *all* cells in the database. Alternatively, you can filter the database to only include cells collected from a certain species.
# Look through <a href="https://allensdk.readthedocs.io/en/latest/allensdk.core.cell_types_cache.html">the documentation for the CellTypesCache</a> for more information on the `get_cells` method.

# In[3]:


# Download metadata for all cells in the database
all_cells = ctc.get_cells()

# Convert it to a dataframe with the cell id as the index
all_cells_df = pd.DataFrame(all_cells).set_index('id')

print('Number of cells:',len(all_cells_df))
all_cells_df.head()


# The Allen Institute for Brain Science uses transgenic mouse lines that have Cre-expressing cells to mark specific types of cells in the brain. Lets find out what cre-lines are availabe in our mouse data under the column `transgenic_line`. 
# 
# We can take a look at how many different values are stored within a column using the `.unique()` method.

# In[4]:


all_cells_df['transgenic_line'].unique()


# For more information on the Allen Cell Types Cre lines, please visit <a href="https://docs.google.com/document/d/1ZMMZgc7cS5BHhoWNqzjw95BdxOuj5wrYl9I7PV2HeUI/edit">the Allen Cell Types Cre Lines Glossary</a> for a short description of the cortical expression patterns of the transgenic Cre lines available in the Allen Cell Types dataset.

# ## Get Morphology data
# 
# The dataframe above only contains metadeta about our cells and no information on the morphology or electrophysiology of our cells. In order to get information about the morphology of these cells, we need to use the `get_morphology_features()` method on our instance of the cell types cache. We will set the indices to be the `specimen_id` because these ids will align with those in `all_cells_df`.

# In[5]:


# Downloads the morphology features and sets up the dataframe all in one line
morphology_df = pd.DataFrame(ctc.get_morphology_features()).set_index('specimen_id')
print('Length of dataframe:',len(morphology_df))
morphology_df.head()


# Now we have two dataframes, one with the metadata for our cells, indexed by id, and another with the morphology data for all cells, also indexed by id. Usefully, these ids are unique to each cell, meaning we can match them across dataframes.
# 
# We'll use [join](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.join.html) to unite our dataframes. Since for the moment we're only interested in cells that have morphology data, we'll **join** the dataframes "on the right," effectively dropping all of the cells that are not in the morphology dataframe.
# 
# **Note**: Above, in get the `get_cells()` method, you can also restrict to experiments with morphology data by usnig the `require_morphology = True` argument.

# In[6]:


# Combine our metadata with our morphology data
meta_morph_df = all_cells_df.join(morphology_df,how='right')
print('Number of cells:',len(meta_morph_df))
meta_morph_df.head()


# The Cell Types Database also contains 3D reconstructions of neuronal morphologies. You can create these single cell reconstructions by executing the `get_reconstruction()` method on your instance of the cells type cache. To do so, you must specify what cell you want to reconstruct by inputing a `specimen_id`. This method returns a class instance with methods for accessing morphology compartments. 

# In[7]:


# Get the cell_id for the first cell in our dataframe
cell_id = meta_morph_df.index[0]

# Call for recontruction of desired cell
single_cell_morphology = ctc.get_reconstruction(specimen_id = cell_id)

# Get summary of cell reconstruction 
single_cell_morphology.soma


# We now have a dictionary of our cell reconstruction. Note that the type field refers to the type of neuronal compartment. The values can be 1 for the soma, 2 for the axon, 3 for dendrites, and 4 for apical dendrites (if present). The x, y, and z, represent the spatial location of the cell soma.
# 
# Morphologies also come with marker files, which contain points of interest in the reconstruction. The marker file contains locations where dendrites have been truncated due to slicing and when axons were not reconstructed. The `name` field indicates the type of marker (10 for dendrite truncation, 20 for no reconstruction).

# In[8]:


# Download and store markers for 3D reconstruction 
markers = ctc.get_reconstruction_markers(cell_id) 
markers


# We can use this data to draw lines between each node and all its children to get a drawing of the cell. We'll reconstruct an image from the front and side view of our cell.
# 
# **Note**: Since we're reconstructing what is likely to be a very complicated neuron, this might take a minute to plot.

# In[9]:


# Import necessary toolboxes
from allensdk.core.swc import Marker

# Set up our plot
fig, ax = plt.subplots(1, 2, sharey=True, sharex=True, figsize=(10,10))
ax[0].set_aspect('equal')
ax[1].set_aspect('equal')

# Make a line drawing of x-y and y-z views
for n in single_cell_morphology.compartment_list:
    for c in single_cell_morphology.children_of(n):
        ax[0].plot([n['x'], c['x']], [n['y'], c['y']], color='black')
        ax[1].plot([n['z'], c['z']], [n['y'], c['y']], color='black')

# Plot cut dendrite markers in red
dm = [ m for m in markers if m['name'] == Marker.CUT_DENDRITE ]
ax[0].scatter([m['x'] for m in dm], [m['y'] for m in dm], color='red')
ax[1].scatter([m['z'] for m in dm], [m['y'] for m in dm], color='red')

# Plot no reconstruction markers in blue
nm = [ m for m in markers if m['name'] == Marker.NO_RECONSTRUCTION ]
ax[0].scatter([m['x'] for m in nm], [m['y'] for m in nm], color='blue')
ax[1].scatter([m['z'] for m in nm], [m['y'] for m in nm], color='blue')
ax[0].set_ylabel('y')
ax[0].set_xlabel('x')
ax[1].set_xlabel('z')
ax[0].set_title('Front View')
ax[1].set_title('Side View')

# Show the plot
plt.show()


# ## Get Electrophysiology Data
# 
# Now that we know what our cell looks like, let's take a look at its action potentials. The `get_ephys_data()` method can download electrophysiology traces for a single cell in the database. This method returns a class instance with helper methods for retrieving stimulus and response traces out of an NWB file. If we take a look at `specimen_ephys_data` we can see that it is an NWBDataSet object.  In order to use `get_ephys_data()`, you must specify the id of the cell specimen whose electrophysiology you would like to download.
# 
# Below we go over methods that can be used to access the electrophysiology data for single cells, the source documentation for all the methods we cover can be found on the <a href = 'https://allensdk.readthedocs.io/en/latest/allensdk.core.nwb_data_set.html'> Allen Brain Atlas website</a>. The `get_experiment_sweep_numbers()` method returns all of the sweep numbers for experiments in the file. Each sweep contains metadata and electrophysiology data.

# In[10]:


# Get electrophysiological traces of our cell
specimen_ephys_data = ctc.get_ephys_data(specimen_id = cell_id)

# Retrieve sweep numbers for cell
sweep_numbers = specimen_ephys_data.get_experiment_sweep_numbers()

print(type(specimen_ephys_data))
print(sweep_numbers)


# Now that we have sweep numbers to choose from, we can take a look at a sweep's metadata by calling get_sweep_metadata(). This returns a dictionary containing information such as stimulus paramaters and recording quality.

# In[11]:


# Select a sweep number 
sweep_number = sweep_numbers[-1]

# Retrieve metadata for selected sweep
specimen_metadata = specimen_ephys_data.get_sweep_metadata(sweep_number)
print(specimen_metadata)


# The `get_sweep()` method returns a dictionary containing the stimulus, response, index_range, and sampling rate for a particular sweep.

# In[12]:


sweep_data = specimen_ephys_data.get_sweep(sweep_number)
print(sweep_data)


# Now that you've pulled down some data, chosen a cell, and chosen a sweep number, let's plot that data. We can look closer at the action potential by plotting the raw recording. Our `sweep_data` variable has all the data we need to plot our sweep; the stimulus current injected into our cell, the cell's response, and sampling rate of the sweep. 

# In[13]:


# Get the stimulus trace (in amps) and convert to pA
stim_current = sweep_data['stimulus'] * 1e12

# Get the voltage trace (in volts) and convert to mV
response_voltage = sweep_data['response'] * 1e3

# Get the sampling rate and can create a time axis for our data
sampling_rate = sweep_data['sampling_rate'] # in Hz
timestamps = (np.arange(0, len(response_voltage)) * (1.0 / sampling_rate))

fig, ax = plt.subplots(2, 1, sharex=True, figsize=(9,9))

ax[0].set_title('Cell: '+str(cell_id)+', Sweep: '+str(sweep_number))
ax[0].plot(timestamps, response_voltage)
ax[0].set_ylabel('Cell Response (mV)')
ax[1].plot(timestamps, stim_current)
ax[1].set_xlabel('Time (sec)')
ax[1].set_ylabel('Input Current (nA)')
ax[1].set_xlim([2,2.2])

plt.show()


# That's how you can dig into the morphology and raw electrophysiology traces for single cells. In the next notebook, we'll take a look at some of the features of these action potentials.

# In[ ]:




