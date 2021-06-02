#!/usr/bin/env python
# coding: utf-8

# # Available Pre-Computed Features

# The Allen Institute also has many more precomputed features. Many of them give access to more information on the electrophysiology, morphology, and metadata on the cells available in the Allen. We will demonstrate how to plug in these features that are available in order to plot your metrics. 

# In[1]:


#Import all the necessary packages and initalize an instance of the cache
import pandas as pd
from allensdk.core.cell_types_cache import CellTypesCache
from allensdk.api.queries.cell_types_api import CellTypesApi
import matplotlib.pyplot as plt

ctc = CellTypesCache(manifest_file='cell_types/manifest.json')

print('Packages succesfully downloaded.')


# Below we have created a pandas dataframe from the electrophysiology data and metadata of our mouse cells and set the row indices to be the `id` column. 

# In[2]:


mouse_df = pd.DataFrame(ctc.get_cells(species = [CellTypesApi.MOUSE])).set_index('id')
ephys_df = pd.DataFrame(ctc.get_ephys_features()).set_index('specimen_id')
mouse_ephys_df = mouse_df.join(ephys_df)
mouse_ephys_df.head()


# The Allen has many pre-computed features that you might consider comparing across cells. Some of these features include input resistance ('input_resistance_mohm'), Adapation ratio ('adaptation'), Average ISI ('avg_isi'), and many others (you can find a complete glossary <a href = "https://docs.google.com/document/d/1YGLwkMTebwrXd_1E817LFbztMjSTCWh83Mlp3_3ZMEo/edit#heading=h.t0p3wngfkxc1"> here </a>).

# We must first select 2 or more cell types that we would like to compare. We can subset our electrophysiology dataframe to compare across transgenic lines, structure layer, and many more  columns. We created two dataframes to compare spiny dendrite types to aspiny dendrite types.

# In[3]:


# Define your cell type variables below
cell_type1 = 'spiny'
cell_type2 = 'aspiny'

# Create our dataframes from our cell types
mouse_spiny_df = mouse_ephys_df[mouse_ephys_df['dendrite_type'] == cell_type1]
mouse_aspiny_df = mouse_ephys_df[mouse_ephys_df['dendrite_type'] == cell_type2]


# Now that we have two cell types we would like to compare, we can now use the pre-computed features to plot some our cells' characteristics. Lets use a boxplot. The syntax to access these precomputed features is as follows:
# ```
# plt.boxplot([dataframe_1['pre_computed_feature'],dataframe_2['pre_computed_feature]])
# ```
# Let's start by comparing the input Resistance between our two cell types.

# In[4]:


# Select our pre computed feature that we would like to compare 
pre_computed_feature = 'input_resistance_mohm'

# Plot our figure and provide labels
plt.boxplot([mouse_spiny_df[pre_computed_feature], mouse_aspiny_df[pre_computed_feature]])
plt.ylabel('Input Resistance (mohm)')
plt.xticks([1,2], ['Spiny', 'Aspiny'])
plt.title('Input Resistance of Mouse Spiny vs Aspiny Neuron Dendrite Types')

# Show our plot 
plt.show()


# **Note**: You cannot plot missing values. Be sure to remove rows that contain missing values before plotting your features. Below is an example of how to compare cell types that contain some missing values in our pre-computed features. 

# In[5]:


# Download our Human cells data and combine with our electrophysiology data
human_df = pd.DataFrame(ctc.get_cells(species = [CellTypesApi.HUMAN])).set_index('id')
human_ephys_df = human_df.join(ephys_df)

# Select our cell types
cell_type3 = 'MTG'
cell_type4 = 'MFG'

# Compare two different brain structures 
human_MTG_df = human_ephys_df[human_ephys_df['structure_area_abbrev']== cell_type3]
human_MFG_df = human_ephys_df[human_ephys_df['structure_area_abbrev']== cell_type4]

# Select pre computed feature you would like to compare 
pre_computed_feature2 = 'avg_isi'

# Drop all null values in our column of interest in order to plot
human_MTG_df = human_MTG_df.dropna(subset =[pre_computed_feature2])
human_MFG_df = human_MFG_df.dropna(subset = [pre_computed_feature2])

print('\n Null values dropped.')


# In[6]:


# Plot our figure and provide labels 
plt.boxplot([human_MTG_df[pre_computed_feature2], human_MFG_df[pre_computed_feature2]])
plt.ylabel('Mean value of all interspike intervals in a sweep')
plt.xticks([1,2], ['MTG', 'MFG'])
plt.title('Average ISI of MTG Cells vs MFG Cells')

# Show our plot 
plt.show()


# In[7]:


print(f'Number of available pre computed features: {len(ephys_df)}')
ephys_df.head()


# In[8]:


col_1 = 'fast_trough_v_long_square'
col_2 = 'upstroke_downstroke_ratio_long_square'

fast_trough = ephys_df[col_1]
upstroke_downstroke = ephys_df[col_2]

plt.scatter(fast_trough, upstroke_downstroke)

plt.show()


# 

# In[9]:


mouse_df = pd.DataFrame(ctc.get_cells(species = [CellTypesApi.MOUSE])).set_index('id')
ephys_df = pd.DataFrame(ctc.get_ephys_features()).set_index('specimen_id')
mouse_ephys_df = mouse_df.join(ephys_df)

col_3 = 'dendrite_type'
desired_value1 = 'spiny'
desired_value2 = 'aspiny'

spiny_df = mouse_ephys_df[mouse_ephys_df[col_3]==desired_value1]
aspiny_df = mouse_ephys_df[mouse_ephys_df[col_3]==desired_value2]

plt.scatter(spiny_df[col_1], spiny_df[col_2])
plt.scatter(aspiny_df[col_1], aspiny_df[col_2])
plt.legend([desired_value1,desired_value2])

plt.show()


# In[ ]:




