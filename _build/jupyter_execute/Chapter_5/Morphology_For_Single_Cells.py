#!/usr/bin/env python
# coding: utf-8

# # Morphology for Single Cells 

# This section will serve as an introduction to the Allen Cell Types database. We'll work with the AllenSDK to see what information we can gain about our cells.
# 
# First, we'll `import` the CellTypesCache module. This module provides tools to allow us to access information from the Allen Cell Types database. We're passing it a **manifest** filename as well. CellTypesCache will store the data in the path specified by the manifest filename. You can look under cell_types in your directory, and take a look at the file.
# 
# (If you're curious, you can see the full source documentation for the core package on the <a href="https://allensdk.readthedocs.io/en/latest/allensdk.core.html">Allen Brain Atlas website</a>.)
# 
# <b>Note</b>: In order to run the line below, you need to have the AllenSDK installed. You can find information on how to do that on the Allen SDK <a href="http://alleninstitute.github.io/AllenSDK/install.html">intall guide</a>. 

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


#Import the "Cell Types Cache" from the AllenSDK core package
from allensdk.core.cell_types_cache import CellTypesCache

#Import CellTypesApi, which will allow us to query the database.
from allensdk.api.queries.cell_types_api import CellTypesApi

# Import Toolkits 
import pandas as pd
import matplotlib.pyplot as plt 
get_ipython().run_line_magic('matplotlib', 'inline')

# We'll then initialize the cache as 'ctc' (cell types cache)
ctc = CellTypesCache(manifest_file='cell_types/manifest.json')

print('Packages were successfully imported.')


# ## Get Cells

# The `get_cells()` method downloads metadata for cells in the database. The database contains human cells and mouse cells. By default, `get_cells()` downloads metata for *all* cells in the database. Alternatively, one can filter out the database to only include cells collected from a certain species.
# Look through <a href="https://allensdk.readthedocs.io/en/latest/allensdk.core.cell_types_cache.html">the documentation for the CellTypesCache</a> for more information on the `get_cells` method.

# In[3]:


# Download metadata for all cells in the database
all_cells = ctc.get_cells()
all_cells_df = pd.DataFrame(all_cells).set_index('id')
print('Length of dataframe:')
print(len(all_cells_df))
all_cells_df.head()


# As you may have noticed already, out current dataframe only contains metadeta about our cells and no information on the morphology of our cells. In order to get information about the morphology of these cells, we need to use the `get_morphology_features()` method on our instance of the cell types cache. We will set the indices to be the `specimen_id` because these ids will align with those in `all_cells_df`.

# In[4]:


# Downloads the morphology features and sets up the dataframe all in one line
morphology_df = pd.DataFrame(ctc.get_morphology_features()).set_index('specimen_id')
print('Length of dataframe:')
print(len(morphology_df))
morphology_df.head()


# Now we have two dataframes, one with the metadata for our cells, indexed by id, and another with the morphology data for all cells, also indexed by id. Usefully, these ids are unique to each cell, meaning we can match them across dataframes.

# In[5]:


# Combine our metadata with our morphology data
meta_morph_df = all_cells_df.join(morphology_df)
print('Length of dataframe:')
print(len(meta_morph_df))
meta_morph_df.head()


# **Note**: Notice that when we combine our metadata with our morphology data, we get a lot of NaN values in our morphology columns. This is becasue not all cells in our dataset will have morphology data. To only download cells that have morphology data from our database, make sure to specify `require_morphology= True,` when calling `get_cells()`.

# In[6]:


# Only download data for cells that have morphology data 
cells_with_morph = pd.DataFrame(ctc.get_cells(require_morphology = True)).set_index('id')
new_df = cells_with_morph.join(morphology_df)
print('Length of dataframe:')
print(len(new_df))
new_df.head()


# The Cell Types Database also contains 3D reconstructions of neuronal morphologies. You can create these single cell reconstructions by exectuing the `get_recontruction()` method on your instance of the cells type cache. To do so, you must specify what cell you want to recontruct by inputing a `specimen_id`. This method returns a class instance with methods for accessing morphology compartments. 

# **Note**: Not all cells will have data for a 3D resonstruction. To only download cells that have cell reconstructions, make sure to specify `require_reconstruction = True,` when calling `get_cells()`.

# In[7]:


# Select a cell
sid = 313862022

# Call for recontruction of desired cell
single_cell_morphology = ctc.get_reconstruction(specimen_id = sid)

# Get summary of cell reconstruction 
single_cell_morphology.soma


# We now have a dictionary of our cell reconstruction. Note that the type field refers to the type of neuronal compartment. The values can be 1 for the soma, 2 for the axon, 3 for dendrites, and 4 for apical dendrites (if present). The x, y, and z, represent the spatial location of the cell soma. 

# Morphologies now also come with marker files, which contains points of interest in the reconstruction. The marker file contains locations where dendrites have been truncated due to slicing and when axons were not reconstructed. The `name` field indicates the type of marker (10 for dendrite truncation, 20 for no reconstruction).

# In[8]:


# Download and store markers for 3D reconstruction 
markers = ctc.get_reconstruction_markers(sid) 
markers


# We can use this data to draw lines between each node and all its children to get a drawing of the cell. We'll reconstruct an image from the front and side view of our cell.

# In[9]:


# Import necessary toolboxes
from allensdk.core.swc import Marker

# Set up our plot
fig, axes = plt.subplots(1, 2, sharey=True, sharex=True, figsize=(10,10))
axes[0].set_aspect('equal')
axes[1].set_aspect('equal')

# Make a line drawing of x-y and y-z views
for n in single_cell_morphology.compartment_list:
    for c in single_cell_morphology.children_of(n):
        axes[0].plot([n['x'], c['x']], [n['y'], c['y']], color='black')
        axes[1].plot([n['z'], c['z']], [n['y'], c['y']], color='black')

# Cut dendrite markers
dm = [ m for m in markers if m['name'] == Marker.CUT_DENDRITE ]
axes[0].scatter([m['x'] for m in dm], [m['y'] for m in dm], color='#3333ff')
axes[1].scatter([m['z'] for m in dm], [m['y'] for m in dm], color='#3333ff')

# No reconstruction markers
nm = [ m for m in markers if m['name'] == Marker.NO_RECONSTRUCTION ]
axes[0].scatter([m['x'] for m in nm], [m['y'] for m in nm], color='#333333')
axes[1].scatter([m['z'] for m in nm], [m['y'] for m in nm], color='#333333')
axes[0].set_ylabel('y')
axes[0].set_xlabel('x')
axes[1].set_xlabel('z')
axes[0].set_title('Front View')
axes[1].set_title('Side View')

# Show the plot
plt.show()


# In[ ]:




