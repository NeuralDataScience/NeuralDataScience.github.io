#!/usr/bin/env python
# coding: utf-8

# # Working with NWB in Python 

# ## About NWB

# - many obstacles in data sharing, especially in neuroscience 
# - there is currently too much data in neuroscience to work with 
# - too much data makes it difficult to share and analyze with scientisits around the worls 
# - "The aim of Neurodata Without Borders is to standardize neuroscience data on an international scale"
# - creating a standard format for neuroscience data will mamke it easier to share and contribute to open soruce projects which will accelerate discovery 

# ## Goal

# - develop a unified, extensible, open-source data format for cellular-based neurophysiology data
# - create a standard for neuroscience datasets to imporve the collaboration of neuroscience projects around the world 

# ## Current Conflict 

# - neuroscience does not have a standardized way to collect and share data
# - no common standard means it is difficult for labs to share and compare results with one another 
# - not being able to compare results and replicate experiments slows down the overall progression of the field 

# ## Neurodata Without Borders: Neurophysiolgy 

# - a common standard to share, store, and build analysis tools for neuroscience data 
# - contains software to stadardize data, API's to read and write data, and important datasets in the neuroscience community that have been converted to NWB format 
# - takes into account experimental design, experimental subjects, behavior, data aquisition, neural activity, and extensions 

# ## NWB Tutorials: Object IDs 

# In[1]:


from pynwb import NWBFile, TimeSeries
from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np

# set up the NWBFile
start_time = datetime(2019, 4, 3, 11, tzinfo=tzlocal())
nwbfile = NWBFile(session_description='demonstrate NWB object IDs',
                  identifier='NWB456',
                  session_start_time=start_time)

# make some fake data
timestamps = np.linspace(0, 100, 1024)
data = np.sin(0.333 * timestamps) + np.cos(0.1 * timestamps) + np.random.randn(len(timestamps))
test_ts = TimeSeries(name='raw_timeseries', data=data, unit='m', timestamps=timestamps)

# add it to the NWBFile
nwbfile.add_acquisition(test_ts)

# print the object ID of the NWB file
print(nwbfile.object_id)

# print the object ID of the TimeSeries
print(test_ts.object_id)


# In[2]:


nwbfile.objects


# In[3]:


for oid in nwbfile.objects:
    print(nwbfile.objects[oid])


# In[4]:


ts_id = test_ts.object_id
my_ts = nwbfile.objects[ts_id]  # test_ts == my_ts
my_ts


# In[5]:


for obj in nwbfile.objects.values():
    print('%s: %s "%s"' % (obj.object_id, obj.neurodata_type, obj.name))


# ## NWB Tutorials: NWB Basics 

# In[6]:


# The NWB file 
start_time2 = datetime(2017, 4, 3, 11, tzinfo=tzlocal())
create_date2 = datetime(2017, 4, 15, 12, tzinfo=tzlocal())

nwbfile2 = NWBFile(session_description='demonstrate NWBFile basics',  # required
                  identifier='NWB123',  # required
                  session_start_time=start_time2,  # required
                  file_create_date=create_date2)  # optional
print(nwbfile2)


# In[7]:


# Time Series Data
from pynwb import TimeSeries

data2 = list(range(100, 200, 10))
timestamps2 = list(range(10))
test_ts2 = TimeSeries(name='test_timeseries', data=data2, unit='m', timestamps=timestamps2)
print(timestamps2)
print(test_ts2)


# In[8]:


# Uniform Sampled rate 
rate_ts = TimeSeries(name='test_timeseries', data=data2, unit='m', starting_time=0.0, rate=1.0)
rate_ts


# In[9]:


nwbfile2.add_acquisition(test_ts)


# In[10]:


nwbfile2


# In[11]:


nwbfile2.acquisition['test_timeseries']


# In[28]:


nwbfile2.objects


# In[ ]:


# Writing an NWB file 

