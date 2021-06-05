#!/usr/bin/env python
# coding: utf-8

# # Analyzing Two Photon Data
# 
# On the previous page, we introduced how to retrieve specific experiments from the Allen Institute SDK's Brain Observatory. Here we'll introduce how researchers analyze this data, from processing single cell activity to understanding tuning curves. 
# 
# ## Setup
# We need a variety of standard Python packages in addition to two different `allensdk` toolboxes. If you have not yet installed the `allensdk`, run the cell below. Otherwise, you can skip to the cell that imports our toolboxes.

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


# Import toolboxes
from allensdk.core.brain_observatory_cache import BrainObservatoryCache
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

print('Packages imported.')


# ## Download & inspect the natural scenes imaging session
# First, we'll look at an experiment where the mouse viewed natural scenes. Below, we'll assign an experiment container ID (the same one we worked with in the previous section), designate that we're interested in only the natural scenes experiments, and download the data for the first experiment in the container.
# 
# **Note**: The cell below downloads some data, and make take a minute or so to run. It is important that you do not interrupt the download of the data or else the file will become corrupted and you will have to delete it and try again. 

# In[3]:


# Create an instance of the Brain Observatory cache
boc = BrainObservatoryCache(manifest_file='manifest.json')

# Assign container ID from previous section
exp_container_id = 627823571
stim = ['natural_scenes']

# Get experiments for our container id and stimuli of interest
experiments = boc.get_ophys_experiments(experiment_container_ids = [exp_container_id],
                                     stimuli = stim)

# Assign the experiment id 
experiment_id = experiments[0]['id']
experiment_data = boc.get_ophys_experiment_data(experiment_id)

print('Data acquired.')


# Let's take a quick look at the data you just downloaded. We'll create a **maximum projection image** of the data, so that we can see the cells in our field of view. If we just looked at one snapshot of the raw imaging data, the cells would look dim -- they only become bright when they're actively firing. A maximum projection image shows us the maximum brightness for each pixel, across the entire experiment. Please visit the <a href = 'https://alleninstitute.github.io/AllenSDK/allensdk.core.brain_observatory_nwb_data_set.html'> Brain Observatory NWB Data Set documentation </a> for the original documentation to the methods used in the fluorescence imaging and natural scenes section. 
# 
# Below, we are using the `get_max_projection()` method on our data, and then using the `imshow()` method in order to see our projection.
# 
# **Note**: The weird text for the ylabel is called "TeX" markup, in order to get the greek symbol *mu* ($\mu$). See documentation on the <a href="https://matplotlib.org/tutorials/text/mathtext.html">matplotlib website</a>.

# In[4]:


# Get the maximum projection (a numpy array) of our data
max_projection = experiment_data.get_max_projection()

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
# In the example below, we will plot the first 10 cells from our data. the `get_dff_traces()` method returns the timestamps (in seconds) and deltaF/F.
# 
# Below, we've also added a line in our loop that offsets each cell by a predetermined amount so that we can see individual calcium traces. Each line is a different neuron, and the small blips in the data are calcium-mediated changes in fluorescence.

# In[5]:


# Assign timestamps and deltaF/F
ts, dff = experiment_data.get_dff_traces()

# Set up a figure
fig = plt.figure(figsize=(18,6))

# Loop through to add an offset on the y-axis
offset = 0
for cell in range(2,12):
    plt.plot(ts, dff[cell]+offset)
    offset+=5
    
plt.xlabel('Timestamp (s)')
plt.ylabel('Neurons ($\Delta$F\F)')
plt.yticks([])
plt.xlim([2700,2720])
plt.show()


# ## Look at the response of your cells to natural scenes
# There are clearly some responses above, but it's tough to see whether this corresponds to different behaviors or visual stimuli with just the raw fluorescence traces.
# 
# Let's see how these cells actually responded to different types of images. To do so, we'll need to use the `get_cell_specimens()` method on our `boc`, giving it the name of the experiment container ID.
# 
# The dataframe that this creates will have a lot more information about what the cells in our experiment prefer. Each row is a different cell, each with its own preferences and response patterns.

# In[6]:


# Get the cell specimens information for this experiment
cell_specimens = boc.get_cell_specimens(experiment_container_ids=[exp_container_id])
cell_specimens_df = pd.DataFrame(cell_specimens)
cell_specimens_df.head()


# Let's create a bar graph of preferred images in our dataset. The `p_ns` column contains the pvalue that corresponds to whether a cell *significantly* prefered an image more than the rest. We will use this column to subset our `cell_specimens_df` dataframe to only contains cells that have a p value less than 0.05. 
# 
# The `pref_image_ns` column contains the image IDs of the stimulus being presented. We can create our bar graph from this column to see how many cells responded to these statistically significant images.

# In[7]:


# Subset dataframe to contain significantly preferred images 
col_1 = 'p_ns'
sig_cells = cell_specimens_df[cell_specimens_df[col_1] < 0.05]

# Assign our image ids for significantly preferred images
col_2 = 'pref_image_ns'
pref_images = sig_cells[col_2]

# Set up our figure 
fig = plt.figure(figsize = (18,6))

# Plot our bar graph
pref_counts = pref_images.value_counts()
pref_counts.plot(kind='bar')
plt.title('Response of cells to natural scenes')
plt.ylabel('Number of cells')
plt.xlabel('Image ID')
plt.show()


# In order to actually see what these images are, first, we'll organize the stimulus table. This tells us which stimulus was played on each trial. This data set has 118 different scenes, and each scene is presented 50 times. Images of the scenes can be found [here](http://observatory.brain-map.org/visualcoding/stimulus/natural_scenes).
# 
# Below, we'll show the top five images for cells in this field of view. Do they have anything in common, either visually or conceptually?
# 
# *Note*: Not every experiment contains the data for the natural scenes experiment. If you change the experiment ID above and try the next cell, you may receive an error. You can use `data.list_stimuli()` to see all of the stimuli available within your experiment.

# In[8]:


# Get the natural scene information
natural_scene_table = experiment_data.get_stimulus_table('natural_scenes')
natural_scene_template = experiment_data.get_stimulus_template('natural_scenes')
sceneIDs = np.unique(natural_scene_table.frame)

# Set up our figure
fig,ax = plt.subplots(1,5,figsize=(15,6))

for image_ID in range(5): # Show the first 5 images
    
    image_id = int(pref_counts.index[image_ID]) # Get the image ID

    # Use imshow to visualize our numpy array
    ax[image_ID].imshow(natural_scene_template[image_id,:,:],cmap='gray')
    ax[image_ID].set_xticks([])
    ax[image_ID].set_yticks([])
    ax[image_ID].set_title('Image ' + str(image_id))
    
plt.show()


# ## Examine the direction selectivity of your cell
# Sometimes, the function of a cell is not particularly clear from natural stimuli. Those stimuli have a lot of information in them, and it might be hard to tell what a cell is actually responding to. Instead, we can use simple drifting gratings to look at one straightforward property of a cell: <b>does it respond to specific directions of movement?</b></br> To do so, we'll examine the **drifting gratings** experiments.
# 
# We will now show how to plot a heatmap of a cell's response organized by orientation and temporal frequency. We will be using one of the three cells from the dataframe above which showed direction selectivity from the significantly preferred images. Please visit the <a href = 'https://allensdk.readthedocs.io/en/latest/allensdk.brain_observatory.drifting_gratings.html'> Drifting Gratings module documentation </a> for additional help on the methods used in the drifting gratings section. 
# 
# Below, we'll use the same experiment container but a different stimulus to create a separate experiment dataset, `dg_experiment`.

# In[9]:


# Get experiment for our container id and stimuli of interest
stim_2 = ['drifting_gratings']
dg_experiment = boc.get_ophys_experiments(
                        experiment_container_ids = [exp_container_id],
                        stimuli = stim_2)

# Download the experiment data using the experiment id
experiment_id_2 = dg_experiment[0]['id']
data_dg = boc.get_ophys_experiment_data(experiment_id_2)

print('Data acquired.')


# Our first step is to create an instance of our DriftingGratings object. The DriftingGratings class requires an NWB data set as an input (i.e. `data_dg`). 
# 
# The `peak` property of the DriftingGratings object returns a Pandas DataFrame of peak conditions (direction and temporal frequency) as well as computed response metrics. Some key columns is this dataframe are the preferred orientation, `ori_dg`, and preferred frequency, `tf_dg`, of the cell. Other computed metrics include:
# 
# - reliability_dg
# - osi_dg (orientation selectivity index)
# - dsi_dg (direction selectivity index)
# - peak_dff_dg (peak dF/F)
# - ptest_dg (number of signficant cells)
# - p_run_dg (K-S statistic comparing running trials to stationary trials) 
# - run_modulation_dg
# - cv_dg (circular variance)

# In[10]:


from allensdk.brain_observatory.drifting_gratings import DriftingGratings

# Create my DriftingGratings Object 
dg = DriftingGratings(data_dg)

# Return dataframe of peak conditions
dg_df = dg.peak
dg_df.head()


# Next, we'll select a cell from our table by `cell_specimen_id`.
# 
# If there is a specific cell you want to analyze, you can use the `get_cell_specimen_indices()` method to locate the index of your cell of interest. The index of your cell is needed becasue you will need to index into the NumPy arrary returned by the `response` attribute to contruct your heatmap.
# 
# Below, we'll simply grab the first `cell_specimen_id` in our table.

# In[11]:


# Select specimen ID from first row
specimen_id = dg_df['cell_specimen_id'][0]
cell_loc = data_dg.get_cell_specimen_indices([specimen_id])[0]

print('Specimen ID:', specimen_id)
print('Cell loc:', cell_loc)


# The `response` attribute returns a 4-D NumPy array with the mean responses to each stimulus condition. The 1st column in the returned NumPy array contains mean responses to the orientations, the 2nd column contains mean responses to the temporal frequencies, the 3rd column contains the number of the cell, and the 4th column contains the response mean to column 1, the response standard error of the mean of column 2, and the number of signficant trials.
# 
# 
# Below, we'll use `plt.imshow()` to plot the mean responses across orientation and frequency, skipping the blank sweep column (0).

# In[17]:


# Plot our data, skiping the blank sweep column (0) of the temporal frequency dimension
plt.imshow(dg.response[:,1:,cell_loc,0], cmap='hot', interpolation='none')
plt.title('Heat Map, Cell Specimen: ' + str(specimen_id))
plt.xticks(range(5), dg.tfvals[1:])
plt.yticks(range(8), dg.orivals)
plt.xlabel("Temporal frequency (Hz)", fontsize=20)
plt.ylabel("Direction (deg)", fontsize=20)
plt.tick_params(labelsize=14)
cbar= plt.colorbar()
cbar.set_label("$\Delta$F/F (%)")
plt.show()


# The preferred directions temporal frequency are stored within `ori_dg` and `tf_dg` in are table above and can be indexed through `dg.orivals` and `tf.tfvals` respectively. 
# 
# For more explanation on the available pre-computed metrics, please see <a href = 'https://alleninstitute.github.io/AllenSDK/_static/examples/nb/brain_observatory_analysis.html#Drifting-Gratings'> here</a>. 

# In[13]:


pref_ori = dg.orivals[dg.peak.ori_dg[cell_loc]]
pref_tf = dg.tfvals[dg.peak.tf_dg[cell_loc]]
print("Preferred direction:", pref_ori)
print("Preferred temporal frequency:", pref_tf)


# It is important to not that these are no the only possible analyses that can be done. We could go a step further and also look at the static gratings. We could plot the running speed of the mouse versus the DF/F of our cells to determine what stimlus elicited the fasted response from our mice. We can even use the data to determine the on and off receptive fields all our cells. In the analyses that we performed above we only looked at one experiment container that included one brain area and one cre line, but we are not limited to this and can compare brain areas and cre lines and can begin forming connections between differnt brain regions. 
# 
# In conclusion, there are many different analyses that you can perform with the two photon imaging data. It is important to look through the downloaded data to ensure your desired brain regions, cre lines, and computed metrics are all availabed before beginning your work. 

# In[ ]:




