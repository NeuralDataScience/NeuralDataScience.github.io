#!/usr/bin/env python
# coding: utf-8

# # Calcium Imaging of Genetically-Identified Cells in Visual Cortex

# In[1]:


# Allen specific toolboxes
import allensdk.brain_observatory.stimulus_info as stim_info
from allensdk.core.brain_observatory_cache import BrainObservatoryCache
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt


# In[2]:


# Ensures that the Allen 
#!pip install allensdk


# In[3]:


# We will create an instance of the Brain Observatory Cache as an object, "boc."
boc = BrainObservatoryCache(manifest_file='manifest.json')


# In[4]:


# Assign previous container id and stimulus for imaging 
exp_container_id = 658854535
stim = 'natural_scenes'

# Call experiment contianer for our id and stimuli of interest
expt_cont = boc.get_ophys_experiments(experiment_container_ids = [exp_container_id],
                                      stimuli = [stim])

session_id = expt_cont[0]['id']
data = boc.get_ophys_experiment_data(session_id)


# ## Download & inspect the natural scenes imaging session
# First, we'll look at the session where the mouse viewed natural scenes.

# Let's take a quick look at the data you just acquired. We'll take a maximum projection of the data, so that we can actually see the cells. If we just looked at one snapshot of the raw imaging data, the cells would look dim. A "maximum projection image" shows us the maximum brightness for each pixel, across the entire experiment.
# 
# Below, we are using the `get_max_projection()` method on our data, and then using the `imshow()` method in order to see our projection.
# 
# **Note**: The weird text for the ylabel is called "TeX" markup, in order to get the greek symbol *mu* ($\mu$). See documentation <a href="https://matplotlib.org/tutorials/text/mathtext.html">here</a>.

# In[5]:


# Get the maximum projection (a numpy array) of our data
max_projection = data.get_max_projection()

# Create a new figure
fig = plt.figure(figsize=(6,6))

# Use imshow to visualize our numpy array
plt.imshow(max_projection, cmap='gray')

# Add labels for microns; weird syntax below is to get the micro sign
plt.ylabel(r'$\mu$m',fontsize=14)
plt.xlabel(r'$\mu$m',fontsize=14)
plt.show()


# ## Converting Calcium Imaging into Spikes 

# Now we'll plot the data of each of our cells (from the field of view above) across time. Each line shows the change in fluorescence over baseline ($\Delta$)F/F) of the individual cells. When there are sharp increases, that's when the cells are responding.
# 
# In the example below, the we will plot the first 10 cells from our data. the `get_dff_traces()` method returns the timestamps (in seconds) and deltaF/F.

# In[6]:


# Assign timestamps and deltaF/F
ts, dff = data.get_dff_traces()

# Set up a figure
fig = plt.figure(figsize=(20,10))

# Plot deltaF/F spikes over time for first 10 cells
for cell in range(10):
    plt.plot(ts, dff[cell])
    
plt.show()


# Although the plotting of our fluorescence was succesfful, the figure is too crowded to identify any relevant information. To solve this issue, we can add a line in our loop that offsets each cell by a predetermined amount. 

# In[7]:


fig = plt.figure(figsize=(20,10))

offset = 0

for cell in range(10):
    plt.plot(ts, dff[cell]+offset)
    offset+=5
plt.xlabel('Timestamp (s)')
plt.ylabel('Neurons')
plt.show()


# ## Look at the response of your cells to natural scenes
# Hmm, there are some responses above, but it's tough to see what's going on with just the raw traces. Let's instead see how these cells actually responded to different types of images. To do so, we'll need to use the `get_cell_specimens()` method on our `boc`, giving it the name of the experiment container ID to look for. The dataframe that this creates will have a lot more information about what the cells in our experiment prefer.

# In[8]:


# Get the cell specimens information for this session
cell_specimens = boc.get_cell_specimens(experiment_container_ids=[exp_container_id])
cell_specimens_df = pd.DataFrame(cell_specimens)
cell_specimens_df.head()


# Let's create a bar graph of preferred images in our dataset. The `p_ns` column contains the pvalue that corresponds to whether a cell *significantly* prefered an image more than the rest. We will subselect our `cell_specimens_df` dataframe to only contains cells that have a pvalue less than 0.05. 
# 
# The `pref_image_ns` column contians the image IDs of the stimulus being presented. We can create our histogram from this column to see how many cells responded to these statistically significant stimuli. 

# In[9]:


# Subselect dataframe to contain significantly preferred images 
sig_cells = cell_specimens_df[cell_specimens_df['p_ns'] < 0.05]

# Assign our image ids
pref_images = sig_cells['pref_image_ns']

# Set up our figure 
fig = plt.figure(figsize = [20,10])

# Plot our bar graph
pref_images.value_counts().plot(kind='bar')
plt.title('Response of cells to natural scenes')
plt.ylabel('Cell Frequency')
plt.xlabel('Image ID')
plt.show()


# In order to actually see what this stimulus are, first, we'll organize the stimulus table. This tells us which stimulus was played on each trial. This data set has 118 different scenes, and each scene is presented 50 times. Images of the scenes can be found [here](http://observatory.brain-map.org/visualcoding/stimulus/natural_scenes).

# In[10]:


natural_scene_table = data.get_stimulus_table('natural_scenes')
natural_scene_template = data.get_stimulus_template('natural_scenes')
sceneIDs = np.unique(natural_scene_table.frame)


# Choose your image id
image_id = 17

# Plot this natural scene
# Create a new figure
fig = plt.figure(figsize=(6,6))

# Use imshow to visualize our numpy array
plt.imshow(natural_scene_template[image_id,:,:])

print("Image ID: 17")
plt.show()


# ## Examine the direction selectivity of your cell
# Sometimes, the function of a cell is not particularly clear from natural stimuli. Those stimuli have a lot of information in them, and it might be hard to tell what a cell is actually responding to. Instead, we can use simple drifting gratings to look at one straightforward property of a cell: <b>does it respond to specific directions of movement?</b></br>
# 
# We can use the columns that look at the direction selectivity index (DSI) in order to determine whether our cells are direction selective (typically considered having a DSI > 0.5). Take another look at the cell_specimens_df we created above. We can subselect `sig_cells` to only contain cells that were direction specific and replot our bar graph to compare. 

# In[11]:


dsi_cells = sig_cells[sig_cells['dsi_dg'] > 0.5]

pref_images_dsi = dsi_cells['pref_image_ns']

# Set up our figure 
fig = plt.figure(figsize = [20,10])

# Plot our bar graph
pref_images_dsi.value_counts().plot(kind='bar')
plt.title('Response of cells to natural scenes (Direction Specific)')
plt.ylabel('Cell Frequency')
plt.xlabel('Image ID')
plt.show()


# As you can see our plot has drastically changed. Our cells were only direction selective to nine images from the significantly preferred data.

# In[ ]:




