#!/usr/bin/env python
# coding: utf-8

# # Obtaining and Working with NWB Datasets
# 
# NWB datasets can be found in a few different places. In this textbook, we'll introduce two primary ways to obtain NWB datasets: through DANDI, and through the Allen Institute SDK. This chapter deals with obtaining and analyzing a sample dataset via DANDI.
# 
# ### Neurodata Without Borders: Neurophysiology
# All of the datasets that we'll work with here are in the [Neurodata Without Borders: Neurophysiology (NWB:N)](https://www.nwb.org/nwb-neurophysiology/) format. NWB:N is the common standard to share, store, and build analysis tools for neuroscience data. NWB:N contains software to stadardize data, APIs to read and write data, and important datasets in the neuroscience community that have been converted to NWB format. As we'll see in our first dataset, NWB:N also includes factors such as experimental design, experimental subjects, behavior, data aquisition, neural activity, and extensions.
# 
# Several of the available NWB:N datasets are highlighted on the [NWB website](https://www.nwb.org/example-datasets/). 
# 
# In this chapter, we'll dig into one of the datasets that uses a technology known as Neuropixels to simultaneously record from many neurons. First, let's get the dataset.
# 
