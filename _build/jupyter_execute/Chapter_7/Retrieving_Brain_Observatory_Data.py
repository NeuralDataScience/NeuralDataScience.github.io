#!/usr/bin/env python
# coding: utf-8

# # Two-photon Calcium Imaging Data

# This section will serve as an introdution to retrieving two-photon calcium imaging data from the Allen Brain Observatory. By the end of this section you will know how to obtain a two-photon imaging dataset for a particular cell type in a specific visual area.
# 
# ## Setup
# We need a variety of standard Python packages in addition to two different `allensdk` toolboxes. If you have not yet installed the `allensdk`, run the cell below. Otherwise, you can skip to the cell that imports our toolboxes.

# In[1]:


# This will ensure that the AllenSDK is installed.
# If not, it will install it for you.
try:
    import allensdk
    print('allensdk already installed.')
except ImportError as e:
    get_ipython().system('pip install allensdk')


# In[2]:


# Import our toolboxes
import allensdk.brain_observatory.stimulus_info as stim_info
from allensdk.core.brain_observatory_cache import BrainObservatoryCache
import pandas as pd 
import matplotlib.pyplot as plt
print('Packages installed.')


# ## Get a list of all possible transgenic mouse lines and brain areas, and choose which to work with.

# Below, we'll create an instance of the [`BrainObservatoryCache`](https://alleninstitute.github.io/AllenSDK/allensdk.core.brain_observatory_cache.html). This object will allow us to retrieve and analyze the Allen Brain Observatory data.

# In[3]:


# We will create an instance of the Brain Observatory Cache as an object, "boc."
boc = BrainObservatoryCache(manifest_file='manifest.json')


# Next, we'll use `get_all_cre_lines()` on our `boc` object to return all of the possible Cre lines and brain areas are that we can analyze. We can also use the `get_all_targeted_structures()` method to return all brain areas in our dataset. 
# 
# You can find more info about the Cre-lines <a href="http://observatory.brain-map.org/visualcoding/transgenic">here</a>. Refer back to the <a href="http://observatory.brain-map.org/visualcoding">Brain Observatory landing page</a> to learn more about the different visual areas.

# In[4]:


# We'll assign the list of cre lines to a variable, 'cre-lines'.
cre_lines = boc.get_all_cre_lines()
print("all cre lines: " + str(cre_lines) + '\n')

# We'll assign the list of possible structures to a variable, 'brain_areas'.
brain_areas = boc.get_all_targeted_structures()
print("all brain regions: " + str(brain_areas))


# ## Extract an experiment session

# With access to the cre lines and brain regions from the dataset, we can construct a dataframe of experiements from our desired cre lines and brain regions. We can use the `get_experiment_containers()` method of our `boc` object to get a list of experiments that are available. The method takes in the arguments `cre_lines` and `targeted_structures` which both require lists as inputs. 
# 
# *Note*: Not every cre line and brain region combination will have data. If no data is availabe for a certain combindation, an empty dataframe will be created. You can use the `empty` attribute on your new datafram to check if it is empty. 

# In[5]:


# Assign visual area and cre line of interest for analysis 
visual_area = 'VISp'
cre_line = 'Tlx3-Cre_PL56'

# Get experiment contianers for visual area and cre line of interest 
exps = boc.get_experiment_containers(targeted_structures = [visual_area], 
                                     cre_lines = [cre_line])

# Create an experiment dataframe 
exps_df = pd.DataFrame(exps)

# Check if dataframe is empty 
if exps_df.empty:
    print('Data frame is empty, choose another cre line & visual area combination.')

# Assign the ID column as the index and return dataframe
exps_df = exps_df.set_index('id')
exps_df.head()


# Let's look into one of these experiment containers, most of which have three different sessions for different types of visual stimuli. We can call `get_ophys_experiments()` on our `boc` object to return the container. This method takes in the arguments `experiment_container_ids` and `stimuli` which both require lists. We can select an id from our dataframe and choose a stimuli. In our case, we'll look for the `natural_scenes` experiment. 

# In[6]:


# Assign experiment ontainer id and stimuli 
exp_container_id = 617381603
stim = 'natural_scenes'

# Call experiment container for our id and stimuli of interest
expt_cont = boc.get_ophys_experiments(experiment_container_ids = [exp_container_id],
                                   stimuli = [stim])

# Print out our container 
print(expt_cont)


# Now, let's get the id for this experiment and extract the data using the `get_ophys_experiment_data` method. If you look closley above, you can see that our experiment container is a list that contains a dictionary. We will need to input the session id of our experiment container into this method. 

# In[7]:


# Go into first entry in list, which is the dictionary 
# Then go within id of dictionary
session_id = expt_cont[0]['id']
data = boc.get_ophys_experiment_data(session_id)

# Take a look at the kind of object data is 
print(data)


# That's how you retrieve an experiment from the Allen Brain Observatory! If you want to retrieve multiple experiments across multiple brain areas or cell types, you can use the `get_experiment_containers` method without specifying a targeted structure or brain area, and then subset your dataframe.
# 
# In the next notebook, we'll discuss how to extract the raw data from these experiment containers.
