#!/usr/bin/env python
# coding: utf-8

#  # Downloading Large Scale Data

# This section will teach you how to interact with the Neuropixels dataset, specifically how to download experimental sessions, return procesed data, and subset your data to contain only brain regions you are interested in. 
# 
# We will first need to import the `EcephysProjectCache` from the Allen SDK and create an instance of the class. The class is used to download the metadata and data for all sessions in the Neuropixels dataset. For the full list of methods, please visit the <a href = 'https://allensdk.readthedocs.io/en/v1.7.1/allensdk.brain_observatory.ecephys.ecephys_project_cache.html'> original documentation</a>.
# 
# Below we will execute `get_session_table()` on our `EcephysProjectCache` object which will return a dataframe with metadata on each session. 

# In[1]:


import warnings
warnings.filterwarnings('ignore')

# Import the Neuropixels Cache
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache

# Assign where data will be stored
manifest_path = 'manifest.json' 

# Create the EcephysProjectCache object
cache = EcephysProjectCache(manifest=manifest_path)

# Return all sessions available in this dataset
sessions = cache.get_session_table()
print('Total number of sessions: ' + str(len(sessions)))
sessions.head()


# A few columns that we may want to pay attention to for future analysis are the `full_genotype`, `unit_count`, and `ecephys_structure_acronyms`. 
# 
# In this dataset, a `unit` referes to an individual neuron that was recorded in the session. The `unit_count` refers to the total number of neurons recorded in a particluar sesssion. As mentioned in the chapter introduction, three different genotypes were used alongside the wildtype for these experiments. You can find the genotype under `full_genotype`. Lastly, you can find what structures the data in a session was collected from under `ecephys_structure_acronyms`.
# 
# Below we will return the follwoing information on our sessions: 
# - how many sessions per genotype
# - the average number of units recorded per session
# - what brain structures were used in our sessions

# In[2]:


genotypes = sessions['full_genotype'].value_counts()

avg_units = sessions['unit_count'].mean()

brain_areas = []

for idx,structure in sessions.iterrows():
    for i in structure['ecephys_structure_acronyms']:
        if i not in brain_areas:
            brain_areas.append(i)
        else:
            continue

print('Genotype Count:')
print(genotypes)

print('\n Average Units:')
print(avg_units)

print('\n All brain areas:')
print(brain_areas)


# Let's say we only want sessions where the data has recordings from CA1. We can do the following to create a session list that we want.

# In[3]:


# Create a session list based on some criteria

session_list = []

for idx,structure_list in enumerate(sessions['ecephys_structure_acronyms']):
    if 'CA1' in structure_list:
        session_list.append(sessions.index[idx])   
        
print('There are '+str(len(session_list))+' sessions that meet this criteria:')
print(session_list)


# ## Single Session

# Now, we can use the session list to get the data we want. Unfortunately, it looks like we can only extract one experiment as a time, so if you want to do this for multiple experiments, you'll need to loop over the `get_session_data` method for your entire session_list. For example, your workflow might be:
# 
# 1. Extract one session.
# 2. Look for units recorded from your brain region of interest in that session.
# 3. Extract whatever metric you're interested in (e.g., firing rate).
# 4. Append those values to a list of firing rates.
# 5. Loop back around to the next session.
# 
# The `get_session_data` downloads the `NWB` data file of our experiment session and returns a session object that contains data and metadata for a single session. For a full list of methods and attributes for an ecephys session object, please visit the <a href = 'https://allensdk.readthedocs.io/en/v1.7.1/allensdk.brain_observatory.ecephys.ecephys_session.html'> original dcumentation</a>. Here, we'll just take one session as an example.

# **Note**: The session files are very large files that will take some time to download depending on your connection speed. It is important that you do not stop the download as the cell is running becasue this will truncate the file and you will not be able to work with the data. The cell block below creates a new instance of `EcephysProjectCache` with a larger `timeout` value to ensure enough time is allowed for the file to download. 

# In[4]:


from allensdk.brain_observatory.ecephys.ecephys_project_api import EcephysProjectWarehouseApi
from allensdk.brain_observatory.ecephys.ecephys_project_api.rma_engine import RmaEngine

cache = EcephysProjectCache(manifest=manifest_path,
                            fetch_api=EcephysProjectWarehouseApi(RmaEngine(scheme="http",host="api.brain-map.org",timeout= 50 * 60)))          


# In[5]:


# Download our session data 
session = cache.get_session_data(session_list[1])
print('Session downloaded.')


# In the next section we will go over how to use the metrics in `units` to plot the behavior of our neurons. 

# In[ ]:




