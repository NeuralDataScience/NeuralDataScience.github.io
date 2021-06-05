#!/usr/bin/env python
# coding: utf-8

# # Analyzing Computed Features

# In addition to the raw electrophysiology and morphology data, the Allen Institute also has computed many electrophysiological features about the cells in their data. These features describe the intrinsic electrophysiological properties of the cell. Here, we will demonstrate how to access and analyze these features both across and within cells.

# In[1]:


#Import all the necessary packages and initalize an instance of the cache
import pandas as pd
from allensdk.core.cell_types_cache import CellTypesCache
from allensdk.api.queries.cell_types_api import CellTypesApi
import matplotlib.pyplot as plt

ctc = CellTypesCache(manifest_file='cell_types/manifest.json')

print('Packages successfully downloaded.')


# Below we'll create pandas dataframes for the electrophysiology data as well as metadata for all of the mouse cells in this dataset. Like the previous notebook, we'll [join](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.join.html) these dataframes and set the row indices to be the `id` column. Unlike the previous notebook, here we'll specify within `get_cells()` that we'd only like to use mouse cells. You can change the argument to `species = [CellTypesApi.HUMAN]` if you'd like to see human cells instead.

# In[2]:


mouse_df = pd.DataFrame(ctc.get_cells(species = [CellTypesApi.MOUSE])).set_index('id')
ephys_df = pd.DataFrame(ctc.get_ephys_features()).set_index('specimen_id')
mouse_ephys_df = mouse_df.join(ephys_df)
mouse_ephys_df.head()


# As you can see if you scroll to the right in the dataframe above, there are many **pre-computed features** available in this dataset. [Here's a glossary](https://docs.google.com/document/d/1YGLwkMTebwrXd_1E817LFbztMjSTCWh83Mlp3_3ZMEo/edit?usp=sharing), in case you're curious.
# 
# ![](https://github.com/ajuavinett/CellTypesLesson/blob/master/docs/ap_features.png?raw=true)
# Image from the <a href="http://help.brain-map.org/download/attachments/8323525/CellTypes_Ephys_Overview.pdf">Allen Institute Cell Types Database Technical Whitepaper.</a>
# <br><br>

# ## Compare Features Across Cells
# 
# The Allen has many precomputed features that you might consider comparing across cells. Some of these features include input resistance ('input_resistance_mohm'), Adaptation ratio ('adaptation'), Average interspike interval ('avg_isi'), and many others. We've compiled [a complete glossary](https://docs.google.com/document/d/1YGLwkMTebwrXd_1E817LFbztMjSTCWh83Mlp3_3ZMEo/edit#heading=h.t0p3wngfkxc1) for you.
# 
# To compare cell types, we can subset our electrophysiology dataframe for a specific transgenic line, structure layer, brain area, and more. Below, we'll create two dataframes to compare cells with spiny dendrites to those with aspiny dendrites. While most excitatory cells are spiny, most inhibitory cells are aspiny.

# In[3]:


# Define your cell type variables below
cell_type1 = 'spiny'
cell_type2 = 'aspiny'

# Create our dataframes from our cell types
mouse_spiny_df = mouse_ephys_df[mouse_ephys_df['dendrite_type'] == cell_type1]
mouse_aspiny_df = mouse_ephys_df[mouse_ephys_df['dendrite_type'] == cell_type2]


# Now that we have two cell types we would like to compare, we can now use the precomputed features to plot some our cells' characteristics. Let's start by using a boxplot to compare the input resistance between our two cell types.

# In[4]:


# Select our pre computed feature that we would like to compare 
feature = 'input_resistance_mohm'

# Get the pandas series for our feature from each dataframe. Drop any NaN values.
clean_spiny = mouse_spiny_df[feature].dropna()
clean_aspiny = mouse_aspiny_df[feature].dropna()

# Plot our figure and provide labels
plt.boxplot([clean_spiny, clean_aspiny])
plt.ylabel('Input Resistance (MOhm)')
plt.xticks([1,2], [cell_type1, cell_type2])
plt.title(feature + ' in ' + cell_type1 + ' and ' + cell_type2 + ' cells')

# Show our plot 
plt.show()


# ## Compare Features Within Cells
# 
# The power in this dataset is not only the ability to compare two cell types, but to look across all of the data for trends that emerge. Even if we dig into the weeds of the action potential shape, we can make some interesting observations.
# 
# Let's look at the speed of the trough, and the ratio between the upstroke and downstroke of the action potential:
# - **Action potential fast trough** (<code>fast_trough_v_long_square</code>): Minimum value of the membrane potential in the interval lasting 5 ms after the peak.
# - **Upstroke/downstroke ratio** (<code>upstroke_downstroke_ratio_long_square</code>)</b>: The ratio between the absolute values of the action potential peak upstroke and the action potential peak downstroke.</div>

# The cell below will dig up the dendrite type of these cells and add that to our dataframe. Then, it'll create a scatterplot to compare the depth of the trough with the upstroke:downstroke ratio, where each dot is colored by dendrite type.

# In[5]:


# Create our plot! Calling scatter twice like this will draw both of these on the same plot.
plt.scatter(mouse_spiny_df['fast_trough_v_long_square'],mouse_spiny_df['upstroke_downstroke_ratio_long_square'])
plt.scatter(mouse_aspiny_df['fast_trough_v_long_square'],mouse_aspiny_df['upstroke_downstroke_ratio_long_square'])

plt.ylabel('upstroke-downstroke ratio')
plt.xlabel('fast trough depth (mV)')
plt.legend(['Spiny','Aspiny'])
    
plt.show()


# This is the true power of neural data science! It looks like the two clusters in the data partially relate to the dendritic type. Cells with spiny dendrites (which are typically excitatory cells) have a big ratio of upstroke:downstroke, and a more shallow trough (less negative). Cells with aspiny dendrites (typically inhibitory cells) are a little bit more varied. But </i>only</i> aspiny cells have a low upstroke:downstroke ratio and a deeper trough (more negative).
