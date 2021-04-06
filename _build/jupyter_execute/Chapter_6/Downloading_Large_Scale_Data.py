#!/usr/bin/env python
# coding: utf-8

#  # Downloading Large Scale Data

# This section will teach you how to interact with the Neuropixels dataset, specifically how to download experimental sessions, return procesed data, and subset your data to contain only brain regions you are interested in. 
# 
# We will first need to import the `EcephysProjectCache` from the Allen SDK and create an instance of the class. The class is needed to download the metadata and data of the Neuropixels dataset and contains methods used to return information on our experiments. For the full list of methods, please visit the <a href = 'https://allensdk.readthedocs.io/en/v1.7.1/allensdk.brain_observatory.ecephys.ecephys_project_cache.html'> original documentation</a>.
# 
# Below we will execute `get_session_table()` on our `EcephysProjectCache` object which will return a dataframe with metadata on each experiment session. 

# In[1]:


# Import the Neuropixels Cache
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache

# We have all of this data on the datahub! This is where it lives.
manifest_path = '/Users/VictorMagdaleno/NeuralDataScience.github.io/Chapter_6/datasets/manifest.json' 

# Create the EcephysProjectCache object
cache = EcephysProjectCache(manifest=manifest_path)

# Get the sessions available in this dataset
sessions = cache.get_session_table()
print('Total number of sessions: ' + str(len(sessions)))
sessions.head()


# Let's say we only want sessions where the data has recordings from CA1. We can do the following to create a session list that we want.

# In[2]:


# Create a session list based on some criteria

session_list = []

for idx,structure_list in enumerate(sessions['ecephys_structure_acronyms']):
    if 'CA1' in structure_list:
        session_list.append(sessions.index[idx])   
        
print('There are '+str(len(session_list))+' sessions that meet this criteria:')
print(session_list)


# Now, we can use the session list to get the data we want. Unfortunately, it looks like we can only extract one experiment as a time, so if you want to do this for multiple experiments, you'll need to loop over the `get_session-data` method for your entire session_list. For example, your workflow might be:
# 
# 1. Extract one session.
# 2. Look for units recorded from your brain region of interest in that session.
# 3. Extract whatever metric you're interested in (e.g., firing rate).
# 4. Append those values to a list of firing rates.
# 5. Loop back around to the next session.
# 
# Here, we'll just take the first session as an example.

# In[3]:


session = cache.get_session_data(session_list[2])


# In[ ]:




