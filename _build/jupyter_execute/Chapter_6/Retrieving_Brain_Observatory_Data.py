#!/usr/bin/env python
# coding: utf-8

# # Retrieving Calcium Imaging Data

# This section will serve as an introdution to retrieving two-photon fluorescence imaging data from the Allen Brain Observatory. By the end of this section you will know how to obtain a two-photon imaging dataset for a particular cell type in a specific visual area.
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
# You can find more info about the Cre-lines on the Allen Brain Atlas <a href="http://observatory.brain-map.org/visualcoding/transgenic"> Transgenic Mouse Lines page</a>. Refer back to the <a href="http://observatory.brain-map.org/visualcoding">Brain Observatory landing page</a> to learn more about the different visual areas. Make sure to visit the <a href = 'https://alleninstitute.github.io/AllenSDK/allensdk.core.brain_observatory_cache.html'>BrainObservatoryCache doucumentation </a> for additional help with the methods used in this notebook. 

# In[4]:


# We'll assign the list of cre lines to a variable, 'cre-lines'.
cre_lines = boc.get_all_cre_lines()
print(f"all cre lines: {cre_lines} \n")

# We'll assign the list of possible structures to a variable, 'brain_areas'.
brain_areas = boc.get_all_targeted_structures()
print("all brain regions: " + str(brain_areas))


# ## Extract an experiment session

# With access to the cre lines and brain regions from the dataset, we can construct a dataframe of experiement containers from our desired cre lines and brain regions. Each experiment container has a group of experiments that share the same targeted brain area, cre line, and depth. However, the stimuli conditions may differ across experiments for a given contianer. 
# 
# We can use the `get_experiment_containers()` method of our `boc` object to return a list of dictionaries with data on the available experiment contianers. The method takes in the arguments `cre_lines` and `targeted_structures` which both require lists as inputs. 
# 
# *Note*: Not every cre line and brain region combination will have data. If no data is availabe for a certain combindation, an empty dataframe will be created. You can use the `empty` attribute on your new datafram to check if it is empty. 

# In[5]:


# Assign visual area and cre line of interest for analysis 
visual_area = 'VISp'
cre_line = 'Tlx3-Cre_PL56'

# Get experiment contianers for visual area and cre line of interest 
exp_cont = boc.get_experiment_containers(targeted_structures = [visual_area], 
                                     cre_lines = [cre_line])

# Create an experiment dataframe 
exp_cont_df = pd.DataFrame(exp_cont)

# Check if dataframe is empty 
if exp_cont_df.empty:
    print('Data frame is empty, choose another cre line & visual area combination.')

# Assign the ID column as the index and return dataframe
exp_cont_df = exp_cont_df.set_index('id')
exp_cont_df


# Let's look into one of these experiment containers, most of which have three different sessions for different types of visual stimuli. We can call `get_ophys_experiments()` on our `boc` object to return the experiments within a container. This method takes in the arguments `experiment_container_ids` and `stimuli` which both require lists. We can select an id from our dataframe and choose a stimuli. In our case, we'll filter for experiments with the `natural_scenes` stimuli. 

# In[6]:


# Assign experiment container id and stimuli 
exp_container_id = 627823571
stim = ['natural_scenes']

# Call experiment container for our id and stimuli of interest
experiments = boc.get_ophys_experiments(experiment_container_ids = [exp_container_id],
                                   stimuli = stim)

# Print out our container 
print(experiments)


# **Note**: You can execute `get_all_stimuli()` on the `boc` object if you are unsure of what stimuli are available. Not all experiments or experiment contiainers will have every stimuli in their datasets. 

# In[7]:


print('Stimuli found in Brain Observatory:')
boc.get_all_stimuli()


# Now, let's download the experiment data using the `get_ophys_experiment_data` method. If you look closley above, you can see that `experiments` is a list of dictionaries for each experiment in our assigned container. We will need to input the session id of our experiment into this method. 
# 
# **Note**: The cell below downloads some data, and make take a minute or so to run. It is important that you do not interrupt the download of the data or else the file will become corrupted and you will have to delete it and try again. 

# In[8]:


# Note: This id is different from our experiment container id 
session_id = experiments[0]['id']
data = boc.get_ophys_experiment_data(session_id)

# Take a look at the kind of object data is 
print(data)


# The returned output is data accessor object that can be used to perform analyses that we will discuss in the next section. 

# That's how you retrieve an experiment from the Allen Brain Observatory! If you want to retrieve multiple experiments across multiple brain areas or cell types, you can use the `get_experiment_containers` method without specifying a targeted structure or brain area, and then subset your dataframe. There are many different types of analyses that can be done with this data. For example, we can creat a maximum projection image of the data to see how our cells respond to certain stimuli. We can also find out if our cells, if any, are direction selective. We will go over how to perform these analyses, and more, in the next two sections.

# In[ ]:




